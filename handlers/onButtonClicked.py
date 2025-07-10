from datetime import datetime, date, timedelta
from calendar import monthrange

from telegram import Update
from telegram.ext import ContextTypes, CallbackQueryHandler

from chat.LangManager import LangManager
from chat.NotificationManager import NotificationManager
from chat.UserManager import UserManager

from misc.buttons import intervalButtonsMarkup, daytimeButtonsMarkup
from misc.convert_delta_to_str import convert_delta_to_str
from misc.generateMonthButtons import generateMonthButtons

from telegram import InlineKeyboardMarkup

from misc.generate_buttons_for_notifications import generate_buttons_for_notifications, \
    generate_buttons_for_notification
from misc.generate_question_buttons import generate_groups_buttons_markup, generate_group_buttons_markup


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
            msg = "Пользователи:"
            for user in UserManager.users.values():
                msg += f"\n@{user.name} [{user.chatID}]" + (" (admin)" if user.isAdmin else "")
            await update.effective_chat.send_message(msg)

        elif query.data == "accepted":
            await update.effective_message.edit_text("(Прочитано) " + update.effective_message.text)
            await NotificationManager.notify_notification_seen(update.effective_chat.id, update.effective_message.id, context.bot)

        elif query.data == "add_notification":
            await update.effective_chat.send_message("Хорошо. Что я должен буду вам сказать, чтобы напомнить вам об "
                                                     "этом?")
            user.state = "setting_notif_msg"

        elif parts[0] == "ask_group":
            if parts[1] == "list_all":
                await update.effective_message.edit_text("Либо вы не знаете, что вам нужно, либо вы проверяете меня. Как скажете, вот:",
                                                         reply_markup=generate_group_buttons_markup("", "ru_ru", True))
            else:
                await update.effective_message.edit_text(
                    "Вот вопросы из этой группы:",
                    reply_markup=generate_group_buttons_markup(parts[2], "ru_ru"))

        elif query.data == "ask_buttons":
            await update.effective_message.edit_text("Конечно! В какой области интересующий вас вопрос?",
                                                     reply_markup=generate_groups_buttons_markup("ru_ru"))

        elif parts[0] == "ask":
            answer = LangManager.get(parts[1], "ru_ru")
            await update.effective_message.edit_text(answer.extra["title"] + "\n\n" + answer.body)

        elif query.data == "list_notifications" or parts[0] == "remove_notification":

            if parts[0] == "remove_notification":
                notification_id = int(parts[1])
                await NotificationManager.notify_notification_removed(notification_id, context.bot)
                NotificationManager.remove(notification_id)

            notifications = NotificationManager.get_notifications_for_chat(update.effective_chat.id)
            if not notifications:
                await update.effective_message.edit_text("У вас нет ни одного прикрепленного уведомления. Напишите /start, чтобы создать такое.")
                return
            buttons = generate_buttons_for_notifications(notifications)
            await update.effective_message.edit_text("Вот уведомления, закрипленные за вами:",
                                                     reply_markup=InlineKeyboardMarkup(buttons))

        elif parts[0] == "notification" or parts[0] == "want_to_remove_notification":
            notification = NotificationManager.get(int(parts[1]))
            if not notification:
                await update.effective_message.edit_text("Кажется, этого уведомления больше нет.")
            else:
                interval = "Один раз" if notification.interval == 0 else convert_delta_to_str(notification.interval)
                await update.effective_message.edit_text(
                    "Вот информация об этом уведомлении:" +
                    "\n\n\"" + notification.message + "\"" +
                    "\n\nИнтервал: " + interval +
                    "\nСледующее сообщение через: " +
                    convert_delta_to_str(NotificationManager.get_time_before_next(notification.id)),
                    reply_markup=InlineKeyboardMarkup(generate_buttons_for_notification(notification.id, parts[0] == "want_to_remove_notification"))
                )

        elif user.state == "setting_time":
            chosen_datetime = user.extra["datetime"]
            if query.data == "+6hours":
                chosen_datetime[3] += 6
            elif query.data == "+hour":
                chosen_datetime[3] += 1
            elif query.data == "-6hours":
                chosen_datetime[3] -= 6
            elif query.data == "-hour":
                chosen_datetime[3] -= 1
            elif query.data == "+30mins":
                chosen_datetime[4] = chosen_datetime[4] + 30
            elif query.data == "+10mins":
                chosen_datetime[4] = chosen_datetime[4] + 10
            elif query.data == "+5mins":
                chosen_datetime[4] = chosen_datetime[4] + 5
            elif query.data == "+min":
                chosen_datetime[4] = chosen_datetime[4] + 1
            elif query.data == "-30mins":
                chosen_datetime[4] = chosen_datetime[4] - 30
            elif query.data == "-10mins":
                chosen_datetime[4] = chosen_datetime[4] - 10
            elif query.data == "-5mins":
                chosen_datetime[4] = chosen_datetime[4] - 5
            elif query.data == "-min":
                chosen_datetime[4] = chosen_datetime[4] - 1

            if chosen_datetime[4] >= 60 or chosen_datetime[4] < 0:
                chosen_datetime[3] += chosen_datetime[4] // 60
                chosen_datetime[4] %= 60
            chosen_datetime[3] %= 24

            now = datetime.now()
            if datetime(*chosen_datetime) < datetime.now():
                chosen_datetime = [now.year, now.month, now.day, now.hour, now.minute+1]
                user.extra["datetime"] = chosen_datetime
                time = str(chosen_datetime[3]).rjust(2, "0") + ":" + str(chosen_datetime[4]).rjust(2, "0")
                await update.effective_message.edit_text(f"К сожалению, я не могу отправить уведомление в прошлое. Выберите другое время, пожалуйста.\n"
                                                         f"В какое время суток прислать первое уведомление?\n{time}?",
                                                         reply_markup=daytimeButtonsMarkup)
            elif query.data != "submit":
                time = str(chosen_datetime[3]).rjust(2, "0") + ":" + str(chosen_datetime[4]).rjust(2, "0")
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
                user.extra.clear()

        elif user.state == "setting_date":
            in_past = False
            actual_date = datetime.now()
            chosen_datetime = user.extra["datetime"]
            if query.data == "month_left":
                if chosen_datetime[0] == actual_date.year and chosen_datetime[1] == actual_date.month:
                    in_past = True
                else:
                    chosen_datetime[1] -= 1
                    if chosen_datetime[1] <= 0:
                        chosen_datetime[1] = 12
                        chosen_datetime[0] -= 1
                    if monthrange(chosen_datetime[0], chosen_datetime[1])[1] < chosen_datetime[2]:
                        chosen_datetime[2] = monthrange(chosen_datetime[0], chosen_datetime[1])[1]
            elif query.data == "month_right":
                chosen_datetime[1] += 1
                if chosen_datetime[1] > 12:
                    chosen_datetime[1] = 1
                    chosen_datetime[0] += 1
                if monthrange(chosen_datetime[0], chosen_datetime[1])[1] < chosen_datetime[2]:
                    chosen_datetime[2] = monthrange(chosen_datetime[0], chosen_datetime[1])[1]
            elif query.data.isdigit():
                n = int(query.data)
                if 0 < n <= monthrange(chosen_datetime[0], chosen_datetime[1])[1]:
                    if chosen_datetime[0] == actual_date.year and chosen_datetime[1] == actual_date.month and n < actual_date.day:
                        in_past = True
                    else:
                        chosen_datetime[2] = n

            if in_past:
                await update.effective_message.edit_text(
                    f"К сожалению, я не могу отправить уведомление в прошлое. Выберите другую дату, пожалуйста.\n"
                    f"Когда следует начать присылать уведомления?\n{date(chosen_datetime[0], chosen_datetime[1], chosen_datetime[2])}?",
                    reply_markup=generateMonthButtons(chosen_datetime[0], chosen_datetime[1]))
            elif query.data != "submit":
                await update.effective_message.edit_text(
                    f"Когда следует начать присылать уведомления?\n{date(chosen_datetime[0], chosen_datetime[1], chosen_datetime[2])}?",
                    reply_markup=generateMonthButtons(chosen_datetime[0], chosen_datetime[1]))
            else:
                time = str(chosen_datetime[3]).rjust(2, "0") + ":" + str(chosen_datetime[4]).rjust(2, "0")
                await update.effective_message.edit_text(f"В какое время суток прислать первое уведомление?\n{time}?",
                                                         reply_markup=daytimeButtonsMarkup)
                user.state = "setting_time"
        elif user.state == "setting_interval":
            if query.data == "once":
                user.extra["interval"] = [0, 0, 0]
                now = datetime.now()
                user.extra["datetime"] = [now.year, now.month, now.day, now.hour, now.minute]
                await update.effective_message.edit_text(f"Когда следует прислать уведомление?\n{now.date()}?",
                                                         reply_markup=generateMonthButtons(now.year, now.month))
                user.state = "setting_date"
            elif query.data == "submit":
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
