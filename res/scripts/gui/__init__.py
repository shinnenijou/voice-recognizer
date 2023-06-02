import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from res.scripts.config import CONST, config, STRING
import myPath

from .frame import WorkFrame
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

        self.title(STRING.TITLE_MAIN)
        self.geometry(f'{CONST.WINDOW_WIDTH}x{CONST.WINDOW_HEIGHT}+{x}+{y}')
        self.resizable(False, False)

        # Main work frame
        self.work_frame = WorkFrame(self, voice_queue=voice_queue, text_queue=text_queue, padding=15)
        self.work_frame.pack(expand=True, fill=BOTH)

        # Menu
        menu = ttk.Menu(self)
        self.configure(menu=menu)

        help_menu = ttk.Menu(menu)
        help_menu.add_command(label=STRING.TITLE_ABOUT, command=self.pop_about_window)
        menu.add_cascade(label=STRING.MENU_HELP, menu=help_menu)

    def run(self):
        # override sys callback
        self.protocol("WM_DELETE_WINDOW", self.on_exit)

        self.mainloop()

    def on_exit(self):
        for name, child in self.children.items():
            if hasattr(child, 'on_exit'):
                getattr(child, 'on_exit')()

        self.destroy()

    def pop_about_window(self):
        win = ttk.Toplevel(master=self, title=STRING.TITLE_ABOUT)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2) - (CONST.ABOUT_WIDTH / 2))
        y = int((screen_height / 2) - (CONST.ABOUT_HEIGHT / 2))
        win.geometry(f'{CONST.ABOUT_WIDTH}x{CONST.ABOUT_HEIGHT}+{x}+{y}')

        about_frame = ttk.Frame(win, padding=15)
        about_frame.pack(fill=BOTH, expand=YES)

        # Logo
        img = ttk.Image.open(myPath.LOGO_IMG)
        photo = ttk.ImageTk.PhotoImage(img)
        label = ttk.Label(about_frame, image=photo)
        label.image = photo
        label.pack()
        img.close()

        # Version
        ttk.Label(about_frame, text=f'Version: {config.get_value(STRING.CONFIG_VERSION)}').pack()

        # Story
        label_frame = ttk.Labelframe(about_frame, text=STRING.LABEL_STORY_TITLE)
        label_frame.pack(fill=BOTH, expand=YES, pady=(15, 0))
        ttk.Label(label_frame, text=STRING.LABEL_STORY_TEXT).pack()
