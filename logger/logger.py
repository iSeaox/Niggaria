import threading

class Logger:

    def __init__(self, io):
        self.__io = io

    def log(self, content, end="\n", subject="info"):
        self.__io.write("[" + str(threading.current_thread().getName()) + "]<"+str(subject)+"> " + str(content) + end)
