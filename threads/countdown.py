from time import sleep

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