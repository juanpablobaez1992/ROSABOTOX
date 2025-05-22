# bot/handlers/text.py

from telegram import Update
from telegram.ext import ContextTypes
from core.link_parser import extract_article_from_link
from core.text_processor import generate_article_structure
from wordpress.media import upload_image_to_wordpress
import requests
import os

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text.startswith("http://") or text.startswith("https://"):
        try:
            article_data = extract_article_from_link(text)

            # Construir texto con fuente al final
            full_text = f"{article_data['title']}\n\n{article_data['text']}\n\nFuente: {article_data['source']}"
            article = generate_article_structure(full_text)
            context.user_data["article"] = article

            # Descargar y subir imagen destacada si existe
            image_url = article_data.get("top_image")
            if image_url:
                try:
                    response = requests.get(image_url)
                    if response.status_code == 200:
                        os.makedirs("temp", exist_ok=True)
                        image_path = f"temp/auto_image.jpg"
                        with open(image_path, 'wb') as f:
                            f.write(response.content)

                        image_id = upload_image_to_wordpress(image_path, "auto_image.jpg")
                        context.user_data["featured_image_id"] = image_id
                        await update.message.reply_text("✅ Imagen destacada asignada automáticamente.")
                except Exception:
                    await update.message.reply_text("⚠️ No se pudo descargar la imagen del artículo.")

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
        except Exception as e:
            await update.message.reply_text(f"❌ Error al procesar el link:\n{str(e)}")
    else:
        await update.message.reply_text(f"Texto recibido:\n\n{text}")
