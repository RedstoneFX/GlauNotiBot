from datetime import datetime, date, timedelta
from calendar import monthrange

from telegram import Update
from telegram.ext import ContextTypes, CallbackQueryHandler

from chat.LangManager import LangManager
from chat.NotificationManager import NotificationManager
from chat.UserManager import UserManager

from misc.buttons import intervalButtonsMarkup, daytimeButtonsMarkup, getAskButtons
from misc.generateMonthButtons import generateMonthButtons

from telegram import InlineKeyboardMarkup


class onButtonClickedHandler(CallbackQueryHandler):
    def __init__(self):
        CallbackQueryHandler.__init__(self, self.onButtonClicked)

    @staticmethod
    async def onButtonClicked(update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        user = UserManager.getUser(update.effective_chat)

        parts = query.data.split('.')

        if query.data == "get_users":
            await onButtonClickedHandler.sendUserList(update.effective_chat)

        elif query.data == "accepted":
            await update.effective_message.edit_text("(Прочитано)" + update.effective_message.text)
            NotificationManager.set_notification_seen(update.effective_message.id)

        elif query.data == "add_notification":
            await update.effective_chat.send_message("Хорошо. Что я должен буду вам сказать, чтобы напомнить вам об "
                                                     "этом?")
            user.state = "setting_notif_msg"

        elif parts[0] == "ask":
            answer = LangManager.get(parts[2], parts[1])
            await update.effective_message.edit_text(answer.extra["title"] + "\n\n" + answer.body)
        elif query.data == "ask_buttons":
            await update.effective_message.edit_text("Конечно! Что именно вы хотите узнать?", reply_markup=InlineKeyboardMarkup(getAskButtons()))

        elif user.state == "setting_time":
            now = user.extra["datetime"]
            if query.data == "+6hours":
                now[3] += 6
            elif query.data == "+hour":
                now[3] += 1
            elif query.data == "-6hours":
                now[3] -= 6
            elif query.data == "-hour":
                now[3] -= 1
            elif query.data == "+30mins":
                now[4] = now[4] + 30
            elif query.data == "+10mins":
                now[4] = now[4] + 10
            elif query.data == "+5mins":
                now[4] = now[4] + 5
            elif query.data == "+min":
                now[4] = now[4] + 1
            elif query.data == "-30mins":
                now[4] = now[4] - 30
            elif query.data == "-10mins":
                now[4] = now[4] - 10
            elif query.data == "-5mins":
                now[4] = now[4] - 5
            elif query.data == "-min":
                now[4] = now[4] - 1
            if query.data != "submit":
                if now[4] >= 60 or now[4] < 0:
                    now[3] += now[4] // 60
                    now[4] %= 60
                now[3] %= 24
                time = str(now[3]).rjust(2, "0") + ":" + str(now[4]).rjust(2, "0")
                await update.effective_message.edit_text(f"В какое время суток прислать первое уведомление?\n{time}?",
                                                         reply_markup=daytimeButtonsMarkup)
            else:
                rawInterval = user.extra["interval"]
                NotificationManager.add_notification(
                    datetime(*user.extra["datetime"]).timestamp(),
                    update.effective_chat.id,
                    user.extra["msg"],
                    timedelta(days=rawInterval[0], hours=rawInterval[1], minutes=rawInterval[2]).total_seconds()
                )
                await update.effective_message.edit_text("Отлично, уведомление создано! Вызовите команду /start, "
                                                         "чтобы добавить еще уведомление.")
                user.state = "idle"

        elif user.state == "setting_date":
            now = user.extra["datetime"]
            if query.data == "month_left":
                now[1] -= 1
                if now[1] <= 0:
                    now[1] = 12
                    now[0] -= 1
                if monthrange(now[0], now[1])[1] < now[2]:
                    now[2] = monthrange(now[0], now[1])[1]
            elif query.data == "month_right":
                now[1] += 1
                if now[1] > 12:
                    now[1] = 1
                    now[0] += 1
                if monthrange(now[0], now[1])[1] < now[2]:
                    now[2] = monthrange(now[0], now[1])[1]
            elif query.data.isdigit():
                n = int(query.data)
                if 0 < n <= monthrange(now[0], now[1])[1]:
                    now[2] = n
            if query.data != "submit":
                await update.effective_message.edit_text(
                    f"Когда следует начать присылать уведомления?\n{date(now[0], now[1], now[2])}?",
                    reply_markup=generateMonthButtons(now[0], now[1]))
            else:
                time = str(now[3]).rjust(2, "0") + ":" + str(now[4]).rjust(2, "0")
                await update.effective_message.edit_text(f"В какое время суток прислать первое уведомление?\n{time}?",
                                                         reply_markup=daytimeButtonsMarkup)
                user.state = "setting_time"
        elif user.state == "setting_interval":
            if query.data == "submit":
                now = datetime.now()
                user.extra["datetime"] = [now.year, now.month, now.day, now.hour, now.minute]
                await update.effective_message.edit_text(f"Когда следует начать присылать уведомления?\n{now.date()}?",
                                                         reply_markup=generateMonthButtons(now.year, now.month))
                user.state = "setting_date"
            else:
                interval = user.extra["interval"]

                if query.data == "+day":
                    interval[0] += 1
                elif query.data == "-day":
                    interval[0] -= 1
                elif query.data == "+7days":
                    interval[0] += 7
                elif query.data == "-7days":
                    interval[0] -= 7

                elif query.data == "+hour":
                    interval[1] += 1
                elif query.data == "-hour":
                    interval[1] -= 1
                elif query.data == "+6hours":
                    interval[1] += 6
                elif query.data == "-6hours":
                    interval[1] -= 6

                elif query.data == "+10mins":
                    interval[2] += 10
                elif query.data == "-10mins":
                    interval[2] -= 10

                elif query.data == "+30mins":
                    interval[2] += 30
                elif query.data == "-30mins":
                    interval[2] -= 30

                if interval[2] >= 60:  # добавить часы, если минут больше 60
                    interval[1] += interval[2] // 60
                    interval[2] %= 60
                elif interval[2] < 0:  # Взять часы, если минут меньше 0
                    interval[1] -= abs(interval[2]) // 60 + 1
                    interval[2] += abs(interval[2]) // 60 * 60 + 60

                if interval[1] >= 24:  # Добавить дни, если часов больше 24
                    interval[0] += interval[1] // 24
                    interval[1] %= 24
                elif interval[1] < 0:  # Взять дни, если часов меньше 0
                    interval[0] -= abs(interval[1]) // 24 + 1
                    interval[1] += abs(interval[1]) // 24 * 24 + 24

                if interval[0] < 0 or interval == [0, 0, 0]:
                    interval[0] = 0
                    interval[1] = 0
                    interval[2] = 10

                await update.effective_message.edit_text(
                    f"Как часто мне следует напоминать вам об этом?\n"
                    f"Раз в {interval[0]} дней {interval[1]} часов и {interval[2]} минут?",
                    reply_markup=intervalButtonsMarkup)

    @staticmethod
    async def sendUserList(chat):
        msg = "Пользователи:"
        for user in UserManager.users.values():
            msg += f"\n@{user.name} [{user.chatID}]" + (" (admin)" if user.isAdmin else "")
        await chat.send_message(msg)
