import logging
from telegram.ext import ApplicationBuilder

from chat.NotificationManager import NotificationManager
from chat.UserManager import UserManager
from handlers.onButtonClicked import onButtonClickedHandler
from handlers.onMessageReceived import onMessageReceivedHandler
from handlers.onStartCommand import onStartCommandHandler

with open("token.txt", mode="r", encoding="utf-8") as f:
    TOKEN = f.read()

logging.basicConfig(format='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s', level=logging.INFO)


if __name__ == '__main__':
    UserManager.filename = "users.json"
    UserManager.load()
    application = ApplicationBuilder().token(TOKEN).build()
    application.job_queue.run_repeating(NotificationManager.sendExpiredNotifications, 5)
    application.job_queue.run_repeating(NotificationManager.notifyPendingToAdmins, 5)
    application.job_queue.run_repeating(NotificationManager.notifyAcceptedToAdmins, 5)
    application.add_handler(onStartCommandHandler())
    application.add_handler(onButtonClickedHandler())
    application.add_handler(onMessageReceivedHandler())
    application.run_polling()
