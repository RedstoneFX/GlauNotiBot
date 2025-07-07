from time import time
from scheduler import Scheduler

sched = Scheduler(1)

sched.addTask(round(time()) + 5, lambda expireTime: print(expireTime))
sched.addTask(round(time()) + 5, lambda expireTime: print(expireTime))
sched.addTask(round(time()) + 5, lambda expireTime: print(expireTime))

sched.setAutorunEnabled(True)
