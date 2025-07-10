import atexit
import logging
from telegram.ext import ApplicationBuilder, CallbackContext

from chat.NotificationManager import NotificationManager
from chat.UserManager import UserManager
from handlers.onButtonClicked import onButtonClickedHandler
from handlers.onMessageReceived import onMessageReceivedHandler
from handlers.onStartCommand import onStartCommandHandler

with open("token.txt", mode="r", encoding="utf-8") as f:
    TOKEN = f.read()

logging.basicConfig(format='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s', level=logging.INFO)

async def saveNotifications(context: CallbackContext):
    NotificationManager.save()

async def saveUsers(context: CallbackContext):
    NotificationManager.save()

if __name__ == '__main__':
    UserManager.filename = "users.json"
    NotificationManager.filename = "notifs.json"
    UserManager.load()
    NotificationManager.load()
    application = ApplicationBuilder().token(TOKEN).build()
    application.job_queue.run_repeating(NotificationManager.send_expired_notifications, 5)
    application.job_queue.run_repeating(NotificationManager.notify_pending_to_admins, 60)
    application.job_queue.run_repeating(saveUsers, 5*60)
    application.job_queue.run_repeating(saveNotifications, 5*60)
    atexit.register(UserManager.save)
    atexit.register(NotificationManager.save)
    application.add_handler(onStartCommandHandler())
    application.add_handler(onButtonClickedHandler())
    application.add_handler(onMessageReceivedHandler())

    application.run_polling()
