from telegram import Update
from telegram.ext import ContextTypes, CallbackQueryHandler

from chat.UserManager import UserManager
from misc.buttons import intervalButtonsMarkup


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
            await update.effective_chat.send_message("Хорошо. Что я должен буду вам сказать, чтобы напомнить вам об "
                                                     "этом?")
            user.state = "setting_notif_msg"

        elif user.state == "setting_interval":
            if query.data == "submit":
                await update.effective_message.edit_text("Хорошо. Теперь нужно ждать, пока реализуют запрос даты начала.")
            else:
                interval = user.extra["interval"]

                if query.data == "+day":
                    interval[0] += 1
                elif query.data == "-day":
                    if interval[0] > 0:
                        interval[0] -= 1
                elif query.data == "+7days":
                    interval[0] += 7
                elif query.data == "-7days":
                    if interval[0] >= 7:
                        interval[0] -= 7

                elif query.data == "+hour":
                    interval[1] += 1
                elif query.data == "-hour":
                    if interval[1] > 1:
                        interval[1] -= 1
                elif query.data == "+6hours":
                    interval[1] += 6
                elif query.data == "-6hours":
                    if interval[1] >= 6:
                        interval[1] -= 6

                elif query.data == "+10mins":
                    interval[2] += 10
                elif query.data == "-10mins":
                    if interval[2] >= 10:
                        interval[2] -= 10
                elif query.data == "+30mins":
                    interval[2] += 30
                elif query.data == "-30mins":
                    if interval[2] >= 30:
                        interval[2] -= 30

                if interval == [0, 0, 0]:
                    interval[2] = 10
                if interval[2] >= 60:
                    interval[1] += interval[2] // 60
                    interval[2] %= 60
                if interval[1] >= 24:
                    interval[0] += interval[1] // 24
                    interval[1] %= 24

                await update.effective_message.edit_text(
                    f"Текущий интервал: раз в {interval[0]} дней {interval[1]} часов и {interval[2]} минут",
                    reply_markup=intervalButtonsMarkup)

    @staticmethod
    async def sendUserList(chat):
        msg = "Пользователи:"
        for user in UserManager.users.values():
            msg += f"\n@{user.name} [{user.chatID}]" + (" (admin)" if user.isAdmin else "")
        await chat.send_message(msg)
