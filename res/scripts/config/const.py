import pyaudio

class CONST:
    # GEOMETRY
    WINDOW_WIDTH = 600
    WINDOW_HEIGHT = 360
    ABOUT_WIDTH = 300
    ABOUT_HEIGHT = 300

    # LOADING
    LOADING_FRAMERATE = 12

    # RECOGNIZER
    MODEL_LIST = ('tiny', 'small', 'base', 'medium', 'large', 'large-v2')
    DEVICE_LIST = ('cuda', 'cpu')

    # AUDIO
    SAMPLING_RATE = 16000
    CHANNELS = 1
    CHUNK_SIZE = 512
    FORMAT = pyaudio.paInt16


class STRING:
    # LABEL TEXT
    LABEL_WEBHOOK = 'Webhook URL'
    LABEL_NAME = '名前'
    LABEL_STORY_TITLE = 'フェンリルちゃんについて'
    LABEL_STORY_TEXT = 'お楽しみに'
    LABEL_SETTING = '設定'
    LABEL_LANGUAGE = '認識言語'
    LABEL_UPDATE = 'アップデート確認中...'
    LABEL_DOWNLOAD = 'ダウンロード中...'

    # BUTTON TEXT
    BUTTON_START = '起動'
    BUTTON_STOP = '停止'

    # TITLE TEXT
    TITLE_MAIN = '音声認識ちゃん'
    TITLE_ABOUT = f'{TITLE_MAIN}について...'

    # MENU
    MENU_HELP = 'ヘルプ'

    # CONFIG FIELDS
    CONFIG_VERSION = 'version'
    CONFIG_LANGUAGE = 'language'
    CONFIG_MODEL = 'model'
    CONFIG_DEVICE = 'device'
    CONFIG_NAME = 'show_name'
    CONFIG_WEBHOOK = 'webhook_url'
    CONFIG_DETECT_THRESHOLD = 'detect_threshold'
    CONFIG_AVERAGE_WINDOW = 'moving_average_window'
    CONFIG_UPDATE_INTERVAL = 'update_interval'
    CONFIG_PROXY = 'proxy'

    # Message TEXT
    START_RECOGNIZING = "┏━━━━━━━━━━━━━━━━━━━━━━━━┓\n" \
                      + "┃                              音声認識が開始しました。                         ┃\n" \
                      + "┗━━━━━━━━━━━━━━━━━━━━━━━━┛"

    # OTHERS
    LANGUAGE_MAP = {
        '日本語': 'ja',
        '中国語': 'zh'
    }


class ThreadCommand:
    ShowDownloadProgress = 1

    RebootExitCode = 100  # avoid 0, 1, 2 due to wellknown exit code
