import sys
from multiprocessing import Queue as p_Queue, Process, Event as p_Event
from threading import Thread, Event as t_Event

import myPath
from res.scripts.loading import check_update, check_dependencies
from res.scripts.utils import FileLikeQueue, mkdir, remove
from res.scripts.config import is_gui_only
from res.scripts.gui import MainWindow, LoadingScreen


# GLOBAL
p_recognizer = None
waveform_queue = p_Queue(maxsize=0)
text_queue = p_Queue(maxsize=0)
loading_screen = None


def loading(flag: t_Event):
    global p_recognizer
    global loading_screen

    # update resource
    check_update()
    check_dependencies()

    # Init processes
    if not is_gui_only():
        from res.scripts.recognize import WhisperRecognizer
        running_flag = p_Event()

        recognizer = WhisperRecognizer(src_queue=waveform_queue, dst_queue=text_queue)
        p_recognizer = Process(target=recognizer.run, args=(running_flag,), name='Whisper')

        # Start
        p_recognizer.start()
        running_flag.wait()

    flag.set()


def main():
    global loading_screen

    # Redirect standard output
    output = FileLikeQueue()
    save_stdout = sys.stdout
    sys.stdout = output
    mkdir(myPath.TEMP_PATH)

    # start loading screen
    complete_flag = t_Event()
    t_loading = Thread(target=loading, args=(complete_flag, ))
    loading_screen = LoadingScreen(complete_flag)
    loading_screen.overrideredirect(True)
    t_loading.start()
    loading_screen.mainloop()
    t_loading.join()

    # Main GUI Process, Threads will be managed in Main Process
    win = MainWindow(themename='minty')
    win.init(waveform_queue, text_queue)

    # start main window
    win.run()

    # Exit
    if not is_gui_only():
        p_recognizer.terminate()

    remove(myPath.TEMP_PATH)
    sys.stdout = save_stdout


if __name__ == '__main__':
    main()
