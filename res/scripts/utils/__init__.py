import os
import shutil
from multiprocessing import Queue


class FileLikeQueue:
    def __init__(self):
        self.__queue = Queue(maxsize=0)

    def write(self, data):
        self.__queue.put(data)

    def flush(self):
        pass

    def read(self):
        ret = []
        while not self.__queue.empty():
            ret.append(self.__queue.get())

        return ret


class MoveAverage:
    def __init__(self, window: int):
        self.__tail = 0
        self.__window = window
        self.__queue = [0.0] * window
        self.__average = 0.0

    def enqueue(self, value: float):
        head = self.__queue[self.__tail]
        value = value / self.__window

        self.__queue[self.__tail] = value
        self.__average = self.__average - head + value

        self.__tail = (self.__tail + 1) % self.__window

        return self.__average

    def set_average(self, value: float):
        self.__average = value
        for i in range(self.__window):
            self.__queue[i] = value / self.__window

    @property
    def average(self):
        return self.__average


def isfile(file_path):
    return os.path.isfile(file_path)


def isdir(dir_path):
    return os.path.isdir(dir_path)


def touch(file_path, content=''):
    if isfile(file_path):
        return

    with open(file_path, 'w') as file:
        file.write(content)


def mkdir(file_path):
    if os.path.isdir(file_path):
        return

    os.mkdir(file_path)


def remove(path: str):
    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        pass
    except Exception as e:
        print(e)


def get_hhmmss(seconds: float):
    dec = seconds - int(seconds)
    seconds = int(seconds)

    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%d:%d:%.2f" % (h, m, s + dec)


def ass_headers():
    text = ""\
         + "[Events]\n" \
         + "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"

    return text


def ass_event(start: str, end: str, text: str):
    return f"Dialogue: 0,{start},{end},,,0,0,0,,{text}\n"


def rm(file_path):
    os.remove(file_path)


def get_files(path):
    return os.listdir(path)
