import tkinter as tk
from threading import Event as t_Event
from PIL import Image, ImageTk, ImageSequence

import myPath
from res.scripts.config import CONST


class LoadingScreen(tk.Tk):
    def __init__(self, flag: t_Event):
        super().__init__()
        self.__stop_flag = flag

        # Loading Image
        self.__img = Image.open(myPath.LOADING_IMG)
        self.__gif_iter = ImageSequence.Iterator(self.__img)

        # Geometry
        width = self.__img.width
        height = self.__img.height

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))

        self.geometry(f'{width}x{height}+{x}+{y}')
        self.resizable(False, False)

        self.__image = tk.Label(self)
        self.__image.grid(row=0, column=0)

        self.__label = tk.Label(self, text="Now Loading")
        self.__label.grid(row=0, column=0, sticky=tk.N)

        self.show_next_frame()
        self.after(int(1000 / CONST.LOADING_FRAMERATE), self.update)

    def update(self) -> None:
        if self.__stop_flag.is_set():
            self.destroy()
        else:
            self.show_next_frame()
            self.after(int(1000 / CONST.LOADING_FRAMERATE), self.update)

    def show_next_frame(self):
        try:
            cur_frame = ImageTk.PhotoImage(self.__gif_iter.__next__())
        except StopIteration:
            self.__gif_iter = ImageSequence.Iterator(self.__img)
            cur_frame = ImageTk.PhotoImage(self.__gif_iter.__next__())

        self.__image.config(image=cur_frame)
        self.__image.image = cur_frame
