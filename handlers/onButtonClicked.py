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
        if UserManager.getUser(update.effective_chat).isAdmin:
            if query.data == "get_users":
                await onButtonClickedHandler.sendUserList(update.effective_chat)
            elif query.data == "add_notification":
                await onButtonClickedHandler.sendAddNotifMenu(update.effective_chat)

    @staticmethod
    async def sendAddNotifMenu(chat):
        await chat.send_message("")

    @staticmethod
    async def sendUserList(chat):
        msg = "Пользователи:"
        for user in UserManager.users.values():
            msg += f"\n@{user.name} [{user.chatID}]" + (" (admin)" if user.isAdmin else "")
        await chat.send_message(msg)
    