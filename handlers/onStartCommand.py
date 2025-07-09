from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler

from chat.UserManager import UserManager

adminKeyboard = [
    # [InlineKeyboardButton("Назначить уведомления", callback_data='not_avaliable')],
    [InlineKeyboardButton("Получить список всех уведомлений", callback_data='get_notifications')],
    [InlineKeyboardButton("Получить список клиентов", callback_data='get_users')],
    [InlineKeyboardButton("Узнать информацию", callback_data='get_notifications')]
]

userKeyboard = [
    [InlineKeyboardButton("Добавить напоминание", callback_data='add_notification')],
    [InlineKeyboardButton("Узнать информацию", callback_data='get_notifications')]
]

class onStartCommandHandler(CommandHandler):
    def __init__(self):
        CommandHandler.__init__(self, "start", self.onStart)

    @staticmethod
    async def onStart(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if UserManager.getUser(update.effective_chat).isAdmin:
            reply_markup = InlineKeyboardMarkup(adminKeyboard)
        else:
            reply_markup = InlineKeyboardMarkup(userKeyboard)
        await update.message.reply_text("Здравствуйте, пользователь! Что вы желаете сделать?", reply_markup=reply_markup)
