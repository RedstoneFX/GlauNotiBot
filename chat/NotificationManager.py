from queue import PriorityQueue
from time import time
import json

from telegram import Bot
from telegram.ext import CallbackContext
from chat.UserManager import UserManager
from misc.buttons import notificationReadMarkup
from misc.convert_delta_to_str import convert_delta_to_str


class PendingNotification:
    def __init__(self, timestamp: float, parent_notification_id: int, admin_messages=None, msg_id: int=0):
        self.timestamp = timestamp
        self.parent_notification_id = parent_notification_id
        self.admin_messages = admin_messages or []
        self.msg_id = msg_id

    def addAdminMsg(self, admin_msg_id):
        self.admin_messages.append(admin_msg_id)

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "parent_parent_notification_id": self.parent_notification_id,
            "admin_messages": self.admin_messages,
            "msg_id": self.msg_id
        }

    @staticmethod
    def from_dict(raw):
        return PendingNotification(
            timestamp=raw["timestamp"],
            parent_notification_id=raw["parent_parent_notification_id"],
            admin_messages=raw["admin_messages"],
            msg_id=raw["msg_id"]
        )

    def __lt__(self, other):
        if self.timestamp < other.timestamp:
            return True
        elif self.timestamp == other.timestamp and self.parent_notification_id < other.parent_notification_id:
            return True
        elif self.timestamp == other.timestamp and self.parent_notification_id == other.parent_notification_id and self.msg_id < other.msg_id:
            return True
        else:
            return False


class Notification:
    def __init__(self, id: int, chat_id: int, message: str, interval: float):
        self.id = id
        self.chat_id = chat_id
        self.message = message
        self.interval = interval

    def __lt__(self, other):
        return self.id < other.id

    def to_dict(self) -> dict:
        notif_dict = dict()
        notif_dict["id"] = self.id
        notif_dict["chat_id"] = self.chat_id
        notif_dict["message"] = self.message
        notif_dict["interval"] = self.interval
        return notif_dict

    @classmethod
    def from_dict(cls, data: dict) -> 'Notification':
        return cls(
            id=data["id"],
            chat_id=data["chat_id"],
            message=data["message"],
            interval=data["interval"]
        )

    def make_pending(self, timestamp: float):
        return PendingNotification(timestamp, self.id)


