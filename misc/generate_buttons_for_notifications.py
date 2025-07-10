from time import time

from telegram import InlineKeyboardButton

from chat.NotificationManager import Notification, NotificationManager
from misc.convert_delta_to_str import convert_delta_to_str
from misc.cut_string import cut_string


def generate_buttons_for_notifications(notifications: list[Notification]):
    buttons = []
    for notification in notifications:
        next_time = convert_delta_to_str(NotificationManager.get_next_time(notification.id) - time())
        buttons.append(
            [
                InlineKeyboardButton(
                    "\"" + cut_string(notification.message, 24) + "\" через " + next_time,
                    callback_data="notification." + str(notification.id)
                )
            ]
        )
    return buttons

def generate_buttons_for_notification(notification_id: int, confirm_removal=False):
    cf = "remove_notification" if confirm_removal else "want_to_remove_notification"
    del_msg = "Подтвердить удаление" if confirm_removal else "Удалить"
    buttons = [
            [InlineKeyboardButton(del_msg, callback_data=cf + "." + str(notification_id))],
            [InlineKeyboardButton("<- назад", callback_data="list_notifications")]
        ]
    # TODO: редактирование
    return buttons