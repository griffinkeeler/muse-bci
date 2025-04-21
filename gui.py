import time
from time import sleep
import threading
import pandas as pd
import FreeSimpleGUI as sg
from raw_data_collection import raw_eeg_to_csv
from filter_raw_data import filter_eeg_csv
from epoch_mne import get_blink_threshold

def countdown(window):
    """
    Background Thread
    Outputs:
      "3...2...1" one character at a time.
    Events:
        -THREE-: Outputs 3
        -TWO-:   Outputs 2
        -One-:   Outputs 1

        -PERIOD[n]-: Outputs '.'
        -OPEN_WINDOW_TWO: Opens the second window
    """

    # Keys for each phase.
    phase_keys = {0: '-THREE-', 1: '-TWO-', 2: '-ONE-'}
    # Keys for each step.
    step_keys = {0: {0: '-PERIOD1-', 1: '-PERIOD2-', 2: '-PERIOD3-'},
                 1: {0: '-PERIOD4-', 1: '-PERIOD5-', 2: '-PERIOD6-'}}
    # Background thread.
    for phase in range(0, 3):
        key = phase_keys[phase]
        # write_event_value() is used to communicate between
        # background thread and main thread. It passes the
        # tuple as an event and 'phase' as the value.
        sleep(0.25)
        window.write_event_value(('-THREAD-', key), phase)
        if phase == 2:
            # Opens window two once thread is complete.
            sleep(0.25)
            window.write_event_value(('-THREAD-', '-OPEN_WINDOW_TWO-'), phase)
        if phase in step_keys:
            for step in range(0, 3):
                key = step_keys[phase][step]
                sleep(0.25)
                window.write_event_value(('-THREAD-', key), step)

def change_dot_color(windows):
    """
    Background thread that changes the color of a red dot to
    green every 5 seconds over 75 seconds.

    Events:
        -RED_DOT-: Changes the dot color to red.
        -GREEN_DOT-: Changes the dot color to green for 0.3 seconds.
        -OPEN_WINDOW_THREE-: Saves the timestamps for each time the dot
        turns green and opens the third window.
    """

    # Background thread.
    for i in range(0, 5):
        # Closes the thread if window is closed.
        if i == 0:
            windows.write_event_value(('-THREAD-', '-RED_DOT-'), i)
        else:
            windows.write_event_value(('-THREAD-', '-GREEN_DOT-'), i)
            sleep(0.3)
        for c in range(0, 5):
            windows.write_event_value(('-THREAD-', '-RED_DOT-'), c)
            sleep(1)
        if i == 4:
            windows.write_event_value(('-THREAD-', '-RED_DOT-'), c)
            sleep(3)
            windows.write_event_value(('-THREAD-', '-OPEN_WINDOW_THREE-'), i)

def window_one():
    """The first window for the GUI."""

    layout_one = [[sg.Push(background_color='light grey'),
                   sg.Text("Welcome!",
                           text_color='black',
                           auto_size_text=True,
                           font=('Arial', 20),
                           background_color='light grey'),
                   sg.Push(background_color='light grey')],
                  [sg.Push(background_color='light grey'),
                   sg.Text('Press "Begin" to start calibration.',
                           text_color='black',
                           font=('Times New Roman', 16),
                           background_color='light grey'),
                   sg.Push(background_color='light grey')],
                  [sg.Text(" ", background_color='light grey')],
                  [sg.Push(background_color='light grey'),
                   sg.Button('Begin',
                             font=('Helvetica', 16)),
                   sg.Push(background_color='light grey')],
                  [sg.Push(background_color='light grey'),
                   sg.Text(key='-INTRO-',
                           font=('Times New Roman', 16),
                           text_color='black',
                           background_color='light grey'),
                   sg.Push(background_color='light grey')],
                  [(sg.Push(background_color='light grey'),
                    sg.Text(key='-DIGIT_ONE-',
                            text_color='black',
                            font=('Times New Roman', 14),
                            background_color='light grey'),
                    sg.Text(key='-P1-',
                            text_color='black',
                            background_color='light grey'),
                    sg.Text(key='-P2-',
                            text_color='black',
                            background_color='light grey'),
                    sg.Text(key='-P3-',
                            text_color='black',
                            background_color='light grey'),
                    sg.Text(key='-DIGIT_TWO-',
                            text_color='black',
                            font=('Times New Roman', 14),
                            background_color='light grey'),
                    sg.Text(key='-P4-',
                            text_color='black',
                            background_color='light grey'),
                    sg.Text(key='-P5-',
                            text_color='black',
                            background_color='light grey'),
                    sg.Text(key='-P6-',
                            text_color='black',
                            background_color='light grey'),
                    sg.Text(key='-DIGIT_THREE-',
                            text_color='black',
                            font=('Times New Roman', 14),
                            background_color='light grey'),
                    sg.Push(background_color='light grey'))]
                  ]

    # Window is created.
    window = sg.Window("Blink Calibrator", layout_one,
                       size=(400, 300),
                       auto_size_text=True,
                       background_color='light grey',
                       finalize=True,)

    # Main Loop
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break
        if event == 'Begin':
            # Begins the thread
            window.start_thread(lambda: countdown(window),
                                ('-THREAD-', '-THREAD ENDED-'))
        # A series of if statements that update the corresponding
        # window to based on the event received from the main
        # thread.
        elif event[0] == '-THREAD-':
            if event[1] == '-THREE-':
                window['-DIGIT_ONE-'].update('3')
                window['-INTRO-'].update('Beginning in: ')
            elif event[1] == '-TWO-':
                window['-DIGIT_TWO-'].update('2')
            elif event[1] == '-ONE-':
                window['-DIGIT_THREE-'].update('1')
            elif event[1] == '-PERIOD1-':
                window['-P1-'].update('.')
            elif event[1] == '-PERIOD2-':
                window['-P2-'].update('.')
            elif event[1] == '-PERIOD3-':
                window['-P3-'].update('.')
            elif event[1] == '-PERIOD4-':
                window['-P4-'].update('.')
            elif event[1] == '-PERIOD5-':
                window['-P5-'].update('.')
            elif event[1] == '-PERIOD6-':
                window['-P6-'].update('.')
            elif event[1] == '-OPEN_WINDOW_TWO-':
                window.close()
                window_two()
                break