class NotificationManager:
    filename = None
    _queue = PriorityQueue()
    sent_not_read: list[PendingNotification] = []
    _notification_by_id: dict[int, Notification] = {}
    _last_created_notification_id = 0


    # Сохранить все уведомления в файл
    @classmethod
    def save(cls):
        if cls.filename is None:
            return

        data = {
            'queue': [notif_ref.to_dict() for notif_ref in cls._queue.queue],
            'sent_not_read': [notif_ref.to_dict() for notif_ref in cls.sent_not_read],
            'notifications': [notification.to_dict() for notification in cls._notification_by_id.values()],
            'last_created_notification_id': cls._last_created_notification_id
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

            cls._last_created_notification_id = data.get('last_created_notification_id', 0)

            for notif_ref_dict in data.get('queue', []):
                notif_ref = PendingNotification.from_dict(notif_ref_dict)
                cls._queue.put(notif_ref)

            for notif_ref_dict in data.get('sent_not_read', []):
                notif_ref = PendingNotification.from_dict(notif_ref_dict)
                cls.sent_not_read.append(notif_ref)

            for notification_dict in data.get('notifications', []):
                notification = Notification.from_dict(notification_dict)
                cls._notification_by_id[notification.id] = notification

        except FileNotFoundError:
            pass

    # Создать новое уведомление
    @classmethod
    def add_notification(cls, first_timestamp: float, chat_id: int, msg: str, interval: float) -> int:
        cls._last_created_notification_id += 1
        notification = Notification(cls._last_created_notification_id, chat_id, msg, interval)
        cls._notification_by_id[cls._last_created_notification_id] = notification
        cls._queue.put(notification.make_pending(first_timestamp))
        cls.save()
        return cls._last_created_notification_id

    # Отправить уведомления по времени
    @classmethod
    async def send_expired_notifications(cls, context: CallbackContext):
        flag_sent_at_least_one = False
        # пытаться отправить уведомление, пока в очереди есть уведомления с просроченной датой...
        while not cls._queue.empty() and cls._queue.queue[0].timestamp <= time():
            # Извлекаем верхнее уведомление, дата которого просрочена
            notification_ref: PendingNotification = cls._queue.get()
            notification = cls._notification_by_id[notification_ref.parent_notification_id]
            # Отправляем уведомление клиенту
            msg = await context.bot.send_message(
                chat_id=notification.chat_id,
                text=notification.message,
                reply_markup=notificationReadMarkup
            )
            notification_ref.msg_id = msg.id
            # Отмечаем это уведомление как отправленное, но непрочитанное
            cls.sent_not_read.append(notification_ref)
            await cls.announce_new_pending_to_admins(notification_ref, context.bot)
            # Добавляем уведомление в очередь, если оно повторяющееся
            if notification.interval > 0:
                new_notification_ref = PendingNotification(
                    notification_ref.timestamp + notification.interval, notification.id
                )
                cls._queue.put(new_notification_ref)
            flag_sent_at_least_one = True
        # Сохраняем уведомления, если отправили хотя бы одно
        if flag_sent_at_least_one:
            cls.save()


    @classmethod
    async def announce_new_pending_to_admins(cls, pending: PendingNotification, bot: Bot):
        if len(pending.admin_messages) != 0:
            raise Exception("Анонс уже был сделан ранее, так как для этого уведомления уже определены сообщения у админов")
        flag_sent_at_least_one = False
        notification = cls._notification_by_id[pending.parent_notification_id]
        for user in UserManager.users.values():
            if user.isAdmin:
                admin_msg = await bot.send_message(user.chatID, f"✴️ Уведомление отправлено пользователю @{user.name} менее 15 минут назад!\nСодержание: \"{notification.message}\"")
                pending.admin_messages.append((admin_msg.chat_id, admin_msg.id))
                flag_sent_at_least_one = True
        if flag_sent_at_least_one:
            cls.save()


    # Уведомить администраторов о непрочитанных уведомлениях
    @classmethod
    async def notify_pending_to_admins(cls, context: CallbackContext):
        if not cls.sent_not_read:
            return

        # попытаться обновить каждое непрочитанное сообщение
        for notif_ref in cls.sent_not_read:
            delta = time() - notif_ref.timestamp
            if delta > 1800:

                notification = cls._notification_by_id[notif_ref.parent_notification_id]
                user = UserManager.users[notification.chat_id]
                user_name = getattr(user, 'name', 'Unknown')

                for admin_chat_id, admin_msg_id in notif_ref.admin_messages:
                    await context.bot.edit_message_text(
                        f"🅾️Пользователь @{user_name} не прочитал уведомление, отправленное {convert_delta_to_str(delta)} назад.\nСодержание: \"{notification.message}\"",
                        admin_chat_id, admin_msg_id)


    # Сменить статус уведомления на "прочитанное"
    @classmethod
    async def notify_notification_seen(cls, chat_id:int, msg_id: int, bot: Bot):
        for i in range(len(cls.sent_not_read)):
            notif_ref = cls.sent_not_read[i]
            notification = cls._notification_by_id[notif_ref.parent_notification_id]
            if notif_ref.msg_id == msg_id and notification.chat_id == chat_id:
                for admin_chat_id, admin_msg_id in notif_ref.admin_messages:
                    delta = time() - notif_ref.timestamp
                    user = UserManager.users.get(notification.chat_id)
                    user_name = getattr(user, 'name', 'Unknown')
                    await bot.edit_message_text(
                        f"✅Пользователь @{user_name} подтвердил уведомление спустя {convert_delta_to_str(delta)} после его отправки.\nСодержание: \"{notification.message}\"",
                        admin_chat_id, admin_msg_id)
                cls.sent_not_read.pop(i)
                break

    @classmethod
    def get_notifications_for_chat(cls, chat_id):
        result = []  # TODO: кеширование и хранение карты для chat_id и его уведомлений
        for notification in cls._notification_by_id.values():
            if notification.chat_id == chat_id:
                result.append(notification)
        return result

    @classmethod
    def get_next_time(cls, notification_id: int):
        for notif_ptr in cls._queue.queue:
            if notif_ptr.parent_notification_id == notification_id:
                return notif_ptr.timestamp
        return 0

    @classmethod
    def get(cls, notification_id: int):
        return cls._notification_by_id.get(notification_id, None)

    @classmethod
    def get_time_before_next(cls, notification_id: int):
        return cls.get_next_time(notification_id) - time()

    @classmethod
    def remove(cls, notification_id):
        if notification_id not in cls._notification_by_id:
            return
        cls._notification_by_id.pop(notification_id)

        new_queue = PriorityQueue()
        while not cls._queue.empty():
            notif_ref: PendingNotification = cls._queue.get()
            if notif_ref.parent_notification_id != notification_id:
                new_queue.put(notif_ref)
        cls._queue = new_queue