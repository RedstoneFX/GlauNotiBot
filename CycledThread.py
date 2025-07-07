from threading import Thread, Event


class CycledThread(Thread):

    def __init__(self, interval: int, target: callable, args=tuple()):
        Thread.__init__(self)
        self.stopEvent = Event()
        self.interval = interval
        self.target = target
        self.args = args

    def run(self):
        while not self.stopEvent.wait(self.interval):
            self.target(*self.args)

    def stop(self):
        self.stopEvent.set()
        Thread.join()

    def start(self):
        self.stopEvent.clear()
        Thread.start(self)
