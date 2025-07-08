import datetime

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Chat
from telegram.ext import ContextTypes, CallbackQueryHandler

from chat.UserManager import UserManager, User

months = "0 Январь Февраль Март Апрель Май Июнь Июль Август Сентябрь Октябрь Ноябрь Декарь".split()


class onButtonClickedHandler(CallbackQueryHandler):
    def __init__(self):
        CallbackQueryHandler.__init__(self, self.onButtonClicked)

    @staticmethod
    async def onButtonClicked(update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        user = UserManager.getUser(update.effective_chat)
        if user.isAdmin:
            if user.state == "add_notif":
                user.extra["target_user"] = int(query.data)
                user.state = "add_notif_year"
                await onButtonClickedHandler.askYear(update.effective_chat, user)
            elif user.state == "add_notif_year":
                user.extra["year"] = int(query.data)
                user.state = "add_notif_month"
                await onButtonClickedHandler.askMonth(update.effective_chat, user)
            elif query.data == "get_users":
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
    async def askYear(chat: Chat, user: User):
        currentYear = datetime.datetime.now().year
        nearYears = [[InlineKeyboardButton(str(currentYear), callback_data=str(currentYear))],
                     [InlineKeyboardButton(str(currentYear + 1), callback_data=str(currentYear + 1))]]
        await chat.send_message("Теперь нужно указать дату начала отправки уведомлений. В каком году начать?",
                                reply_markup=InlineKeyboardMarkup(nearYears))

    @staticmethod
    async def askMonth(chat: Chat, user: User):
        currentDate = datetime.datetime.now()
        nearMonths = []
        minMonth = 1 if currentDate.year != user.extra["year"] else currentDate.month
        for i in range(minMonth, 13):
            nearMonths.append([InlineKeyboardButton(f"{months[i]} {user.extra['year']} года", callback_data=str(i))])
        await chat.send_message("Теперь нужно указать дату начала отправки уведомлений. В каком году начать?",
                                reply_markup=InlineKeyboardMarkup(nearMonths))

    @staticmethod
    async def sendUserList(chat):
        msg = "Пользователи:"
        for user in UserManager.users.values():
            msg += f"\n@{user.name} [{user.chatID}]" + (" (admin)" if user.isAdmin else "")
        await chat.send_message(msg)
