import threading
import FreeSimpleGUI as sg
from gui.layouts.layout_three import layout_window3
from filter_raw_data import filter_eeg_csv
from epoch_mne import get_blink_threshold

def create_window_three():
    """The third window for the GUI."""

    layout_three = layout_window3()

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