import pandas as pd
from eeg_filters import bandpass_filter

def filter_eeg_csv(input_path,
                   output_path, fs=256.0):
    """Filters a csv file with raw EEG data using the bandpass
    filter and outputs a new csv file with the filtered data."""
    df = pd.read_csv(input_path)

    # Applies the bandpass filter to each column
    for ch in ['TP9', 'AF7', 'AF8', 'TP10']:
        df[ch] = bandpass_filter(df[ch], fs=fs)

    # Saves the filtered data to a csv file
    df.to_csv(output_path, index=False)

