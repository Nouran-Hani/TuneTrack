import librosa
import numpy as np
import librosa.display
import hashlib
import imagehash
from PIL import Image

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

    def compute_feature_vector(self):
        feature_vector = [
            self.spectral_bandwidth,
            self.spectral_centroid,
            self.spectral_contrast,
            self.spectral_flatness,
            *self.mfccs,  # Unpack MFCCs into the vector
        ]


        return feature_vector
    def compute_hash(self, feature_vector):
        # Create a flattened array of all features
        # feature_vector = [
        #     self.spectral_bandwidth,
        #     self.spectral_centroid,
        #     self.spectral_contrast,
        #     self.spectral_flatness,
        #     *self.mfccs,  # Unpack MFCCs into the vector
        # ]
        # Normalize the feature vector
        feature_vector = np.array(feature_vector)
        feature_vector = (feature_vector - np.min(feature_vector)) / (np.max(feature_vector) - np.min(feature_vector) + 1e-10)

        # Convert the feature vector to a string and hash it
        feature_string = ",".join(map(str, feature_vector))
        return hashlib.sha256(feature_string.encode('utf-8')).hexdigest()


    def compute_perceptual_hash(self):
        """
        Hash the extracted features using perceptual hashing (pHash).
        This method treats the feature vector as an "image" for perceptual hashing.
        """
        feature_vector = self.compute_feature_vector()

        # Reshape the feature vector to make it image-like (e.g., 8x8 grid)
        # You can adjust the shape based on the number of features.
        reshaped_vector = np.array(feature_vector).reshape(8, -1)  # Reshaping into an 8-row grid
        reshaped_vector = np.interp(reshaped_vector, (reshaped_vector.min(), reshaped_vector.max()), (0, 255))

        # Convert the reshaped vector into an image (8xN)
        img = Image.fromarray(reshaped_vector.astype(np.uint8))

        # Use perceptual hash on the image
        phash = imagehash.phash(img)
        return str(phash)

    def save_to_hdf5(self, output_file, h5py=None):
        """
        Save the spectrogram and features to a single HDF5 file.
        """
        with h5py.File(output_file, 'w') as hf:
            # Save the spectrogram as a 2D dataset
            hf.create_dataset('spectrogram', data=self.spectrogram)

            # Save the extracted features as a dataset
            features = self.compute_feature_vector()
            hf.create_dataset('features', data=features)

            # Save the perceptual hash of features
            feature_hash = self.compute_perceptual_hash()
            hf.create_dataset('feature_hash', data=np.string_(feature_hash))


# Example usage
audio_paths = ['Music/Group1_Save-your-tears(instruments).wav']
audio_titles = ["Instruments"]

for audio_path, title in zip(audio_paths, audio_titles):
    audio_features = Processing(audio_path, title)

    # Save everything (spectrogram, features, and hash) to a single HDF5 file
    audio_features.save_to_hdf5(f"{title}_features_and_spectrogram_with_phash.h5")


# # List of audio file paths
# audio_paths = ['Music/Group1_Save-your-tears(instruments).wav']
# 
# audio_titles = ["Instruments"]
# 
# # # # Create AudioFeatures objects for each audio file and print their features
# for audio_path in audio_paths:
#     audio_features = Processing(audio_path,audio_titles).compute_feature_vector()
#     print(audio_features)

# # another statement as the one above bas feeha title for debugging
# for audio_path, title in zip(audio_paths, audio_titles):
#     audio_features = Processing(audio_path, title)
#     print(audio_features.compute_hash())
