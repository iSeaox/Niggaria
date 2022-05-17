# import time
#
#
# class Clock:
#     def __init__(self, frequency):
#         self.frequency = frequency
#
#     def sleep(self, duration, get_now=time.perf_counter):
#         now = get_now()
#         end = now + duration
#         while now < end:
#             now = get_now()
