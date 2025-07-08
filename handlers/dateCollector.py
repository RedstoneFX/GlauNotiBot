from calendar import calendar
from datetime import datetime
from telegram import Chat, InlineKeyboardButton, InlineKeyboardMarkup

from chat.UserManager import User

months = ["0", "Январь", "Февраль", "Март",
          "Апрель", "Май", "Июнь", "Июль",
          "Август", "Сентябрь", "Октябрь",
          "Ноябрь", "Декарь"]


class DateCollector:
    @staticmethod
    async def askYear(chat: Chat, user: User):
        currentYear = datetime.datetime.now().year
        nearYears = [[InlineKeyboardButton(str(currentYear), callback_data=str(currentYear))],
                     [InlineKeyboardButton(str(currentYear + 1), callback_data=str(currentYear + 1))]]
        await chat.send_message("Теперь нужно указать дату начала отправки уведомлений. В каком году начать?",
                                reply_markup=InlineKeyboardMarkup(nearYears))

    @staticmethod
    async def askMonth(chat: Chat, user: User):
        currentDate = datetime.datetime.now()
        nearMonths = []
        minMonth = 1 if currentDate.year != user.extra["year"] else currentDate.month
        for i in range(minMonth, 13):
            nearMonths.append([InlineKeyboardButton(f"{months[i]} {user.extra['year']} года", callback_data=str(i))])
        await chat.send_message("Теперь нужно указать дату начала отправки уведомлений. В каком году начать?",
                                reply_markup=InlineKeyboardMarkup(nearMonths))

    @staticmethod
    async def askDay(chat: Chat, user: User):
        currentDate = datetime.datetime.now()
        nearDays = []
        minDay = 1 if currentDate.year != user.extra["year"] or currentDate.month != user.extra[
            "month"] else currentDate.day
        for i in range(minDay, calendar.monthrange(user.extra["year"], user.extra["month"])[1]):
            nearDays.append([InlineKeyboardButton(f"{i} {months[user.extra['month']]} {user.extra['year']} года",
                                                  callback_data=str(i))])
        await chat.send_message("Какое число?",
                                reply_markup=InlineKeyboardMarkup(nearDays))
