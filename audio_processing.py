import librosa
import numpy as np
import librosa.display
import hashlib

class Processing:
    def __init__(self, audio_path,title):
        """
        Initializes the AudioFeatures class and computes various features.
        
        :param audio_path: Path to the audio file.
        """
        self.audio_path = audio_path
        self.x, self.sr = librosa.load(audio_path)
        self.title=title

        self.spectrogram = np.abs(librosa.stft(self.x, n_fft=1024, hop_length=512))
        
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
        # print("FEATURES FORM SPECTOGRAM")
        self.spectral_bandwidth = np.mean(
            librosa.feature.spectral_bandwidth(S=self.spectrogram, sr=self.sr)
        )
        self.spectral_centroid = np.mean(
            librosa.feature.spectral_centroid(S=self.spectrogram, sr=self.sr)
        )
        self.spectral_contrast = np.mean(
            librosa.feature.spectral_contrast(S=self.spectrogram, sr=self.sr)
        )
        self.spectral_flatness = np.mean(
            librosa.feature.spectral_flatness(S=self.spectrogram)
        )
        self.mfccs = np.mean(
            librosa.feature.mfcc(S=librosa.power_to_db(self.spectrogram**2), sr=self.sr),
            axis=1,
        )

        # debug
    #     self.print_features()
  
    # def print_features(self):
    #     """
    #     Print the computed features in a readable format.
    #     """
    #     print(f"Features for {self.title}:")
    #     print(f"  Spectral Bandwidth: {self.spectral_bandwidth:.2f}")
    #     print(f"  Spectral Centroid: {self.spectral_centroid:.2f}")
    #     print(f"  Spectral Contrast: {self.spectral_contrast:.2f}")
    #     print(f"  Spectral Flatness: {self.spectral_flatness:.2f}")
    #     print(f"  MFCCs: {self.mfccs}")
    #     print()

    def compute_hash(self):
        # Create a flattened array of all features
        feature_vector = [
            self.spectral_bandwidth,
            self.spectral_centroid,
            self.spectral_contrast,
            self.spectral_flatness,
            *self.mfccs,  # Unpack MFCCs into the vector
        ]
        # Normalize the feature vector
        feature_vector = np.array(feature_vector)
        feature_vector = (feature_vector - np.min(feature_vector)) / (np.max(feature_vector) - np.min(feature_vector) + 1e-10)

        # Convert the feature vector to a string and hash it
        feature_string = ",".join(map(str, feature_vector))
        return hashlib.sha256(feature_string.encode('utf-8')).hexdigest()

# List of audio file paths
# audio_paths = ['TuneTrack/Music/Group1_Save-your-tears(instruments).wav']

# audio_titles = ["Instruments"]

# # # Create AudioFeatures objects for each audio file and print their features
# # for audio_path in audio_paths:
# #     audio_features = AudioFeatures(audio_path)
# #     audio_features.print_features()

# # another statement as the one above bas feeha title for debugging
# for audio_path, title in zip(audio_paths, audio_titles):
#     audio_features = Processing(audio_path, title)
#     print(audio_features.compute_hash())
