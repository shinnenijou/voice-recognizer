from queue import Queue as t_Queue

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from res.scripts.config import CONST, is_gui_only
from res.scripts.managers import ThreadManager

from .workFrame import WorkFrame
from .loadingScreen import LoadingScreen


class MainWindow(ttk.Window):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title(CONST.TITLE)
        self.geometry(CONST.WINDOW_SIZE)

        self.__thread_manager = ThreadManager()
        self.__work_tab = WorkFrame(self)

    def run(self):
        # override sys callback
        self.protocol("WM_DELETE_WINDOW", self.on_exit)

        # Work Tab

        self.__work_tab.pack()
        self.__work_tab.init_widgets('pack')

        self.mainloop()

    def on_exit(self):
        self.stop_threads()
        self.destroy()

    def init(self, waveform_queue, text_queue):
        # Init Threads
        if not is_gui_only():
            self.__init_threads(waveform_queue, text_queue)

        # Init Widgets
        self.__init_widgets()

    def __init_threads(self, waveform_queue, text_queue):
        record_queue = t_Queue(maxsize=0)

        from res.scripts.stream import MicrophoneRecorder
        self.__thread_manager.add(
            MicrophoneRecorder,
            "Recorder",
            dst_queue=record_queue
        )

        from res.scripts.stream import VoiceDetector
        self.__thread_manager.add(
            VoiceDetector,
            "Detector",
            src_queue=record_queue,
            dst_queue=waveform_queue
        )

        from res.scripts.webhook import WebhookSender
        self.__thread_manager.add(
            WebhookSender,
            "Sender",
            src_queue=text_queue
        )

    def __init_widgets(self):
        # WEBHOOK URL
        self.__work_tab.add_entry(
            label_args={'text': CONST.WEBHOOK_URL_TEXT, 'justify': RIGHT},
            label_pos={},
            entry_args={'name': CONST.WEBHOOK_URL, 'exportselection': False, 'width': 60},
            entry_pos={}
        )

        # Show Name
        self.__work_tab.add_entry(
            label_args={'text': CONST.NAME_TEXT, 'justify': RIGHT},
            label_pos={},
            entry_args={'name': CONST.SHOW_NAME, 'exportselection': False, 'width': 30},
            entry_pos={}
        )

        # Device List
        # self.__work_tab.add_combox(
        #     label_args={'text': CONST.DEVICE_TEXT},
        #     label_pos={},
        #     combox_args={'name': CONST.DEVICE, 'values': CONST.DEVICE_LIST, 'width': 5,
        #                  'justify': CENTER, 'state': 'readonly'},
        #     combox_pos={}
        # )

        # Setting Button
        # self.__work_tab.add_trans_button(
        #     b1_args={'text': CONST.BUTTON_MODIFY_TEXT, 'command': self.__work_tab.enable_setting,
        #              'name': CONST.SETTING_BUTTON, 'width': 10},
        #     b1_pos={},
        #     b2_args={'text': CONST.BUTTON_SAVE_TEXT, 'command': self.__work_tab.save_config},
        #     b2_pos={}
        # )

        # start button
        self.__work_tab.add_trans_button(
            b1_args={'text': CONST.BUTTON_START_TEXT, 'command': self.start_threads, 'name': CONST.START_BUTTON,
                     'width': 10, 'bootstyle': 'primary'},
            b1_pos={},
            b2_args={'text': CONST.BUTTON_STOP_TEXT, 'command': self.stop_threads, 'bootstyle': 'danger'},
            b2_pos={}
        )

        # Scrolled Text
        self.__work_tab.add_scrolledtext(
            text_args={'height': 10, 'pady': 5, 'state': DISABLED},
            text_pos={},
            bar_args={'bootstyle': 'round'},
            bar_pos={}
        )

    def start_threads(self):
        if self.__thread_manager.is_running():
            return True

        # 保存配置
        self.__work_tab.clear_text()
        self.__work_tab.save_config(True)

        result = self.__thread_manager.start()
        if result:
            self.__work_tab.disable_setting()

        return result

    def stop_threads(self):
        result = self.__thread_manager.stop()
        if result:
            self.__work_tab.enable_setting()

        return result
