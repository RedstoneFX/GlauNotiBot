import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

with open("token.txt", mode="r", encoding="utf-8") as f:
    TOKEN = f.read()

logging.basicConfig(format='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s', level=logging.INFO)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


application = ApplicationBuilder().token(TOKEN).build()
start_handler = CommandHandler('start', start)
application.add_handler(start_handler)
application.run_polling()
