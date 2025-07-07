import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

with open("token.txt", mode="r", encoding="utf-8") as f:
    TOKEN = f.read()

logging.basicConfig(format='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s', level=logging.INFO)


async def onStartCommand(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def onMessageReceived(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


application = ApplicationBuilder().token(TOKEN).build()
start_handler = CommandHandler('start', onStartCommand)
message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), onMessageReceived)
application.add_handler(start_handler)
application.add_handler(message_handler)
application.run_polling()
