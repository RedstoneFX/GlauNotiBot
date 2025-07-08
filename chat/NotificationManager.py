from queue import PriorityQueue
from time import time
from datetime import timedelta

from telegram import Bot

import asyncio

from telegram.ext import CallbackContext

from chat.UserManager import UserManager


class NotificationManager:
    filename = None
    queue = PriorityQueue()
    pending = []
    lastIndex = 0

    @staticmethod
    def save():
        pass

    @staticmethod
    def load():
        pass

    @staticmethod
    def setBot(bot):
        NotificationManager.bot = bot

    @staticmethod
    def addNotification(timestamp: float, chatID: int, msg: str, interval: float):
        NotificationManager.queue.put([timestamp, NotificationManager.lastIndex, chatID, msg, interval])

    @staticmethod
    async def sendExpiredNotifications(context: CallbackContext):
        while not NotificationManager.queue.empty() and NotificationManager.queue.queue[0][0] <= time():
            item = NotificationManager.queue.get()
            await context.bot.send_message(item[2], item[3])
            NotificationManager.pending.append(item.copy())
            item[0] += item[4]
            NotificationManager.queue.put(item)

    @staticmethod
    async def notifyAdmins(context: CallbackContext):
        for user in UserManager.users.values():
            hugeMsg = ""
            if user.isAdmin:
                for pending in NotificationManager.pending:
                    delta = round(time() - pending[0])
                    seconds = delta % 60
                    minutes = delta // 60 % 60
                    hours = delta // 360 % 24
                    days = delta // 360 // 24

                    if days != 0:
                        deltamsg = f"{days} дней и {hours} часов"
                    elif hours != 0:
                        deltamsg = f"{hours} часов и {minutes} минут"
                    elif minutes != 0:
                        deltamsg = f"{minutes} минут и {seconds} секунд"
                    elif seconds != 0:
                        deltamsg = f"{seconds} секунд"
                    else:
                        deltamsg = "меньше секунды"

                    hugeMsg += "Пользователю " + UserManager.users[pending[2]].name + \
                               " было отправлено уведомление, но оно непрочитано уже " + deltamsg + "\n"
                if not hugeMsg.isspace():
                    await context.bot.send_message(user.chatID, hugeMsg.strip())




