# bot/handlers/image.py

from telegram import Update
from telegram.ext import ContextTypes
from wordpress.media import upload_image_to_wordpress
import os

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photos = update.message.photo
    if not photos:
        await update.message.reply_text("No recibí ninguna foto.")
        return

    photo = photos[-1]
    file = await context.bot.get_file(photo.file_id)

    os.makedirs("temp", exist_ok=True)
    image_path = f"temp/{photo.file_unique_id}.jpg"
    await file.download_to_drive(image_path)

    try:
        image_id = upload_image_to_wordpress(image_path, os.path.basename(image_path))
        context.user_data["featured_image_id"] = image_id
        await update.message.reply_text("✅ Imagen destacada subida con éxito. Enviá /publicar para asociarla al post.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error al subir imagen: {str(e)}")
