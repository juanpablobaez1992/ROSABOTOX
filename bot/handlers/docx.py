# bot/handlers/docx.py

from telegram import Update, Document
from telegram.ext import ContextTypes
from core.docx_parser import extract_text_from_docx
from core.text_processor import generate_article_structure
import os

async def handle_docx(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document: Document = update.message.document
    if document.mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        os.makedirs("temp", exist_ok=True)
        file_path = f"temp/{document.file_name}"
        file = await context.bot.get_file(document.file_id)
        await file.download_to_drive(file_path)

        extracted_text = extract_text_from_docx(file_path)
        article = generate_article_structure(extracted_text)
        context.user_data["article"] = article

        preview = f"""📝 <b>Vista previa del artículo</b>

<b>Título:</b> {article['title']}
<b>Subtítulo:</b> {article['excerpt']}
<b>Categoría:</b> {article['categories'][0] if article['categories'] else 'Sin clasificar'}
<b>Slug:</b> {article['slug']}
<b>Etiquetas:</b> {", ".join(article['tags'])}
<b>SEO keywords:</b> {", ".join(article['seo']['keywords'])}

<b>Cuerpo:</b>
{article['body'][:1000]}{"..." if len(article['body']) > 1000 else ""}
"""
        await update.message.reply_text(preview, parse_mode="HTML")
        await update.message.reply_text("¿Listo para publicar? Enviá /publicar para crear el borrador en WordPress.")
    else:
        await update.message.reply_text("Solo acepto archivos .docx por ahora.")
