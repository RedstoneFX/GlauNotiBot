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