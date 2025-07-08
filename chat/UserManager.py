from telegram import Chat
import json

import atexit


class User:
    def __init__(self, chatID: int, username: str, isAdmin=False, state="idle", extra=dict()):
        self.name = username
        self.chatID = chatID
        self.isAdmin = isAdmin
        self.state = state
        self.extra = extra

    def toDict(self):
        o = dict()
        o["name"] = self.name
        o["chatID"] = self.chatID
        o["isAdmin"] = self.isAdmin
        o["state"] = self.state
        o["extra"] = self.extra
        return o


class UserManager:
    filename = None
    users = dict()

    @staticmethod
    def getUser(chat: Chat) -> User:
        if chat.id not in UserManager.users:
            UserManager.load()
            UserManager.users[chat.id] = User(chat.id, chat.username)
            UserManager.save()
        return UserManager.users[chat.id]

    @staticmethod
    def save():
        if UserManager.filename is None:
            return
        with open(UserManager.filename, mode="w", encoding="utf-8") as f:
            data = list(map(User.toDict, UserManager.users.values()))
            f.write(json.dumps(data, indent=4, ensure_ascii=False))

    @staticmethod
    def load():
        try:
            with open(UserManager.filename, mode="r", encoding="utf-8") as f:
                data = json.load(f)
                for user in data:
                    UserManager.users[user["chatID"]] = User(user["chatID"], user["name"], user["isAdmin"],
                                                             user["state"], user["extra"])
        except FileNotFoundError:
            pass


atexit.register(UserManager.save)
