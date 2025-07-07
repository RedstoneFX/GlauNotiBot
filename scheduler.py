from queue import PriorityQueue
from time import time
from typing import Callable


class Scheduler:
    def __init__(self):
        self.__queue = PriorityQueue()

    def addTask(self, runTime: int, handler: Callable, args=tuple()):
        self.__queue.put((runTime, handler, args))

    def runExpired(self):
        now = round(time())
        while not self.__queue.empty() and self.__queue.queue[0][0] <= now:
            item = self.__queue.get()
            item[1](*item[2], expireTime=item[0])
