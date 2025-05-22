# bot/handlers/__init__.py

from .docx import handle_docx
from .text import handle_text
from .image import handle_photo
from .commands import start, publicar
from .edit import edit_command, edit_choice, apply_edit, cancel
from .view import ver


from telegram.ext import (
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters
)

# Estados de conversación
EDIT_CHOICE, EDIT_FIELD = range(2)

def register_handlers(app):
    # Comandos principales
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("publicar", publicar))
    app.add_handler(CommandHandler("ver", ver))


    # Manejadores de contenido
    app.add_handler(MessageHandler(filters.Document.ALL, handle_docx))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    # Conversación para /edit
    app.add_handler(ConversationHandler(
        entry_points=[CommandHandler("edit", edit_command)],
        states={
            EDIT_CHOICE: [MessageHandler(filters.TEXT, edit_choice)],
            EDIT_FIELD: [MessageHandler(filters.TEXT & ~filters.COMMAND, apply_edit)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        name="edit_conversation",
        persistent=False
    ))
