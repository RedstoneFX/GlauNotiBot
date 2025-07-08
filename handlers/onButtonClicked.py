from telegram import Update
from telegram.ext import ContextTypes, CallbackQueryHandler

from chat.UserManager import UserManager


class onButtonClickedHandler(CallbackQueryHandler):
    def __init__(self):
        CallbackQueryHandler.__init__(self, self.onButtonClicked)

    @staticmethod
    async def onButtonClicked(update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        if query.data == "get_users":
            msg = "Пользователи:"
            for user in UserManager.users.values():
                msg += f"\n@{user.name} [{user.chatID}]" + (" (admin)" if user.isAdmin else "")
            await update.effective_chat.send_message(msg)
