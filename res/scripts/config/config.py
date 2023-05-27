from configparser import RawConfigParser

from .. import utils
from .const import CONST

REQUIRE_FIELDS = {
    CONST.MOVING_AVERAGE_WINDOW_FIELD: 10,
    CONST.DETECT_THRESHOLD_FIELD: 0.05,
    CONST.UPDATE_INTERVAL_FIELD: 100,
    CONST.LANGUAGE: 'ja',
    CONST.MODEL: "large-v2",
    CONST.DEVICE: 'auto',
}


class Config(RawConfigParser):
    def __init__(self, config_file, *args, **kwargs):
        super().__init__(*args, **kwargs)
        utils.touch(config_file, '[global]')
        self.read(config_file)
        self.__section = self.sections()[0]
        self.__config_file = config_file
        for field, default_value in REQUIRE_FIELDS.items():
            if not self.has_option(self.__section, field):
                self.set_value(field, default_value)

        self.save()

    def get_value(self, option: str, fallback='') -> str:
        return self.get(self.__section, option, fallback=fallback)

    def get_int(self, option: str, fallback=0) -> int:
        return self.getint(self.__section, option, fallback=fallback)

    def get_float(self, option: str, fallback=0.0) -> float:
        return self.getfloat(self.__section, option, fallback=fallback)

    def get_bool(self, option: str, fallback=False) -> bool:
        return self.getboolean(self.__section, option, fallback=fallback)

    def set_value(self, option: str, value: any):
        self.set(self.__section, option, str(value))

    def save(self):
        with open(self.__config_file, 'w') as f:
            self.write(f)