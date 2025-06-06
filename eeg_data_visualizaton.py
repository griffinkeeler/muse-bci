import pandas as pd
import matplotlib.pyplot as plt

def plot_eeg_csv(filepath):
    """Plots EEG data from a csv file"""
    df = pd.read_csv(filepath)

    timestamps = df['timestamp']
    channels = ['TP9', 'AF7', 'AF8', 'TP10']

    plt.figure(figsize=(12, 6))
    for ch in channels:
        plt.plot(timestamps, df[ch], label=ch)

    plt.title("EEG Signal Over Time")
    plt.xlabel("Timestamp (s)")
    plt.ylabel("Voltage (uV)")
    plt.legend()
    plt.show()


def main():
    plot_eeg_csv('/Users/griffinkeeler/PycharmProjects/muse-bci/filtered_eeg_data.csv')

if __name__ == "__main__":
    main()