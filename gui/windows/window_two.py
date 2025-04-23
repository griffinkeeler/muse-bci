import threading
import time
import pandas as pd
import FreeSimpleGUI as sg
from gui.layouts.layout_two import layout_window2
from gui.windows.window_three import create_window_three
from raw_data_collection import raw_eeg_to_csv
from threads.calibration_dot import change_dot_color

def create_window_two():
    """The second window for the GUI."""

    layout_two = layout_window2()

    window = sg.Window("Calibration",
                       layout_two,
                       size=(400, 300),
                       background_color='light grey',
                       finalize=True)


    threading.Thread(target=raw_eeg_to_csv).start()

    # Begins the thread right away.
    window.start_thread(lambda: change_dot_color(window),
                            ('-THREAD-', '-THREAD ENDED-'))

    # A list of times the dot turns green
    green_dot_times = []
    # Main Loop
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event[0] == '-THREAD-':
            if event[1] == '-GREEN_DOT-':
                window['-DOT-'].update('🟢')
                # The exact time the dot turns green is added to the
                # green_dot_times list
                cue_time = time.time()
                green_dot_times.append(cue_time)
            elif event[1] == '-RED_DOT-':
                window['-DOT-'].update('🔴')
            elif event[1] == '-OPEN_WINDOW_THREE-':
                # Saves the corresponding blink timestamps to a csv
                pd.DataFrame({'blink_cue_time': green_dot_times}
                             ).to_csv('/Users/griffinkeeler/PycharmProjects/muse-bci/blink_cue_timestamps.csv', index=False)
                window.close()
                create_window_three()
                break
