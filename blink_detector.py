
def detect_blink_from_evoked(evoked, channel='TP10', threshold=-200, fs=256, tmin=0.0, tmax=0.2):
    """Detects blinks from an averaged Evoked object from MNE.
    Returns True if the threshold is passed,
    otherwise returns False."""
    # Get the channel index
    ch_index = evoked.ch_names.index(channel)

    # Extract the signal from the epoch window
    signal = evoked.data[ch_index]

    # Convert time window to sample indices
    start_sample = int((tmin + 0.5) * fs)
    end_sample = int((tmax + 0.5) * fs)

    # Slice the signal after the green dot cue
    post_cue = signal[start_sample:end_sample]

    # Check for a large negative deflection
    # Returns True if threshold is passed
    # Returns False if threshold is not passed
    return post_cue.min() < threshold

def detect_blink_from_buffer(buffer, threshold, channel_index=3, fs=256, window_s=0.2):
    """Detects blinks from a live buffer in the last 'window_s' seconds"""

    # Converts the window_s to samples
    # 256 * 0.2 = 51 samples
    window_size = int(window_s * fs)

    # Grabs the last window_size samples from selected EEG channel
    signal = buffer[channel_index, -window_size:]

    # Returns the lowest value in the signal chunk
    return signal.min() < threshold