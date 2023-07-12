import os
from multiprocessing import Event

from faster_whisper import WhisperModel
import torch

import myPath
from res.scripts.config import CONST, config, STRING
from res.scripts.utils import logger


class WhisperRecognizer:
    def __init__(self, **kwargs):
        super().__init__()
        self.__src_queue = kwargs.get('src_queue')
        self.__dst_queue = kwargs.get('dst_queue')
        self.__model = None

    def init(self):
        device = config.get_value(STRING.CONFIG_DEVICE)
        if device == 'auto':
            device = 'cuda' if torch.cuda.is_available() else 'cpu'

        self.__model = WhisperModel(
            model_size_or_path=os.path.join(myPath.MODEL_PATH, config.get_value(STRING.CONFIG_MODEL)),
            device=device
        )

        if not torch.cuda.is_available():
            logger.log_warning("cuda is not available!")
        else:
            logger.log_info("cuda is available.")

        if os.path.exists(myPath.LOADING_WAV):
            try:
                self.transcribe(myPath.LOADING_WAV, 'ja')
            except Exception as e:
                logger.log_error("[WhisperRecognizer:transcribe]", str(e))

    def transcribe(self, _input: str, _language: str):
        segments, info = self.__model.transcribe(
            _input,
            language=_language,
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
            file, language = self.__src_queue.get()
            texts = self.transcribe(file, language)
            for text in texts:
                self.__dst_queue.put(text)
