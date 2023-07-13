import time
import requests
from threading import Thread, Event
from multiprocessing import Queue as p_Queue

from res.scripts.config import config, STRING, CONST
from res.scripts.utils import logger

PROXIES = {}
if config.get_value(STRING.CONFIG_PROXY):
    PROXIES = {
        'http': config.get_value(STRING.CONFIG_PROXY),
        'https': config.get_value(STRING.CONFIG_PROXY),
    }


class WebhookSender(Thread):

    def __init__(self, _running_flag: Event, **kwargs):
        super().__init__()

        self.__payload = {'username': '', 'content': ''}
        self.__session = requests.Session()

        self.__src_queue: p_Queue = kwargs.get('src_queue')
        self.__running_flag = _running_flag

    def send(self, url: str, name: str, content: str):
        if not url:
            return

        self.__payload['content'] = content
        self.__payload['username'] = name

        try:
            self.__session.post(url, data=self.__payload, proxies=PROXIES)
        except Exception as e:
            logger.log_error("[WebhookSender:send]" + str(e))

    def run(self):
        url = config.get_value(STRING.CONFIG_WEBHOOK)
        name = config.get_value(STRING.CONFIG_NAME)

        while self.__running_flag.is_set():
            if self.__src_queue.empty():
                time.sleep(config.get_int(STRING.CONFIG_UPDATE_INTERVAL) / 1000)
                continue

            text = self.__src_queue.get()
            if text == '':
                continue

            print(text)
            self.send(url, name, text)

        self.__session.close()
