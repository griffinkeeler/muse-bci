
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