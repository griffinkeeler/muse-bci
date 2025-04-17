import mne
import numpy as np
import pandas as pd

# Configuration
fs = 256 # Sampling rate in Hz
tmin = -0.5 # Seconds before blink cue
tmax = 1.0 # Seconds after blink cue
channel_names = ['TP9', 'AF7', 'AF8', 'TP10'] # Muse EEG Channels

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
cue_sample_indices = [np.argmin(np.abs(eeg_timestamps - t)) for t in cue_times]

# Create MNE-compatible events array: [sample_index, 0, event_id]
# At these sample indices, a blink event happened
events = np.array([[idx, 0, 1] for idx in cue_sample_indices])

# Create the MNE Info object (metadata about EEG channels)
info = mne.create_info(
    ch_names=channel_names,
    sfreq=fs,
    ch_types='eeg'
)

# Create the Raw object from EEG data
data = eeg_df[channel_names].to_numpy().T # shape: (n_channels, n_samples)
raw = mne.io.RawArray(data, info)

# Create the Epochs object around each blink cue
epochs = mne.Epochs(
    raw,                    # EEG recordings
    events,                 # blink cue event array
    event_id=1,             # event code for blink
    tmin=tmin,              # start time relative to cue
    tmax=tmax,              # end time relative to cue
    baseline=(None, 0),     # baseline correct from beginning to cue
    preload=True,           # load all data into memory for fast access
    event_repeated='drop',   # drop repeated sample indices
    reject=None             # disables automatic rejection

)

# Plot the Epochs
evoked = epochs.average()
evoked.plot()
