from queue import PriorityQueue
from time import time
from typing import Callable

from CycledThread import CycledThread


class Scheduler:
    def __init__(self, autorunInterval=5):
        self.__queueInserted = 0
        self.__autorunThread = CycledThread(autorunInterval, Scheduler.runExpired, (self,))
        self.__queue = PriorityQueue()

    def addTask(self, runTime: int, handler: Callable, args=tuple()):
        self.__queue.put((runTime, self.__queueInserted, handler, args))
        self.__queueInserted += 1

    def runExpired(self):
        now = round(time())
        while not self.__queue.empty() and self.__queue.queue[0][0] <= now:
            item = self.__queue.get()
            item[2](*item[3], expireTime=item[0])

    def setAutorunEnabled(self, isEnabled):
        if self.__autorunThread.is_alive() and not isEnabled:
            self.__autorunThread.stop()
        elif not self.__autorunThread.is_alive() and isEnabled:
            self.__autorunThread.start()


sched = Scheduler(1)

sched.addTask(round(time()) + 5, lambda expireTime: print(expireTime))
sched.addTask(round(time()) + 5, lambda expireTime: print(expireTime))
sched.addTask(round(time()) + 5, lambda expireTime: print(expireTime))

sched.setAutorunEnabled(True)
