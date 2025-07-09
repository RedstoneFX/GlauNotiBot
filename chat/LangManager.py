from os import listdir
import json

class Replica:
    def __init__(self, body: str, extra:dict):
        self.body = body
        self.extra = extra or dict()

    @staticmethod
    def fromDict(dictionary: dict):
        return Replica(dictionary["body"], dictionary.get("extra", dict()))

    def getExtra(self, name):
        self.extra.get(name, None)


class LangDictionary:
    def __init__(self, langDir: str):
        self.replicas = dict()
        for file in listdir(langDir):
            with open(langDir + file, encoding="utf-8", mode="r") as f:
                self.replicas[file[:-5]] = Replica.fromDict(json.load(f))

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