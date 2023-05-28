import pyaudio


class CONST:
    # RECORDER
    DETECT_THRESHOLD_FIELD = 'detect_threshold'
    MOVING_AVERAGE_WINDOW_FIELD = 'moving_average_window'

    # RECOGNIZER
    MODEL_LIST = ('tiny', 'small', 'base', 'medium', 'large', 'large-v2')
    DEVICE_LIST = ('cuda', 'cpu')
    LANGUAGE = 'language'
    MODEL = 'model'

    # AUDIO
    SAMPLING_RATE = 16000
    CHANNELS = 1
    CHUNK_SIZE = 512
    FORMAT = pyaudio.paInt16

    # WEBHOOK
    WEBHOOK_URL = 'webhook_url'
    WEBHOOK_URL_TEXT = 'Webhook URL'

    # SHOW NAME
    SHOW_NAME = 'show_name'
    NAME_TEXT = '名前'

    # DEVICE LIST
    DEVICE = 'device'

    # BUTTON
    SETTING_BUTTON = 'setting'
    START_BUTTON = 'start'

    # GUI
    TITLE = '音声認識'
    WINDOW_WIDTH = 600
    WINDOW_HEIGHT = 330
    UPDATE_INTERVAL_FIELD = 'update_interval'

    # WorkFrame CONFIG TEXT
    DEVICE_TEXT = '使用デバイス'
    BUTTON_START_TEXT = '起動'
    BUTTON_STOP_TEXT = '停止'
    BUTTON_MODIFY_TEXT = '変更'
    BUTTON_SAVE_TEXT = '保存'
    SAVE_CONFIRM_TITLE = '設定の保存'
    SAVE_CONFIRM_TEXT = '変更を保存しますか？'
    YES = 'はい'
    NO = 'いいえ'
    CANCEL = 'キャンセル'

    # Message TEXT
    START_RECOGNIZING = "┏━━━━━━━━━━━━━━━━━━━━━━━━┓\n" \
                      + "┃            音声認識が開始しました。            ┃\n" \
                      + "┗━━━━━━━━━━━━━━━━━━━━━━━━┛"
