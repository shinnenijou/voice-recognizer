import wave
import os
from threading import Thread, Event
from queue import Queue as t_Queue

import pyaudio
import torch

import myPath
from res.scripts import utils
from res.scripts.config import CONST, config, STRING


SAMPLING_RATE = 16000
torch.set_num_threads(1)


class VoiceDetector(Thread):

    def __init__(self, _running_flag: Event, **kwargs):
        super().__init__()
        self.__model, model_utils = torch.hub.load(
            repo_or_dir=os.path.join(myPath.dirname(__file__), "silero-vad"),
            model='silero_vad',
            force_reload=True,
            source='local'
        )

        (self.__get_speech_timestamps,
         self.__save_audio,
         self.__read_audio,
         self.__VADIterator,
         self.__collect_chunks) = model_utils

        self.__average_prob = utils.MoveAverage(config.get_int(STRING.CONFIG_AVERAGE_WINDOW))
        self.__sentence_flag = False
        self.__detect_threshold = config.get_float(STRING.CONFIG_DETECT_THRESHOLD)

        self.__index = 0
        self.__running_flag = _running_flag
        self.__src_queue: t_Queue = kwargs.get('src_queue')
        self.__dst_queue: t_Queue = kwargs.get('dst_queue')

    def predict_probability(self, file):
        wav = self.__read_audio(file, sampling_rate=SAMPLING_RATE)
        return self.__model(wav, SAMPLING_RATE).item()

    def run(self):
        wave_data = b''
        while self.__running_flag.is_set():
            if self.__src_queue.empty():
                continue

            data = self.__src_queue.get()
            file = self.save_waveform(data)

            # predict voice probability
            prob = self.predict_probability(file)
            average_prob = self.__average_prob.average
            self.__average_prob.enqueue(prob)
            utils.rm(file)

            if not self.__sentence_flag and prob > average_prob / self.__detect_threshold:
                self.__sentence_flag = True
                wave_data = b''
            elif self.__sentence_flag and prob < average_prob * self.__detect_threshold:
                self.__sentence_flag = False
                self.__average_prob.set_average(prob)
                file = self.save_waveform(wave_data)
                self.__dst_queue.put((file, config.get_value(STRING.CONFIG_LANGUAGE)))
                wave_data = b''

            if self.__sentence_flag:
                wave_data = wave_data + data

    def save_waveform(self, data: bytes):
        self.__index = self.__index + 1
        file = os.path.join(myPath.TEMP_PATH, f'{self.__index}.wav')
        with wave.open(file, 'wb') as wf:
            wf.setnchannels(CONST.CHANNELS)
            wf.setsampwidth(pyaudio.get_sample_size(CONST.FORMAT))
            wf.setframerate(CONST.SAMPLING_RATE)
            wf.writeframes(data)

        return file
