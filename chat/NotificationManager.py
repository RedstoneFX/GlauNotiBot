from queue import PriorityQueue
from time import time

from telegram import Bot

import asyncio

from telegram.ext import CallbackContext


class NotificationManager:
    filename = None
    queue = PriorityQueue()
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
            item[0] += item[4]
            NotificationManager.queue.put(item)
