from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from chat.UserManager import UserManager
from misc.buttons import intervalButtonsMarkup


class onMessageReceivedHandler(MessageHandler):
    def __init__(self):
        MessageHandler.__init__(self, filters.TEXT & (~filters.COMMAND), self.onMessageReceived)

    @staticmethod
    async def onMessageReceived(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = UserManager.getUser(update.effective_chat)
        if user.state == "setting_notif_msg":
            user.extra["msg"] = update.message.text
            user.state = "setting_interval"
            user.extra["interval"] = [1, 0, 0]
            interval = user.extra["interval"]
            await update.effective_chat.send_message(
                f"Как часто мне следует напоминать вам об этом?\n"
                f"Раз в {interval[0]} дней {interval[1]} часов и {interval[2]} минут?",
                reply_markup=intervalButtonsMarkup)
