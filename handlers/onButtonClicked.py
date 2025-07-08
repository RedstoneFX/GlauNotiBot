from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler

from chat.UserManager import UserManager


class onButtonClickedHandler(CallbackQueryHandler):
    def __init__(self):
        CallbackQueryHandler.__init__(self, self.onButtonClicked)

    @staticmethod
    async def onButtonClicked(update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        user = UserManager.getUser(update.effective_chat)
        if query.data == "get_users":
            await onButtonClickedHandler.sendUserList(update.effective_chat)
        elif query.data == "add_notification":
            await onButtonClickedHandler.sendAddNotifMenu(update.effective_chat)

    @staticmethod
    async def sendAddNotifMenu(chat):
        userSelection = []
        for user in UserManager.users.values():
            if not user.isAdmin:
                userSelection.append([InlineKeyboardButton(f"@{user.name} [{user.chatID}]",
                                                           callback_data=str(user.chatID))])
        if len(userSelection) == 0:
            await chat.send_message("Хм... Кажется, в системе нет ни одного пользователя, не являющегося "
                                    "администратором. Администраторам не следует получать уведомления.")
        else:
            await chat.send_message("Хорошо, давайте выберем пользователя, которому требуется назначить уведомление.",
                                    reply_markup=InlineKeyboardMarkup(userSelection))
            UserManager.getUser(chat).state = "add_notif"

    @staticmethod
    async def sendUserList(chat):
        msg = "Пользователи:"
        for user in UserManager.users.values():
            msg += f"\n@{user.name} [{user.chatID}]" + (" (admin)" if user.isAdmin else "")
        await chat.send_message(msg)
