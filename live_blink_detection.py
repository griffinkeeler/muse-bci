from pylsl import StreamInlet, resolve_streams
import numpy as np
import time
from blink_detector import detect_blink_from_buffer

threshold = -178.12139590441942

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

cooldown = 1.0 # seconds between allowed blinks
last_blink_time = 0

print("Start blinking now...")

while True:
    # Grabs the latest sample
    sample, _ = inlet.pull_sample()

    # Shift the buffer left by 1 sample
    buffer[:, :-1] = buffer[:, 1:]

    # Add a new sample to the end of the buffer
    buffer[:, -1] = sample[:4]

    # Check for a blink after cooldown
    current_time = time.time()
    if current_time - last_blink_time > cooldown:
        if detect_blink_from_buffer(buffer, threshold, channel_index=3):
            print("Blink detected!")
            last_blink_time = current_time




