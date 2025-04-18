import turtle
import time
from pylsl import StreamInlet, resolve_streams
import numpy as np
from blink_detector import detect_blink_from_buffer
from epoch_mne import get_threshold

blink_threshold = get_threshold() + 20

print("Blink threshold:", blink_threshold)

# TODO: Get calibrated clench thresholds
draw_clench_threshold = 350
clear_clench_threshold = 600

# Connect to the Muse 2 stream
print("Looking for EEG streams...")
streams = resolve_streams()
eeg_streams = next(s for s in streams if s.type() == 'EEG')
inlet = StreamInlet(eeg_streams)
print("Connected to Muse EEG stream.")

fs = 256 # sampling rate in Hz
buffer_len_sec = 1.5 # length of rolling buffer in seconds
buffer_size = int(fs * 1.5)

# Create an empty 2D buffer: shape = (n_channels, n_samples)
buffer = np.zeros((4, buffer_size))

# Cooldown between events
# The clench cooldown is longer because
# the signal lasts longer than a blink
blink_cooldown = 1.0
clench_cooldown = 2.0

# seconds allowed for two blinks
double_blink_window = 2.0

last_blink_time = 0
last_clench_time = 0

print("Start blinking now...")
print("Threshold:", blink_threshold)

# Mike the turtle
mike = turtle.Turtle()

# Turtle for labelling pen status
label = turtle.Turtle()
label.hideturtle()
label.penup()
label.goto(-200, 200)

double_blink_times = []
clench_times = []

# Tracks the pen state
pen_down = True

while True:
    # Grabs the latest sample
    sample, _ = inlet.pull_sample()

    # Shift the buffer left by 1 sample
    buffer[:, :-1] = buffer[:, 1:]

    # Add a new sample to the end of the buffer
    buffer[:, -1] = sample[:4]

    # Check for a blink after cooldown
    current_time = time.time()
    if current_time - last_blink_time > blink_cooldown:
        if detect_blink_from_buffer(buffer, blink_threshold, channel_index=3):
            double_blink_times.append(current_time)
            last_blink_time = current_time

            # Ensures only the last two blinks are in the list
            if len(double_blink_times) > 2:
                double_blink_times.pop(0)

            # Require at least 0.2 seconds in between blinks
            min_interval = 0.2

            # Check for a double blink in 1 second
            if len(double_blink_times) == 2:
                double_blink_interval = double_blink_times[1] - double_blink_times[0]
                if min_interval < double_blink_interval < 1.3:

                    pen_down = not pen_down

                    label.clear()
                    if pen_down:
                        mike.pendown()
                        label.write("Pen is down")
                    else:
                        mike.penup()
                        label.write("Pen is up")
                    double_blink_times = [] # resets to avoid double detection
                    continue
            mike.right(90)

    # Jaw clench commands
    if current_time - last_clench_time > clench_cooldown:
        window_size = int(0.2 * fs)
        signal = buffer[2, -window_size:]
        clench_value = signal.max()

        # Since the clear threshold is larger than the
        # draw threshold, the clear threshold is the
        # first condition.
        if clench_value > clear_clench_threshold:
            clench_times.append(current_time)
            last_clench_time = current_time
            mike.clear()
        elif clench_value > draw_clench_threshold:
            clench_times.append(current_time)
            last_clench_time = current_time
            mike.forward(100)