import tkinter as tk
from threading import Event


class LoadingWindow(tk.Tk):
    def __init__(self, complete_flag: Event):
        super().__init__()

        self.__complete_flag = complete_flag

        self.after(100, self.__update)

    def __update(self):
        if self.__complete_flag.is_set():
            self.destroy()
        else:
            self.after(100, self.__update)
