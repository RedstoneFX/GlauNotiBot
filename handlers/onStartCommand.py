from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler


class onStartCommandHandler(CommandHandler):
    def __init__(self):
        CommandHandler.__init__(self, "start", self.onStart)

    @staticmethod
    async def onStart(update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [InlineKeyboardButton("Создать единоразовое уведомление", callback_data='make_single')],
            [InlineKeyboardButton("Создать интервальное уведомление", callback_data='make_interval')],
            [InlineKeyboardButton("Просмотреть подключенные уведомления", callback_data='list')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text('Здравствуй, пользователь! Я - бот, управляющий доставкой уведомлений о '
                                        'приеме лекарств и посещений врача. Вы можете установить напоминания '
                                        'самостоятельно, либо при помощи специалиста, который определит все параметры '
                                        'приема за вас. Буду рад помочь сохранить ваше здоровье!', reply_markup=reply_markup)
