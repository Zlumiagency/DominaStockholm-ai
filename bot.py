from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from config import TELEGRAM_TOKEN
from assistant import ask_ai


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Domina Stockholm AI.\n\nHow may I assist you today?"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Simply write your message and I'll help you."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user
    message = update.message.text

    await update.message.chat.send_action(ChatAction.TYPING)

    try:

        answer = ask_ai(
            user_id=user.id,
            username=user.username or "",
            message=message,
        )

        await update.message.reply_text(answer)

    except Exception as e:

        print(e)

        await update.message.reply_text(
            "Something went wrong. Please try again."
        )


def main():

    app = Application.builder().token(
        TELEGRAM_TOKEN
    ).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message,
        )
    )

    print("🚀 Domina Stockholm AI is running...")

    app.run_polling()


if __name__ == "__main__":
    main()