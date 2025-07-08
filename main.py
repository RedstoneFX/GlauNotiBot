import logging
from telegram.ext import ApplicationBuilder

from chat.UserManager import UserManager
from handlers.onButtonClicked import onButtonClickedHandler
from handlers.onMessageReceived import onMessageReceivedHandler
from handlers.onStartCommand import onStartCommandHandler

with open("token.txt", mode="r", encoding="utf-8") as f:
    TOKEN = f.read()

logging.basicConfig(format='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s', level=logging.INFO)


if __name__ == '__main__':
    UserManager.load("users.json")
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(onStartCommandHandler())
    application.add_handler(onButtonClickedHandler())
    application.add_handler(onMessageReceivedHandler())
    application.run_polling()
