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
        return self.replicas.get(name, None)

    def has(self, name: str):
        return name in self.replicas

    def listWithCertainExtra(self, extra_name: str) -> list[Replica]:
        result = []
        for replica in self.replicas.values():
            if extra_name in replica.extra:
                result.append(replica)
        return result

    def getUniqueExtraValues(self, extra_name: str) -> set[str]:
        values = set()
        for replica in self.replicas.values():
            value = replica.extra.get(extra_name, None)
            if value and value not in values:
                values.add(value)
        return values


    def getAllWithExtraValue(self, extra_name: str, extra_value: str):
        replicas = []
        for replica in self.replicas.values():
            value = replica.extra.get(extra_name, None)
            if value and value == extra_value:
                replicas.append(replica)
        return replicas



class LangManager:
    langs: dict[str, LangDictionary] = dict()

    @classmethod
    def loadLang(cls, langName: str, langDir):
        cls.langs[langName] = LangDictionary(langDir)

    @classmethod
    def get(cls, name:str, lang:str):
        if lang not in cls.langs:
            return None  # "[Ошибка: запрошенный язык {lang} не определен]" TODO: исправить несоответствие типов
        else:
            return cls.langs[lang].get(name)
