from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from chat.LangManager import LangManager

def generate_groups_buttons_markup(lang: str):
    lang = LangManager.langs[lang]
    groups = lang.getUniqueExtraValues("group")
    buttons = []
    for group in groups:
        replica = lang.get(group)
        if replica:
            name = replica.body
        else:
            name = group
        buttons.append([InlineKeyboardButton(name, callback_data="ask_group.by_name." + group)])
    buttons.append([InlineKeyboardButton("Покажи все вопросы", callback_data="ask_group.list_all")])
    return InlineKeyboardMarkup(buttons)

def generate_group_buttons_markup(group_name: str, lang: str, debug_all: bool=False):
    lang = LangManager.langs[lang]
    buttons = []
    for replica in lang.replicas.values():
        if "group" in replica.extra and "title" in replica.extra:  # TODO: надо бы переименовать group в ask_group, чтобы избежать путаницы - этот тег только у вопросов должен быть
            if replica.extra["group"] == group_name or debug_all:
                buttons.append([InlineKeyboardButton(replica.extra["title"], callback_data="ask." + replica.name)])
    buttons.append([InlineKeyboardButton("<- Назад", callback_data="ask_buttons")])
    return InlineKeyboardMarkup(buttons)
