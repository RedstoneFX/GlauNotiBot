from telegram import Chat


class User:
    def __init__(self, chatID: int, username: str):
        self.name = username
        self.chatID = chatID
        self.isAdmin = False


class UserManager:
    users = dict()

    @staticmethod
    def getUserFromChat(chat: Chat):
        if chat.id not in UserManager.users:
            UserManager.users[chat.id] = User(chat.id, chat.username)
        return UserManager.users[chat.id]
