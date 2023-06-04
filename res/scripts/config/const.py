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
    DEVICE_LIST = ('cuda', 'cpu', 'auto')

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
    LABEL_PROXY = 'プロキシ'
    LABEL_MODEL = '認識モデル'
    LABEL_SAVE = '保存'
    LABEL_CANCEL = 'キャンセル'
    LABEL_YES = 'はい'
    LABEL_NO = 'いいえ'
    LABEL_MODIFY_MARK = '*'
    LABEL_DEVICE = '使用デバイス'

    # BUTTON TEXT
    BUTTON_START = '起動'
    BUTTON_STOP = '停止'

    # TITLE TEXT
    TITLE_MAIN = '音声認識ちゃん'
    TITLE_ABOUT = f'{TITLE_MAIN}について...'
    TITLE_SETTING = '詳細設定'

    # MENU
    MENU_HELP = 'ヘルプ'
    MENU_OPTIONAL = 'オプション'

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
    CONFIRM_SETTING_MODIFY = "変更した項目を保存しますか\n※一部の設定は再起動してから有効になります"

    # OTHERS
    LANGUAGE_MAP = {
        '日本語': 'ja',
        '中国語': 'zh'
    }


class ThreadCommand:
    ShowDownloadProgress = 1

    RebootExitCode = 100  # avoid 0, 1, 2 due to wellknown exit code
