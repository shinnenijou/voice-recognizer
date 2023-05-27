import requests
import os
from threading import Thread, Event
from multiprocessing import Queue as p_Queue

from res.scripts.config import config, CONST

PROXIES = {}
if int(os.getenv('DEBUG', 0)) == 1:
    PROXIES = {
        'http': 'http://127.0.0.1:7890',
        'https': 'http://127.0.0.1:7890',
    }


class WebhookSender(Thread):

    def __init__(self, _running_flag: Event, **kwargs):
        super().__init__()

        self.__payload = {'username': '', 'content': ''}
        self.__session = requests.Session()

        self.__src_queue: p_Queue = kwargs.get('src_queue')
        self.__running_flag = _running_flag

    def send(self, url: str, name: str, content: str):
        self.__payload['content'] = content
        self.__payload['username'] = name

        try:
            self.__session.post(url, data=self.__payload, proxies=PROXIES)
        except:
            pass

    def run(self):
        url = config.get_value(CONST.WEBHOOK_URL)
        name = config.get_value(CONST.SHOW_NAME)

        while self.__running_flag.is_set():
            if self.__src_queue.empty():
                continue

            text = self.__src_queue.get()
            if text == '':
                continue

            print(text)
            self.send(url, name, text)

        self.__session.close()
