# bot/handlers/commands.py

from telegram import Update
from telegram.ext import ContextTypes
from wordpress.wp_api import create_draft_post

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hola 👋\nEnviame un archivo .docx, un link o una imagen para generar una nota periodística."
    )

async def publicar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    article = context.user_data.get("article")
    image_id = context.user_data.get("featured_image_id")

    if not article:
        await update.message.reply_text("No hay artículo para publicar. Primero enviá un archivo .docx o un link.")
        return

    try:
        wp_response = create_draft_post(article, featured_image_id=image_id)
        await update.message.reply_text(
            f"✅ Publicado como borrador en WordPress:\n{wp_response['link']}"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error al publicar en WordPress:\n{str(e)}")
