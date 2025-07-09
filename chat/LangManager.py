from os import listdir
import json

class Replica:
    def __init__(self, name: str, isForAdminOnly: bool, body: str):
        self.name = name
        self.isForAdmin = isForAdminOnly
        self.body = body

    @staticmethod
    def fromDict(dictionary: dict):
        return Replica(dictionary["name"], dictionary["isForAdminOnly"], dictionary["body"])


class LangDictionary:
    def __init__(self, langDir: str):
        self.replicas = dict()
        for file in listdir(langDir):
            with open(file, encoding="utf-8", mode="r") as f:
                rawDict = json.load(f)
                replica = Replica.fromDict(rawDict)
                self.replicas[replica.name] = replica

    def get(self, name: str):
        self.replicas.get(name, "[Ошибка: не удалось найти реплику]")

    def has(self, name: str):
        return name in self.replicas


class LangManager:
    langs = dict()

    @classmethod
    def loadLang(cls, langName: str, langDir):
        cls.langs[langName] = LangDictionary(langDir)

    @classmethod
    def get(cls, name:str, lang:str):
        if lang not in cls.langs:
            return "[Ошибка: запрошенный язык {lang} не определен]"
        elif not cls.langs[lang].has(name):
            return f"[Ошибка: запрошенный язык {lang} не содержит реплику {name}"
        else:
            return cls.langs[lang].get(name)