from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler

from chat.UserManager import UserManager
from misc.buttons import userKeyboardMarkup, adminKeyboardMarkup


class onStartCommandHandler(CommandHandler):
    def __init__(self):
        CommandHandler.__init__(self, "start", self.onStart)

    @staticmethod
    async def onStart(update: Update, context: ContextTypes.DEFAULT_TYPE):
        reply_markup = adminKeyboardMarkup if UserManager.getUser(update.effective_chat).isAdmin else userKeyboardMarkup
        await update.message.reply_text("Здравствуйте, пользователь! Что вы желаете сделать?",
                                        reply_markup=reply_markup)