def window_two():
    """The second window for the GUI."""

    layout_two = [[sg.Push(background_color='light grey'),
                   sg.Text('Sit completely still and focus on the red dot.',
                           text_color='black',
                           font=('Times New Roman', 20),
                           auto_size_text=True,
                           background_color='light grey')],
                  [sg.Push(background_color='light grey'),
                   sg.Text('Blink once each time the color changes.',
                           text_color='black',
                           font=('Times New Roman', 20),
                           auto_size_text=True,
                           background_color='light grey'),
                   sg.Push(background_color='light grey')],
                  [sg.Text(background_color='light grey')],
                  [sg.Text(background_color='light grey')],
                  [sg.Push(background_color='light grey'),
                   sg.Text('🔴',
                           key='-DOT-',
                           font=('Arial,', 40),
                           background_color='light grey'),
                   sg.Push(background_color='light grey')]
                  ]

    window = sg.Window("Calibration",
                       layout_two,
                       size=(400, 300),
                       background_color='light grey',
                       finalize=True)

    # The time the stream starts
    stream_start_time = time.time()

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
                             ).to_csv('blink_cue_timestamps.csv', index=False)
                window.close()
                window_three()
                break

def window_three():
    """The third window for the GUI."""

    layout_three = [[sg.Text(background_color='light grey')],
                    [sg.Text(background_color='light grey')],
                    [sg.Text(background_color='light grey')],
                    [sg.Text(background_color='light grey')],
                    [sg.Push(background_color='light grey'),
                     sg.Text("Calibration Complete!",
                             font=('Times New Roman', 20),
                             text_color='black',
                             background_color='light grey'),
                     sg.Push(background_color='light grey')],
                    [[sg.Push(background_color='light grey'),
                      sg.Button('View Results',
                                font=('Helvetica', 16)),
                      sg.Push(background_color='light grey')]],
                    [[sg.Push(background_color='light grey'),
                      sg.Text(key='-VIEW_THRESHOLD-',
                              background_color='light grey'),
                      sg.Push(background_color='light grey')]],
                    [sg.Text(background_color='light grey')],
                    [sg.Text(background_color='light grey')],
                    [sg.Text(background_color='light grey')]
                    ]

    window = sg.Window("Calibration Complete",
                       layout_three,
                       finalize=True,
                       size=(400, 300),
                       background_color='light grey')

    threading.Thread(target=lambda: filter_eeg_csv(
        input_path='/Users/griffinkeeler/PycharmProjects/muse-bci/raw_eeg_data.csv',
        output_path='/Users/griffinkeeler/PycharmProjects/muse-bci/filtered_eeg_data.csv'
    )).start()

    def compute_threshold():
        threshold = get_blink_threshold()
        window.write_event_value('-THRESHOLD_READY-', threshold)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        elif event == 'View Results':
            threading.Thread(target=compute_threshold, daemon=True).start()

        elif event == '-THRESHOLD_READY-':
            threshold = values['-THRESHOLD_READY-']
            window['-VIEW_THRESHOLD-'].update(f"Blink threshold: {threshold:.2f}")

def main():
    window_one()

if __name__ == '__main__':
    main()