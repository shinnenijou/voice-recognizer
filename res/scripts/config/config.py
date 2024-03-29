from configparser import RawConfigParser

from .. import utils
from .const import STRING

REQUIRE_FIELDS = {
    STRING.CONFIG_AVERAGE_WINDOW: 10,
    STRING.CONFIG_DETECT_THRESHOLD: 0.2,
    STRING.CONFIG_UPDATE_INTERVAL: 100,
    STRING.CONFIG_LANGUAGE: 'ja',
    STRING.CONFIG_MODEL: "large-v2",
    STRING.CONFIG_DEVICE: 'auto',
    STRING.CONFIG_VERSION: '0.0.0',
    STRING.CONFIG_PROXY: '',
    STRING.CONFIG_TIMEOUT: 3,
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

        # some special validata
        if not utils.is_unit_float(self.get_value(STRING.CONFIG_DETECT_THRESHOLD)):
            self.set_value(STRING.CONFIG_DETECT_THRESHOLD, REQUIRE_FIELDS[STRING.CONFIG_DETECT_THRESHOLD])

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