# bot/handlers/edit.py

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler

EDIT_CHOICE, EDIT_FIELD = range(2)

edit_options = ["Título", "Subtítulo", "Slug", "Cuerpo", "Categoría", "Etiquetas", "Cancelar"]

async def edit_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    article = context.user_data.get("article")
    if not article:
        await update.message.reply_text("❌ No hay artículo cargado para editar.")
        return ConversationHandler.END

    markup = ReplyKeyboardMarkup(
        [[opt] for opt in edit_options],
        one_time_keyboard=True,
        resize_keyboard=True
    )
    await update.message.reply_text("¿Qué parte querés editar?", reply_markup=markup)
    return EDIT_CHOICE

async def edit_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = update.message.text.strip().lower()
    context.user_data["edit_target"] = choice

    if choice == "cancelar":
        await update.message.reply_text("Edición cancelada.", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

    await update.message.reply_text(f"Enviame el nuevo contenido para: {choice}", reply_markup=ReplyKeyboardRemove())
    return EDIT_FIELD

async def apply_edit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    article = context.user_data.get("article")
    field = context.user_data.get("edit_target")
    new_value = update.message.text.strip()

    field_map = {
        "título": "title",
        "subtítulo": "excerpt",
        "slug": "slug",
        "cuerpo": "body",
        "categoría": "categories",
        "etiquetas": "tags"
    }

    key = field_map.get(field.lower())
    if not key:
        await update.message.reply_text("Campo no reconocido.")
        return ConversationHandler.END

    if key in ["categories", "tags"]:
        # Asignamos como lista de strings, separadas por coma
        article[key] = [s.strip() for s in new_value.split(",") if s.strip()]
    else:
        article[key] = new_value

    context.user_data["article"] = article
    await update.message.reply_text("✅ Cambios aplicados.")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Edición cancelada.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
