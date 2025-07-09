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
    [InlineKeyboardButton("Узнать информацию", callback_data='get_info')]
]

userKeyboardLearnInfo = [
    [InlineKeyboardButton("Что такое глаукома?", callback_data='show_info_1')],
    [InlineKeyboardButton("Какие компоненты зрения страдают при глаукоме?", callback_data='show_info_2')],
    [InlineKeyboardButton("Как проявляется ГЛАУКОМА? Каковы симптомы заболевания?", callback_data='show_info_3')],
    [InlineKeyboardButton("Можно ли предотвратить глаукому?", callback_data='show_info_4')],
    [InlineKeyboardButton("У меня не диагностирована глаукома, НО...", callback_data='show_info_5')],
    [InlineKeyboardButton("Что я могу сделать, чтобы успешно бороться с ГЛАУКОМОЙ?", callback_data='show_info_6')],
    [InlineKeyboardButton("С лечением всё понятно. Как быть в обычной жизни?", callback_data='show_info_7')],
    [InlineKeyboardButton("Могу ли я самостоятельно обнаружить у себя ГЛАУКОМУ?", callback_data='show_info_8')]
]

userKeyboardLearnWhatIs = [
    [InlineKeyboardButton("Почему повышается внутриглазное давление (ВГД)?", callback_data='show_info_1_1')],
    [InlineKeyboardButton("Какое внутриглазное давление считается нормальным?", callback_data='show_info_1_2')],
    [InlineKeyboardButton("Какие последствия этого заболевания могут меня ждать?", callback_data='show_info_1_3')],
    [InlineKeyboardButton("Если у меня выявлена ГЛАУКОМА на одном глазу, разовьётся ли заболевание на другом глазу?", callback_data='show_info_1_4')]
]

userKeyboardLearnComponents = [
    [InlineKeyboardButton("Что такое поле зрения?", callback_data='show_info_2_1')],
    [InlineKeyboardButton("Если у меня глаукома, я ослепну?", callback_data='show_info_2_2')],
    [InlineKeyboardButton("Как быстро можно ослепнуть при глаукоме?", callback_data='show_info_2_3')]
]

userKeyboardLearnNoDiagnoseBut = [
    [InlineKeyboardButton("Если я хорошо вижу, значит у меня нет глаукомы?", callback_data='show_info_5_1')],
    [InlineKeyboardButton("Если мои родители болели глаукомой, у меня она тоже появится?", callback_data='show_info_5_2')],
    [InlineKeyboardButton("У меня в семье есть больные ГЛАУКОМОЙ! Я обязательно заболею?", callback_data='show_info_5_3')],
    [InlineKeyboardButton("Какие факторы риска увеличивают вероятность заболевания ГЛАУКОМОЙ?", callback_data='show_info_5_4')]
]

userKeyboardLearnWhatToDo = [
    [InlineKeyboardButton("Какое лечение назначит мне врач при ГЛАУКОМЕ?", callback_data='show_info_6_1')],
    [InlineKeyboardButton("Существует ли эффективное лекарство для лечения глаукомы?", callback_data='show_info_6_2')],
    [InlineKeyboardButton("Какие физические нагрузки полезны при глаукоме?", callback_data='show_info_6_3')],
    [InlineKeyboardButton("Нужно ли мне заниматься физкультурой? Какие нагрузки Вы рекомендуете?", callback_data='show_info_6_4')],
    [InlineKeyboardButton("В каком положении спать при глаукоме?", callback_data='show_info_6_5')],
    [InlineKeyboardButton("Нужно ли мне придерживаться диеты при ГЛАУКОМЕ?", callback_data='show_info_6_6')],
    [InlineKeyboardButton("Какой режим труда и отдыха Вы рекомендуете?", callback_data='show_info_6_7')]
]

userKeyboardLearnHowToCure = [
    [InlineKeyboardButton("Нужно ли делать перерывы в лечении глазными каплями или их надо закапывать постоянно?", callback_data='show_info_6_1_1')],
    [InlineKeyboardButton("Если врач назначил два вида глазных капель, как правильно их закапывать?", callback_data='show_info_6_1_2')],
    [InlineKeyboardButton("Что делать, если капли не понижают внутриглазное давление?", callback_data='show_info_6_1_3')],
    [InlineKeyboardButton("Что делать, если я забыл вовремя закапать глазные капли?", callback_data='show_info_6_1_4')],
    [InlineKeyboardButton("Улучшится ли мое зрение после операции? Нужно ли закапывать капли?", callback_data='show_info_6_1_5')],
    [InlineKeyboardButton("Бывают ли побочные эффекты при закапывании глазных капель?", callback_data='show_info_6_1_6')],
    [InlineKeyboardButton("Можно ли мне закапывать глазные капли, если у меня есть другие хронические заболевания?", callback_data='show_info_6_1_7')],
    [InlineKeyboardButton("Как правильно закапывать глазные капли?", callback_data='show_info_6_1_8')],
    [InlineKeyboardButton("Где и как хранить глазные капли?", callback_data='show_info_6_1_9')]
]

userKeyboardLearnRegularLife = [
    [InlineKeyboardButton("Могу ли я продолжать работать на компьютере?", callback_data='show_info_7_1')],
    [InlineKeyboardButton("Можно ли водить машину при глаукоме?", callback_data='show_info_7_2')],
    [InlineKeyboardButton("Можно ли носить контактные линзы при глаукоме?", callback_data='show_info_7_3')],
    [InlineKeyboardButton("Можно ли при глаукоме пить много воды?", callback_data='show_info_7_4')],
    [InlineKeyboardButton("Что нельзя делать при глаукоме?", callback_data='show_info_7_5')],
    [InlineKeyboardButton("Какой вес можно поднимать при глаукоме?", callback_data='show_info_7_6')]
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
