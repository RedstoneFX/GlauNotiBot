import datetime, calendar
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

months = ["0", "Январь", "Февраль", "Март",
          "Апрель", "Май", "Июнь", "Июль",
          "Август", "Сентябрь", "Октябрь",
          "Ноябрь", "Декарь"]


def generateMonthButtons(year, month):
    weekDay, days = calendar.monthrange(year, month)
    buttons = [
        [
            InlineKeyboardButton("<-", callback_data="month_left"),
            InlineKeyboardButton(months[month], callback_data="-"),
            InlineKeyboardButton("->", callback_data="month_right")],
        [], [], [], [], []
    ]
    for i in range(weekDay):
        buttons[1].append(InlineKeyboardButton("-", callback_data="-"))
    for dayIndex in range(0, days):
        humanIndex = str(dayIndex + 1)
        lineIndex = (weekDay + dayIndex) // 7 + 1
        buttons[lineIndex].append((InlineKeyboardButton(humanIndex, callback_data=humanIndex)))
    if len(buttons[-1]) == 0:
        buttons.pop()
    while len(buttons[-1]) < 7:
        buttons[-1].append(InlineKeyboardButton("-", callback_data="-"))
    buttons.append([InlineKeyboardButton("Подтвердить", callback_data="submit")])
    return InlineKeyboardMarkup(buttons)
