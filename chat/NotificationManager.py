from telegram import Chat, Bot

from scheduler import Scheduler
import asyncio


class NotificationManager:
    filename = None
    schedule = Scheduler()
    bot: Bot = None

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
        NotificationManager.schedule.addTask(
            timestamp, NotificationManager.runNotification, (timestamp, chatID, msg, interval)
        )

    @staticmethod
    def runNotification(timestamp: float, chatID: int, msg: str, interval: float):
        asyncio.run(NotificationManager.bot.send_message(chatID, msg))
        NotificationManager.addNotification(timestamp + interval, chatID, msg, interval)
