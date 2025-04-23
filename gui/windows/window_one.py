import FreeSimpleGUI as sg
from gui.layouts.layout_one import layout_window1
from threads.countdown import countdown
from gui.windows.window_two import create_window_two

def create_window_one():
    """The first window for the GUI."""

    layout = layout_window1()

    # Window is created.
    window = sg.Window("Blink Calibrator", layout,
                       size=(400, 300),
                       auto_size_text=True,
                       background_color='light grey',
                       finalize=True)

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
                create_window_two()
                break

