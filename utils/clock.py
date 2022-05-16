import time


class Clock:
    def __init__(self, frequency=None):
        self.frequency = frequency

        self.start_time = self.get_time(False)
        self.time = self.get_time()

    def start_tick(self):
        self.start_time = self.get_time(False)

    def tick(self):
        elapsed = self.get_time(False) - self.start_time
        waiting_time = (1 / self.frequency) - elapsed
        if waiting_time > 0:
            self.__sleep(waiting_time)

    def time_step(self):
        time_step = self.get_time() - self.time
        self.time = self.get_time()

        return time_step

    @staticmethod
    def __sleep(duration, get_now=time.perf_counter):
        now = get_now()
        end = now + duration
        while now < end:
            now = get_now()

    @staticmethod
    def get_time(ns=True):
        return time.time_ns() if ns else time.time_ns() / 1_000_000_000
