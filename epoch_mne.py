import mne
import numpy as np
import pandas as pd
from thresholding import get_threshold_from_evoked

def get_info(channels, channel_type, fs=256):
    """
    Args:
        channels (list[str]): Names of the EEG channels.
        channel_type (str): The type of channel (e.g. eeg).
        fs (int, optional): Sampling rate, or frequency of channels.
    Returns:
        mne.Info: An Info object containing information about the channels.
    """
    return mne.create_info(
        ch_names=channels,
        sfreq=fs,
        ch_types=channel_type
    )

def get_epochs(data,
               info,
               cue_sample_indices,
               tmin=-0.5,
               tmax=1.0,
               ):
    """
    Args:
        data (np.ndarray): EEG data array with shape (n_channels,
         n_samples)

        info (mne.Info): Info object describing the EEG data
         (channel names, frequency, channel types, etc.).

        cue_sample_indices (List[int]): List of sample indices where
         blink cues occurred.

        tmin (float, optional): Time (in seconds) before each event.
         Default is -0.5.

        tmax (float, optional): Time (in seconds) after each event.
         Default is 1.0.
    Returns:
        mne.Epochs: An Epochs object containing epochs around
         each blink cue.
    """

    # Create the Raw object from EEG data
    raw = mne.io.RawArray(data, info)

    # Create MNE-compatible events array: [sample_index, 0, event_id]
    # At these sample indices, a blink event happened
    events = np.array([[idx, 0, 1] for idx in cue_sample_indices])

    # Create the Epochs object around each blink cue
    return mne.Epochs(
        raw,  # EEG recordings
        events,  # blink cue event array
        event_id=1,  # event code for blink
        tmin=tmin,  # start time relative to cue
        tmax=tmax,  # end time relative to cue
        baseline=(None, 0),  # baseline correct from beginning to cue
        preload=True,  # load all data into memory for fast access
        event_repeated='drop',  # drop repeated sample indices
        reject=None  # disables automatic rejection

    )

def get_blink_threshold():
    """
    Returns:
        float: A threshold based on the average wave forms
        from an evoked potential.
    """
    channel_names = ['TP9', 'AF7', 'AF8', 'TP10']

    # Load EEG data from CSV
    eeg_df = pd.read_csv('filtered_eeg_data.csv')
    # Load blink cues from CSV
    cue_df = pd.read_csv('blink_cue_timestamps.csv')

    # Extract EEG timestamps and blink cues
    eeg_timestamps = eeg_df['timestamp'].to_numpy()
    cue_times = cue_df['blink_cue_time'].to_numpy()

    # Convert blink cue timestamps to sample indices
    # For each blink cue, find the index of the EEG sample that occurred
    # closest to that time
    blink_sample_indices = [np.argmin(np.abs(eeg_timestamps - t))
                            for t in cue_times]

    muse_info = get_info(channel_names, channel_type='eeg')
    muse_data = eeg_df[channel_names].to_numpy().T

    epochs = get_epochs(data=muse_data, info=muse_info,
                        cue_sample_indices=blink_sample_indices)

    evoked = epochs.average()

    return get_threshold_from_evoked(evoked=evoked, channel='TP10')

if __name__ == "__main__":
    threshold = get_blink_threshold()

