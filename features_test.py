import librosa
import numpy as np
import librosa.display

class AudioFeatures:
    def __init__(self, audio_path):
        """
        Initializes the AudioFeatures class and computes various features.
        
        :param audio_path: Path to the audio file.
        """
        self.audio_path = audio_path
        self.x, self.sr = librosa.load(audio_path)
        
        # Initialize feature variables
        self.zero_crossing = 0
        self.spectral_bandwidth = 0
        self.spectral_centroid = 0
        self.spectral_contrast = 0
        self.spectral_flatness = 0
        self.mfccs = []

        # Compute features
        self.compute_features()

    def compute_features(self):
        """
        Compute and store various audio features.
        """
        self.zero_crossing = sum(librosa.zero_crossings(self.x, pad=False))
        self.spectral_bandwidth = np.mean(librosa.feature.spectral_bandwidth(y=self.x, sr=self.sr))
        self.spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=self.x, sr=self.sr))
        self.spectral_contrast = np.mean(librosa.feature.spectral_contrast(y=self.x, sr=self.sr))
        self.spectral_flatness = np.mean(librosa.feature.spectral_flatness(y=self.x))
        self.mfccs = np.mean(librosa.feature.mfcc(y=self.x, sr=self.sr), axis=1)  # Averaged across time

# List of audio file paths
audio_paths = [
    r'C:\Users\HP\OneDrive\Documents\GitHub\TuneTrack\Music\Group1_Save-your-tears(instruments).wav',
    r'C:\Users\HP\OneDrive\Documents\GitHub\TuneTrack\Music\Group1_Save-your-tears(lyrcis).wav',
    r'C:\Users\HP\OneDrive\Documents\GitHub\TuneTrack\Music\Group1_Save-your-tears(original).wav'
]

# Create AudioFeatures objects for each audio file and print their features
for audio_path in audio_paths:
    audio_features = AudioFeatures(audio_path)
    audio_features.print_features()
