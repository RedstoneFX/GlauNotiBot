from telegram import Chat
import json

from CycledThread import CycledThread


class User:
    def __init__(self, chatID: int, username: str, isAdmin=False):
        self.name = username
        self.chatID = chatID
        self.isAdmin = isAdmin

    def toDict(self):
        o = dict()
        o["name"] = self.name
        o["chatID"] = self.chatID
        o["isAdmin"] = self.isAdmin
        return o


class UserManager:
    users = dict()

    @staticmethod
    def getUserFromChat(chat: Chat):
        if chat.id not in UserManager.users:
            UserManager.users[chat.id] = User(chat.id, chat.username)
            UserManager.save()
        return UserManager.users[chat.id]

    @staticmethod
    def save():
        with open("users.json", mode="w", encoding="utf-8") as f:
            data = list(map(User.toDict, UserManager.users.values()))
            json.dump(data, f)

    @staticmethod
    def load(filename: str):
        try:
            with open(filename, mode="r", encoding="utf-8") as f:
                data = json.load(f)
                for user in data:
                    UserManager.users[user["chatID"]] = User(user["chatID"], user["name"], user["isAdmin"])
        except FileNotFoundError:
            pass
