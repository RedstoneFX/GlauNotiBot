from telegram import Chat
import json

from CycledThread import CycledThread


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
    users = dict()
    filename = "defaultUsers.json"

    @staticmethod
    def getUser(chat: Chat) -> User:
        if chat.id not in UserManager.users:
            UserManager.load(UserManager.filename)
            UserManager.users[chat.id] = User(chat.id, chat.username)
            UserManager.save(UserManager.filename)
        return UserManager.users[chat.id]

    @staticmethod
    def save(filename: str):
        with open(filename, mode="w", encoding="utf-8") as f:
            data = list(map(User.toDict, UserManager.users.values()))
            json.dump(data, f)

    @staticmethod
    def load(filename: str):
        try:
            with open(filename, mode="r", encoding="utf-8") as f:
                data = json.load(f)
                for user in data:
                    UserManager.users[user["chatID"]] = User(user["chatID"], user["name"], user["isAdmin"], user["state"], user["extra"])
        except FileNotFoundError:
            pass
