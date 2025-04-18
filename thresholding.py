def get_threshold_from_evoked(
        evoked,
        channel,
        fs=256,
        tmin=0.25,
        tmax=0.4,
        margin=50
):
    """Calculates the average threshold for an EEG channel
    in an evoked waveform.

    Args:
        channel (str):
    Returns:
        float: a real-time detection threshold."""

    # Gets the channel index
    ch_index = evoked.ch_names.index(channel)

    # Creates a 2D NumPy array with the shape
    # (n_channels, n_samples)
    signal = evoked.data[ch_index]

    # Converts time in seconds to sample index
    start_sample = int((tmin + 0.5) * fs)
    end_sample   = int((tmax + 0.5) * fs)

    # Slices the time window from the signal
    post_cue = signal[start_sample:end_sample]

    # Finds the lowest voltage value
    # with a +50 uV safety margin
    return post_cue.min() + margin