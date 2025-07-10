from os import listdir
import json

class Replica:
    def __init__(self, name: str, body: str, extra:dict):
        self.name = name
        self.body = body
        self.extra = extra or dict()

    @staticmethod
    def fromDict(dictionary: dict, name: str):
        return Replica(name, dictionary["body"], dictionary.get("extra", dict()))

    def getExtra(self, name):
        self.extra.get(name, None)


class LangDictionary:
    def __init__(self, langDir: str):
        self.replicas: dict[str, Replica] = dict()
        for file in listdir(langDir):
            name = file[:-5]
            with open(langDir + file, encoding="utf-8", mode="r") as f:
                self.replicas[name] = Replica.fromDict(json.load(f), name)

    def get(self, name: str):
        return self.replicas.get(name, "[Ошибка: не удалось найти реплику]")

    def has(self, name: str):
        return name in self.replicas

    def listWithCertainExtra(self, extra_name) -> list[Replica]:
        result = []
        for replica in self.replicas.values():
            if extra_name in replica.extra:
                result.append(replica)
        return result


class LangManager:
    langs: dict[str, LangDictionary] = dict()

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