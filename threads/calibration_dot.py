from time import sleep

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
    for i in range(0, 16):
        # Closes the thread if window is closed.
        if i == 0:
            windows.write_event_value(('-THREAD-', '-RED_DOT-'), i)
        else:
            windows.write_event_value(('-THREAD-', '-GREEN_DOT-'), i)
            sleep(0.3)
        for c in range(0, 5):
            windows.write_event_value(('-THREAD-', '-RED_DOT-'), c)
            sleep(1)
        if i == 15:
            windows.write_event_value(('-THREAD-', '-RED_DOT-'), c)
            sleep(3)
            windows.write_event_value(('-THREAD-', '-OPEN_WINDOW_THREE-'), i)