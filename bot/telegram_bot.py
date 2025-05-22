# bot/telegram_bot.py

from telegram.ext import ApplicationBuilder
from bot.handlers import register_handlers
from config import TELEGRAM_BOT_TOKEN

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    register_handlers(app)
    print("Bot corriendo...")
    app.run_polling()
    print("Bot started.")

if __name__ == "__main__":
    main()
