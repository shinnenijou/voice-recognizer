import tkinter as tk

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from res.scripts.config import CONST

from.frame import WorkFrame
from .button import TransButton
from .text import WorkText


class MainWindow(ttk.Window):
    def __init__(self, **kwargs):
        voice_queue = kwargs.pop('voice_queue')
        text_queue = kwargs.pop('text_queue')

        super().__init__(**kwargs)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2) - (CONST.WINDOW_WIDTH / 2))
        y = int((screen_height / 2) - (CONST.WINDOW_HEIGHT / 2))

        self.title(CONST.TITLE)
        self.geometry(f'{CONST.WINDOW_WIDTH}x{CONST.WINDOW_HEIGHT}+{x}+{y}')
        self.resizable(False, False)

        # Main work frame
        self.work_frame = WorkFrame(self, voice_queue=voice_queue, text_queue=text_queue, padding=15)
        self.work_frame.pack(expand=True, fill=BOTH)

        # Menu

    def run(self):
        # override sys callback
        self.protocol("WM_DELETE_WINDOW", self.on_exit)

        self.mainloop()

    def on_exit(self):
        for name, child in self.children.items():
            if hasattr(child, 'on_exit'):
                getattr(child, 'on_exit')()

        self.destroy()
