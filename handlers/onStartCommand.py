from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler

from chat.UserManager import UserManager


class onStartCommandHandler(CommandHandler):
    def __init__(self):
        CommandHandler.__init__(self, "start", self.onStart)

    @staticmethod
    async def onStart(update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [InlineKeyboardButton("Получить список пользователей", callback_data='get_users')],
            [InlineKeyboardButton("Получить список всех уведомлений", callback_data='get_notifications')]
        ]

        UserManager.getUserFromChat(update.effective_chat)
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text('Отладка:', reply_markup=reply_markup)
