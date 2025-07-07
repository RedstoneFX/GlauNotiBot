from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters


class onMessageReceivedHandler(MessageHandler):
    def __init__(self):
        MessageHandler.__init__(self, filters.TEXT & (~filters.COMMAND), self.onMessageReceived)

    @staticmethod
    async def onMessageReceived(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
