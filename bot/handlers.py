# bot/handlers.py

from telegram import Update, Document
from telegram.ext import CommandHandler, MessageHandler, filters, ContextTypes
from core.docx_parser import extract_text_from_docx
from core.text_processor import generate_article_structure
from core.link_parser import extract_text_from_link
from wordpress.wp_api import create_draft_post
import os

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hola 👋\nEnviame un archivo .docx, texto o link para convertirlo en una nota periodística."
    )

async def handle_docx(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document: Document = update.message.document
    if document.mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        os.makedirs("temp", exist_ok=True)
        file_path = f"temp/{document.file_name}"
        file = await context.bot.get_file(document.file_id)
        await file.download_to_drive(file_path)

        extracted_text = extract_text_from_docx(file_path)
        article = generate_article_structure(extracted_text)

        context.user_data["article"] = article  # Guardar en memoria para /publicar

        preview = f"""📝 <b>Vista previa del artículo</b>

<b>Título:</b> {article['title']}
<b>Slug:</b> {article['slug']}
<b>Extracto:</b> {article['excerpt']}
<b>SEO keywords:</b> {", ".join(article['seo']['keywords'])}

<b>Cuerpo:</b>
{article['body'][:1000]}{"..." if len(article['body']) > 1000 else ""}
        """

        await update.message.reply_text(preview, parse_mode="HTML")
        await update.message.reply_text("¿Listo para publicar? Enviá /publicar para crear el borrador en WordPress.")
    else:
        await update.message.reply_text("Solo acepto archivos .docx por ahora.")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text.startswith("http://") or text.startswith("https://"):
        try:
            extracted_text = extract_text_from_link(text)
            article = generate_article_structure(extracted_text)

            context.user_data["article"] = article

            preview = f"""📝 <b>Vista previa del artículo</b>

<b>Título:</b> {article['title']}
<b>Slug:</b> {article['slug']}
<b>Extracto:</b> {article['excerpt']}
<b>SEO keywords:</b> {", ".join(article['seo']['keywords'])}

<b>Cuerpo:</b>
{article['body'][:1000]}{"..." if len(article['body']) > 1000 else ""}
            """

            await update.message.reply_text(preview, parse_mode="HTML")
            await update.message.reply_text("¿Listo para publicar? Enviá /publicar para crear el borrador en WordPress.")
        except Exception as e:
            await update.message.reply_text(f"❌ Error al procesar el link:\n{str(e)}")
    else:
        await update.message.reply_text(f"Texto recibido:\n\n{text}")
        # En el futuro: también podemos procesar texto plano como nota

async def publicar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    article = context.user_data.get("article")

    if not article:
        await update.message.reply_text("No hay artículo para publicar. Primero enviá un archivo .docx o un link.")
        return

    try:
        wp_response = create_draft_post(article)
        await update.message.reply_text(
            f"✅ Publicado como borrador en WordPress:\n{wp_response['link']}"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error al publicar en WordPress:\n{str(e)}")

def register_handlers(app):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("publicar", publicar))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_docx))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

