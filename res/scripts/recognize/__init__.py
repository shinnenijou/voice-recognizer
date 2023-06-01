import os
from multiprocessing import Event

from faster_whisper import WhisperModel
import torch

import myPath
from res.scripts.config import CONST, config, STRING


class WhisperRecognizer:
    def __init__(self, **kwargs):
        super().__init__()
        self.__src_queue = kwargs.get('src_queue')
        self.__dst_queue = kwargs.get('dst_queue')
        self.__language = config.get_value(CONST.LANGUAGE)
        self.__model = None

    def init(self):
        device = config.get_value(STRING.CONFIG_DEVICE)
        if device == 'auto':
            device = 'cuda' if torch.cuda.is_available() else 'cpu'

        self.__model = WhisperModel(
            model_size_or_path=os.path.join(myPath.MODEL_PATH, config.get_value(STRING.CONFIG_MODEL)),
            device=device
        )

        print("cuda: ", torch.cuda.is_available())

        if os.path.exists(myPath.LOADING_WAV):
            self.transcribe(myPath.LOADING_WAV)
            pass

    def transcribe(self, _input: str):
        segments, info = self.__model.transcribe(
            _input,
            language=self.__language,
            vad_filter=True
        )

        texts = []
        for segment in segments:
            text = segment.text.strip()
            if text == '':
                continue

            texts.append(text)

        return texts

    def run(self, running_flag: Event):
        self.init()

        running_flag.set()

        while True:
            file = self.__src_queue.get()
            texts = self.transcribe(file)
            for text in texts:
                self.__dst_queue.put(text)
