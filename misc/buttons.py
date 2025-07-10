from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from chat.LangManager import LangManager

adminKeyboard = [
    [InlineKeyboardButton("Добавить напоминание (отладка)", callback_data='add_notification')],
    [InlineKeyboardButton("Список напоминаний (отладка)", callback_data='list_notifications')],
    [InlineKeyboardButton("Получить список клиентов", callback_data='get_users')],
    [InlineKeyboardButton("Узнать информацию", callback_data='ask_buttons')]
    ]

userKeyboard = [
    [InlineKeyboardButton("Добавить напоминание", callback_data='add_notification')],
    [InlineKeyboardButton("Список напоминаний", callback_data='list_notifications')],
    [InlineKeyboardButton("Узнать информацию", callback_data='ask_buttons')]
    ]

intervalButtons = [
    [
        InlineKeyboardButton("+7 дней", callback_data="+7days"),
        InlineKeyboardButton("+6 часов", callback_data="+6hours"),
        InlineKeyboardButton("+30 минут", callback_data="+30mins")
    ],
    [
        InlineKeyboardButton("+1 день", callback_data="+day"),
        InlineKeyboardButton("+1 час", callback_data="+hour"),
        InlineKeyboardButton("+10 минут", callback_data="+10mins")
    ],
    [
        InlineKeyboardButton("-1 день", callback_data="-day"),
        InlineKeyboardButton("-1 час", callback_data="-hour"),
        InlineKeyboardButton("-10 минут", callback_data="-10mins")
    ],
    [
        InlineKeyboardButton("-7 дней", callback_data="-7days"),
        InlineKeyboardButton("-6 часов", callback_data="-6hours"),
        InlineKeyboardButton("-30 минут", callback_data="-30mins")
    ],
    [
        InlineKeyboardButton("Подтвердить", callback_data="submit")
    ],
    [
        InlineKeyboardButton("Прислать только один раз", callback_data="once")
    ]
]

daytimeButtons = [
    [
        InlineKeyboardButton("+6 часов", callback_data="+6hours"),
        InlineKeyboardButton("+30 минут", callback_data="+30mins"),
        InlineKeyboardButton("+5 минут", callback_data="+5mins")
    ],
    [
        InlineKeyboardButton("+1 час", callback_data="+hour"),
        InlineKeyboardButton("+10 минут", callback_data="+10mins"),
        InlineKeyboardButton("+1 минута", callback_data="+min")
    ],
    [
        InlineKeyboardButton("-1 час", callback_data="-hour"),
        InlineKeyboardButton("-10 минут", callback_data="-10mins"),
        InlineKeyboardButton("-1 минута", callback_data="-min")
    ],
    [
        InlineKeyboardButton("-6 часов", callback_data="-6hours"),
        InlineKeyboardButton("-30 минут", callback_data="-30mins"),
        InlineKeyboardButton("-5 минут", callback_data="-5mins")
    ],
    [
        InlineKeyboardButton("Подтвердить", callback_data="submit"),
    ]
]

notificationRead = [
    [InlineKeyboardButton("Принято", callback_data="accepted")]
]

userKeyboardMarkup = InlineKeyboardMarkup(userKeyboard)
adminKeyboardMarkup = InlineKeyboardMarkup(adminKeyboard)
notificationReadMarkup = InlineKeyboardMarkup(notificationRead)
daytimeButtonsMarkup = InlineKeyboardMarkup(daytimeButtons)
intervalButtonsMarkup = InlineKeyboardMarkup(intervalButtons)
