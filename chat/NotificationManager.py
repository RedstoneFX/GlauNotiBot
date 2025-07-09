from queue import PriorityQueue
from time import time
from datetime import timedelta

from telegram import Bot

import asyncio

from telegram.ext import CallbackContext

from chat.UserManager import UserManager
from misc.buttons import notificationReadMarkup


class Notification:
    def __init__(self, timestamp: float, index: int, chat_id: int, message: str, interval: float):
        self.timestamp = timestamp
        self.index = index
        self.chat_id = chat_id
        self.message = message
        self.interval = interval

    def to_dict(self) -> dict:
        notif_dict = dict()
        notif_dict["timestamp"] = self.timestamp
        notif_dict["index"] = self.index
        notif_dict["chat_id"] = self.chat_id
        notif_dict["message"] = self.message
        notif_dict["interval"] = self.interval
        return notif_dict

    @classmethod
    def from_dict(cls, data: dict) -> 'Notification':
        return cls(
            timestamp=data["timestamp"],
            index=data["index"],
            chat_id=data["chat_id"],
            message=data["message"],
            interval=data["interval"]
        )


class NotificationManager:
    filename = None
    queue = PriorityQueue()
    pending = dict()
    accepted = []
    lastIndex = 0
    _queue = PriorityQueue()
    _pending = {}  # message_id: Notification
    _accepted = [] # Notification
    _last_index = 0

    @staticmethod
    def save():
        pass

    @staticmethod
    def load():
        pass

    # Добавить новое уведомление в очередь
    @classmethod
    def add_notification(cls, timestamp: float, chat_id: int, msg: str, interval: float) -> int:
        cls._last_index += 1
        notification = Notification(timestamp, cls._last_index, chat_id, msg, interval)
        cls._queue.put((notification.timestamp, notification))
        cls.save()
        return notification.index

    # Отправить уведомления по времени
    @classmethod
    async def send_expired_notifications(cls, context: CallbackContext):
        while not cls._queue.empty() and cls._queue.queue[0][0] <= time():
            _, notification = cls._queue.get()
            try:
                msg = await context.bot.send_message(
                    chat_id=notification.chat_id,
                    text=notification.message,
                    reply_markup=notificationReadMarkup
                )
                cls._pending[msg.message_id] = notification

                # Обработка интервальных (повторяющихся) уведомлений
                if notification.interval > 0:
                    new_notification = Notification(
                        timestamp=notification.timestamp + notification.interval,
                        index=notification.index,
                        chat_id=notification.chat_id,
                        message=notification.message,
                        interval=notification.interval
                    )
                    cls._queue.put((new_notification.timestamp, new_notification))

                cls.save()
            except Exception as e:
                print(f"Не удалось отправить уведомление: {e}")
                cls._queue.put((notification.timestamp, notification))


    # Уведомить администраторов о прочитанных уведомлениях
    @classmethod
    async def notify_accepted_to_admins(cls, context: CallbackContext):
        if not cls._accepted:
            return

        messages = []
        current_time = time()

        for notification in cls._accepted:
            delta = current_time - notification.timestamp
            if delta < 15 * 60:
                continue

            user = UserManager.users.get(notification.chat_id)
            user_name = getattr(user, 'name', 'Unknown')
            seconds = delta % 60
            minutes = delta // 60 % 60
            hours = delta // 360 % 24
            days = delta // 360 // 24
            if days != 0:
                delta_str = f"{days} дней и {hours} часов"
            elif hours != 0:
                delta_str = f"{hours} часов и {minutes} минут"
            else:
                delta_str = f"{minutes} минут и {seconds} секунд"
            messages.append(f"Пользователь {user_name} прочитал уведомление {delta_str} назад")

        if messages:
            for user in UserManager.users.values():
                if getattr(user, 'isAdmin', False):
                    await context.bot.send_message(
                        chat_id=user.chatID,
                        text="\n".join(messages)
                    )
            cls._accepted.clear()
            cls.save()


    @staticmethod
    async def notifyPendingToAdmins(context: CallbackContext):
        for user in UserManager.users.values():
            hugeMsg = ""
            if user.isAdmin:
                for pending in NotificationManager.pending.values():
                    delta = round(time() - pending[0])
                    if delta < 15 * 60:
                        continue

                    seconds = delta % 60
                    minutes = delta // 60 % 60
                    hours = delta // 360 % 24
                    days = delta // 360 // 24

                    if days != 0:
                        deltamsg = f"{days} дней и {hours} часов"
                    elif hours != 0:
                        deltamsg = f"{hours} часов и {minutes} минут"
                    else:
                        deltamsg = f"{minutes} минут и {seconds} секунд"

                    hugeMsg += "Пользователю " + UserManager.users[pending[2]].name + \
                               " было отправлено уведомление, но оно непрочитано уже " + deltamsg + "\n"
                if hugeMsg != "":
                    await context.bot.send_message(user.chatID, hugeMsg.strip())

    @staticmethod
    def setNotificationSeen(messageID):
        NotificationManager.accepted.append(NotificationManager.pending.pop(messageID))