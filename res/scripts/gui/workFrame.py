import sys

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs.dialogs import Messagebox
from ttkbootstrap.scrolled import ScrolledText

from res.scripts.config import CONST, config


class WorkFrame(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # widgets
        self.__pos_args = {}
        self.__pos_method = 'pack'

        # ScrolledText
        self.__text = None
        self.__text_pos = None

        # register update
        self.__update_interval = config.get_int(CONST.UPDATE_INTERVAL_FIELD)
        self.after(self.__update_interval, self.__update)

    @property
    def pos_method(self):
        return self.__pos_method

    def init_widgets(self, method: str = 'pack'):
        if hasattr(self, f'{method}_children'):
            self.__pos_method = method

        getattr(self, f'{self.__pos_method}_children')()

    def grid_children(self):
        for name, widget in self.children.items():
            if name in self.__pos_args:
                widget.grid(**self.__pos_args[name])

        if  self.__text is not None:
            self.__text.grid(**self.__text_pos)

    def pack_children(self):
        for name, widget in self.children.items():
            if name in self.__pos_args:
                widget.pack(**self.__pos_args[name])

        if  self.__text is not None:
            self.__text.pack(**self.__text_pos)

    def place_children(self):
        for name, widget in self.children.items():
            if name in self.__pos_args:
                widget.place(**self.__pos_args[name])

        if  self.__text is not None:
            self.__text.place(**self.__text_pos)

    def __update(self) -> None:
        self.after(self.__update_interval, self.__update)

        if self.__text is None:
            return

        texts = sys.stdout.read()
        for text in texts:
            if text == '':
                continue

            self.__text.insert('end', text)
            self.__text.see(END)

    def clear_text(self):
        self.__text.delete(1.0, END)

    def disable_setting(self):
        for name, child in self.children.items():
            if isinstance(child, ttk.Entry):
                child.configure(state=DISABLED)
            elif isinstance(child, ttk.Combobox):
                child.configure(state=DISABLED)

    def enable_setting(self):
        for name, child in self.children.items():
            if isinstance(child, ttk.Entry):
                child.configure(state=NORMAL)
            elif isinstance(child, ttk.Combobox):
                child.configure(state=READONLY)

        return True

    def save_config(self, not_ask=False):
        if not not_ask:
            result = Messagebox.show_question(
                message=CONST.SAVE_CONFIRM_TEXT,
                title=CONST.SAVE_CONFIRM_TITLE,
                parent=self,
                buttons=[f'{CONST.YES}:primary', f'{CONST.NO}: secondary']
            )

            if result == CONST.NO or result is None:
                return False

        for name, widget in self.children.items():
            if isinstance(widget, ttk.Entry):
                config.set_value(name, widget.get())
            elif isinstance(widget, ttk.Combobox):
                config.set_value(name, widget.get())

        config.save()

        self.disable_setting()
        return True

    def add_entry(self, label_args: dict, label_pos: dict, entry_args: dict, entry_pos: dict):
        if 'name' not in label_args:
            label_args['name'] = '_'.join(['label', str(len(self.children))])

        if 'name' not in entry_args:
            entry_args['name'] = '_'.join(['entry', str(len(self.children))])

        label = ttk.Label(self, **label_args)
        entry = ttk.Entry(self, **entry_args)
        entry.insert(0, config.get_value(entry_args['name']))

        self.__pos_args[label_args['name']] = label_pos
        self.__pos_args[entry_args['name']] = entry_pos

    def add_combox(self, label_args: dict, label_pos: dict, combox_args: dict, combox_pos: dict):
        if 'name' not in label_args:
            label_args['name'] = '_'.join(['label', str(len(self.children))])

        if 'name' not in combox_args:
            combox_args['name'] = '_'.join(['combox', str(len(self.children))])

        label = ttk.Label(self, **label_args)
        combox = ttk.Combobox(self, **combox_args)

        self.__pos_args[label_args['name']] = label_pos
        self.__pos_args[combox_args['name']] = combox_pos

        values = combox_args.get('values', ())
        if len(values) == 0:
            return

        try:
            combox.current(values.index(config.get_value(combox_args['name'])))
        except ValueError:
            combox.current(0)

    def add_button(self, args: dict, pos: dict):
        if 'name' not in args:
            args['name'] = '_'.join(['button', str(len(self.children))])

        ttk.Button(self, **args)
        self.__pos_args[args['name']] = pos

    def add_trans_button(self, b1_args: dict, b1_pos: dict, b2_args: dict, b2_pos: dict):
        if 'name' not in b1_args:
            b1_args['name'] = '_'.join(['trans_button_1', str(len(self.children))])

        if 'name' not in b2_args:
            b2_args['name'] = '_'.join(['trans_button_2', str(len(self.children))])

        button_2 = ttk.Button(self, **b2_args)
        button_1 = ttk.Button(self, **b1_args)

        def wrapper(cmd, name_1, name_2):
            widget_1 = self.children[name_1]
            widget_2 = self.children[name_2]

            def func():
                if callable(cmd) and cmd():
                    getattr(widget_1, f'{self.pos_method}_forget')()
                    getattr(widget_2, f'{self.pos_method}')(self.__pos_args[name_2])

            return func

        if 'command' in b1_args and callable(b1_args['command']):
            button_1.configure(command=wrapper(b1_args['command'], b1_args['name'], b2_args['name']))

        if 'command' in b2_args and callable(b2_args['command']):
            button_2.configure(command=wrapper(b2_args['command'], b2_args['name'], b1_args['name']))

        self.__pos_args[b1_args['name']] = b1_pos
        self.__pos_args[b2_args['name']] = b2_pos

    def add_scrolledtext(self, text_args: dict, text_pos: dict):
        if 'name' not in text_args:
            text_args['name'] = '_'.join(['scrolledtext', str(len(self.children))])

        # Text frame
        self.__text = ScrolledText(self, **text_args)
        self.__text_pos = text_pos
