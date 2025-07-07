from telegram import Update
from telegram.ext import ContextTypes, CallbackQueryHandler


class onButtonClickedHandler(CallbackQueryHandler):
    def __init__(self):
        CallbackQueryHandler.__init__(self, self.onButtonClicked)

    @staticmethod
    async def onButtonClicked(update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Selected option: {query.data}")
        # await query.edit_message_text(text=f"Selected option: {query.data}")
