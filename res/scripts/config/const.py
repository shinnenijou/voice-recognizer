import pyaudio


class CONST:
    # GEOMETRY
    WINDOW_WIDTH = 600
    WINDOW_HEIGHT = 480
    ABOUT_WIDTH = 400
    ABOUT_HEIGHT = 350
    GLOBAL_FONT = ("Microsoft YaHei UI", 10)

    # LOADING
    LOADING_FRAMERATE = 15

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
    LABEL_STORY_TEXT = '昔々、とある遠い国で\n' \
                       '一群の小さなフィンリルが\n' \
                       '可愛くて優しい魔王に従い\n' \
                       '毎日幸せに過ごしていました\n' \
                       '\n' \
                       'しかし\n' \
                       '魔王の言葉は難しくて\n' \
                       'フィンリルたちは理解できず\n' \
                       '交流することができませんでした\n' \
                       '「魔王ちゃま、今何言ってまちゅか」\n' \
                       '「！＠＃＄％＾＆＠＃＄」\n' \
                       '「魔王ちゃま、分かんないよ！」\n' \
                       'そして、何十年、何百年を経て\n' \
                       'ついに、一狼の狼工知能\n' \
                       '「フェンリルちゃん」\n' \
                       'が出現しました...'
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
    LABEL_DETECT_THRESHOLD = '認識感度'
    LABEL_AUTHOR = 'Shinnen'
    LABEL_TIMEOUT = '送信タイムアウト'

    # TIPS
    TIP_DETECT_THRESHOLD = 'この数字は、大きいほど音声が認識されやすいが、\nノイズも拾われやすくなる。実際試しながら適切な数値に調整してください。'
    TIP_PROXY = '入力例：http://127.0.0.1:7890'

    # BUTTON TEXT
    BUTTON_START = '起動'
    BUTTON_STOP = '停止'

    # TITLE TEXT
    TITLE_MAIN = 'フェンリルちゃん'
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
    CONFIG_TIMEOUT = 'timeout'

    # Message TEXT
    START_RECOGNIZING = "┏━━━━━━━━━━━━━━━━━━━━━━━━┓\n" \
                      + "┃      音声認識が開始しました。   ┃\n" \
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
