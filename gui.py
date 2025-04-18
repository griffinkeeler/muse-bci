import time
from time import sleep
import threading
import pandas as pd
import FreeSimpleGUI as sg
from raw_data_collection import raw_eeg_to_csv
from filter_raw_data import filter_eeg_csv
from epoch_mne import get_blink_threshold

def countdown(window):
    """Background thread that outputs
      "3...2...1" one character at a time."""

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

def blink_dot(windows):
    """Background thread that changes the color of a red dot to
    green every 5 seconds over 75 seconds."""

    # Background thread.
    for i in range(0, 16):
        # Closes the thread if window is closed.
        if i == 0:
            windows.write_event_value(('-THREAD-', '-RED_DOT-'), i)
        else:
            windows.write_event_value(('-THREAD-', '-GREEN_DOT-'), i)
            sleep(0.3)
        if i == 15:
            windows.write_event_value(('-THREAD-', '-RED_DOT-'), c)
            sleep(3)
            windows.write_event_value(('-THREAD-', '-DOT_DONE-'), i)
        for c in range(0, 5):
            windows.write_event_value(('-THREAD-', '-RED_DOT-'), c)
            sleep(1)

def window_one():
    """The first window for the GUI."""

    layout_one = [[sg.Push(),
                   sg.Text("Welcome!", text_color='white',
                           auto_size_text=True),
                   sg.Push()],
                  [sg.Push(),
                   sg.Text('Press "Begin" to start calibration.',
                           text_color='gold'),
                   sg.Push()],
                  [sg.Push(), sg.Button('Begin'), sg.Push()],
                  [sg.Push(), sg.Text(key='-INTRO-'), sg.Push()],
                  [(sg.Text(key='-DIGIT_ONE-', text_color='white'),
                    sg.Text(key='-P1-', text_color='white'),
                    sg.Text(key='-P2-', text_color='white'),
                    sg.Text(key='-P3-', text_color='white'),
                    sg.Text(key='-DIGIT_TWO-', text_color='white'),
                    sg.Text(key='-P4-', text_color='white'),
                    sg.Text(key='-P5-', text_color='white'),
                    sg.Text(key='-P6-', text_color='white'),
                    sg.Text(key='-DIGIT_THREE-', text_color='white'))],
                  ]

    # Window is created.
    window = sg.Window("Blink Calibrator", layout_one,
                       size=(500, 300), auto_size_text=True, finalize=True)

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

    layout_two = [[sg.Push(background_color='white'),
                   sg.Text('Focus on the red dot in front of you.\n'
                            'Blink once each time the color changes.',
                             text_color='black',
                             background_color='white'),
                   sg.Push(background_color='white')],
                  [sg.Text(background_color='white')],
                  [sg.Text(background_color='white')],
                  [sg.Push(background_color='white'),
                   sg.Text('🔴', key='-DOT-', background_color='white')
                      , sg.Push(background_color='white')]
                  ]

    window = sg.Window("Calibration", layout_two,
                           size=(250, 150), background_color='white', finalize=True)

    # The time the stream starts
    stream_start_time = time.time()

    threading.Thread(target=raw_eeg_to_csv).start()

    # Begins the thread right away.
    window.start_thread(lambda: blink_dot(window),
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
            elif event[1] == '-DOT_DONE-':
                # Saves the corresponding blink timestamps to a csv
                pd.DataFrame({'blink_cue_time': green_dot_times}
                             ).to_csv('blink_cue_timestamps.csv', index=False)
                window.close()
                window_three()
                break

def window_three():
    """The third window for the GUI."""

    layout_three = [[sg.Text()], [sg.Text()], [sg.Text()],
                    [sg.Text()],
                    [sg.Text("Calibration Complete!")],
                    [[sg.Push(), sg.Button('View Results'), sg.Push()]],
                    [[sg.Push(), sg.Text(key='-VIEW_THRESHOLD-'), sg.Push()]],
                    [sg.Text()], [sg.Text()], [sg.Text()]
                    ]

    window = sg.Window("Calibration Complete", layout_three, finalize=True)

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