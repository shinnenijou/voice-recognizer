import tkinter as tk
from threading import Event as t_Event


class LoadingScreen(tk.Tk):
    def __init__(self, flag: t_Event):
        super().__init__()
        self.__stop_flag = flag

        width = 600
        height = 300

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))

        self.geometry(f'{width}x{height}+{x}+{y}')
        self.resizable(False, False)

        label = tk.Label(text='loading')
        label.pack()

        self.after(100, self.update)

    def update(self) -> None:
        if self.__stop_flag.is_set():
            self.destroy()
        else:
            self.after(100, self.update)

