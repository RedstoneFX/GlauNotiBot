from telegram import InlineKeyboardButton, InlineKeyboardMarkup

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
        InlineKeyboardButton("Подтвердить", callback_data="submit"),
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

daytimeButtonsMarkup = InlineKeyboardMarkup(daytimeButtons)
intervalButtonsMarkup = InlineKeyboardMarkup(intervalButtons)
