from queue import PriorityQueue
from time import time
import json
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
    _queue = PriorityQueue()
    _pending = {}  # message_id: Notification
    _accepted = [] # Notification
    _last_index = 0


    # Сохранить все уведомления в файл
    @classmethod
    def save(cls):
        if cls.filename is None:
            return

        data = {
            'queue': [notification.to_dict() for _, notification in cls._queue.queue],
            'pending': [notification.to_dict() for notification in cls._pending.values()],
            'pending_id': list(cls._pending.keys()),
            'accepted': [notification.to_dict() for notification in cls._accepted],
            'last_index': cls._last_index
        }

        with open(cls.filename, mode="w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


    # Загрузить уведомления из файла
    @classmethod
    def load(cls):
        if cls.filename is None:
            return

        try:
            with open(cls.filename, mode="r", encoding="utf-8") as f:
                data = json.load(f)

            cls._last_index = data.get('last_index', 0)

            for notification_data in data.get('queue', []):
                notification = Notification.from_dict(notification_data)
                cls._queue.put((notification.timestamp, notification))

            pend_notif = data.get('pending', [])
            pend_id = data.get('pending_id', [])
            for i in range(len(pend_notif)):
                notification = Notification.from_dict(pend_notif[i])
                cls._pending[pend_id[i]] = notification

            cls._accepted = [Notification.from_dict(notification_data)
                            for notification_data in data.get('accepted', [])]

        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Не удалось загрузить уведомления: {e}")

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


    # Уведомить администраторов о непрочитанных уведомлениях
    @classmethod
    async def notify_pending_to_admins(cls, context: CallbackContext):
        if not cls._pending:
            return

        messages = []
        current_time = time()

        for notification in cls._pending.values():
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
            messages.append(
                f"Пользователь {user_name} не прочитал уведомление (отправлено {delta_str} назад)"
            )

        if messages:
            for user in UserManager.users.values():
                if getattr(user, 'isAdmin', False):
                    await context.bot.send_message(
                        chat_id=user.chatID,
                        text="\n".join(messages)
                    )


    # Сменить статус уведомления на "прочитанное"
    @classmethod
    def set_notification_seen(cls, message_id: int):
        if message_id in cls._pending:
            cls._accepted.append(cls._pending.pop(message_id))
            cls.save()