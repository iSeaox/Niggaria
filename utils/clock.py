import time


def sleep(duration, get_now=time.perf_counter):
    now = get_now()
    end = now + duration
    while now < end:
        now = get_now()


def get_time(ns=True):
    return time.time_ns() if ns else time.time_ns() / 1_000_000_000


class Clock:
    def __init__(self, frequency):
        self.frequency = frequency

        self.start_time = get_time(False)

    def start_tick(self):
        self.start_time = get_time(False)

    def tick(self):
        elapsed = get_time(False) - self.start_time
        waiting_time = (1 / self.frequency) - elapsed
        if waiting_time > 0:
            sleep(waiting_time)
