import sys
from multiprocessing import Queue as p_Queue, Process, Event

import myPath
from res.scripts.loading import check_update, check_dependencies
from res.scripts.utils import FileLikeQueue, mkdir, remove
from res.scripts.config import is_gui_only
from res.scripts.gui import MainWindow, LoadingWindow


def main():
    # Redirect standard output
    output = FileLikeQueue()
    save_stdout = sys.stdout
    sys.stdout = output
    mkdir(myPath.TEMP_PATH)

    waveform_queue = p_Queue(maxsize=0)
    text_queue = p_Queue(maxsize=0)

    # start loading window

    # Init processes
    p_recognizer = None
    if not is_gui_only():
        from res.scripts.recognize import WhisperRecognizer
        running_flag = Event()

        recognizer = WhisperRecognizer(src_queue=waveform_queue, dst_queue=text_queue)
        p_recognizer = Process(target=recognizer.run, args=(running_flag, ))

        # Start
        p_recognizer.start()
        running_flag.wait()

    # Main GUI Process, Threads will be managed in Main Process
    win = MainWindow(themename='darkly')
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


