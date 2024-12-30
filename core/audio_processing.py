import librosa
import numpy as np
# import librosa.display

# class Processing:
#     def __init__(self, audio, title, sr):
#         """
#         Initializes the AudioFeatures class and computes various features.
#
#         :param audio_path: Path to the audio file.
#         """
#         self.title=title
#         self.sr = sr
#         self.audio = audio
#
#         self.spectrogram = np.abs(librosa.stft(self.audio, n_fft=1024, hop_length=512))
#
#         # Initialize feature variables
#         self.zero_crossing = 0
#         self.spectral_bandwidth = 0
#         self.spectral_centroid = 0
#         self.spectral_contrast = 0
#         self.spectral_flatness = 0
#         self.mfccs = []
#
#         # Compute features
#         self.compute_features()
#
#     def compute_features(self):
#         """
#         Compute and store various audio features.
#         """
#         # print("FEATURES FORM SPECTOGRAM")
#         self.spectral_bandwidth = np.mean(
#             librosa.feature.spectral_bandwidth(S=self.spectrogram, sr=self.sr)
#         )
#         self.spectral_centroid = np.mean(
#             librosa.feature.spectral_centroid(S=self.spectrogram, sr=self.sr)
#         )
#         self.spectral_contrast = np.mean(
#             librosa.feature.spectral_contrast(S=self.spectrogram, sr=self.sr)
#         )
#         self.spectral_flatness = np.mean(
#             librosa.feature.spectral_flatness(S=self.spectrogram)
#         )
#         self.mfccs = np.mean(
#             librosa.feature.mfcc(S=librosa.power_to_db(self.spectrogram**2), sr=self.sr),
#             axis=1,
#         )
#         self.compute_feature_vector()
#
#     def compute_feature_vector(self):
#         self.feature_vector = [
#             self.spectral_bandwidth,
#             self.spectral_centroid,
#             self.spectral_contrast,
#             self.spectral_flatness,
#             *self.mfccs,  # Unpack MFCCs into the vector
#         ]
#
#     def compute_hash(self, feature_vector):
#         # Normalize the feature vector
#
#         feature_vector = np.array(feature_vector)
#         feature_vector = (feature_vector - np.min(feature_vector)) / (np.max(feature_vector) - np.min(feature_vector) + 1e-10)
#
#         # Simplified perceptual hash: use a binary threshold
#         # Convert normalized feature vector to a binary array
#         median = np.median(feature_vector)
#         binary_vector = (feature_vector > median).astype(int)
#
#         # Convert binary array to a hexadecimal string
#         hash_str = ''.join(map(str, binary_vector))
#         self.hash_hex = f"{int(hash_str, 2):x}"  # Convert binary string to hex
#         return self.hash_hex
#
#     def get_hashed_features(self):
#         self.compute_hash(self.feature_vector)
#         return self.hash_hex

    # def compute_perceptual_hash(self):
    #     """
    #     Hash the extracted features using perceptual hashing (pHash).
    #     This method treats the feature vector as an "image" for perceptual hashing.
    #     """
    #     feature_vector = self.compute_feature_vector()

    #     # Reshape the feature vector to make it image-like (e.g., 8x8 grid)
    #     # You can adjust the shape based on the number of features.
    #     reshaped_vector = np.array(feature_vector).reshape(8, -1)  # Reshaping into an 8-row grid
    #     reshaped_vector = np.interp(reshaped_vector, (reshaped_vector.min(), reshaped_vector.max()), (0, 255))

    #     # Convert the reshaped vector into an image (8xN)
    #     img = Image.fromarray(reshaped_vector.astype(np.uint8))

    #     # Use perceptual hash on the image
    #     phash = imagehash.phash(img)
    #     return str(phash)

#     def save_to_hdf5(self, output_file, h5py=None):
#         """
#         Save the spectrogram and features to a single HDF5 file.
#         """
#         with h5py.File(output_file, 'w') as hf:
#             # Save the spectrogram as a 2D dataset
#             hf.create_dataset('spectrogram', data=self.spectrogram)

#             # Save the extracted features as a dataset
#             features = self.compute_feature_vector()
#             hf.create_dataset('features', data=features)

#             # Save the perceptual hash of features
#             feature_hash = self.compute_perceptual_hash()
#             hf.create_dataset('feature_hash', data=np.string_(feature_hash))


# # Example usage
# audio_paths = ['Music/Group1_Save-your-tears(instruments).wav']
# audio_titles = ["Instruments"]

# for audio_path, title in zip(audio_paths, audio_titles):
#     audio_features = Processing(audio_path, title)

#     # Save everything (spectrogram, features, and hash) to a single HDF5 file
#     audio_features.save_to_hdf5(f"{title}_features_and_spectrogram_with_phash.h5")


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


import librosa
import numpy as np
import scipy.ndimage
import imagehash
from PIL import Image
import matplotlib.pyplot as plt
from PIL.Image import Resampling


class Processing:
    def __init__(self, audio, title, sr):
        """
        Initializes the Processing class and computes various features.

        :param audio: Audio data array.
        :param title: Title of the audio (e.g., song name).
        :param sr: Sampling rate of the audio.
        """
        self.title = title
        self.sr = sr
        self.audio = audio

        # Compute the spectrogram
        self.spectrogram = np.abs(librosa.stft(self.audio, n_fft=1024, hop_length=512))

        # Initialize other feature variables
        self.feature_vector = []
        self.hash_hex = None

        # Compute features
        self.compute_features()

    def compute_features(self):
        """
        Compute and store the spectrogram features and hash.
        """
        # Compute the spectrogram in dB
        D_db = librosa.amplitude_to_db(self.spectrogram, ref=np.max)

        # Detect peaks in the spectrogram
        peaks = self.extract_peaks(D_db)

        # Visualize peaks on the spectrogram
        peak_image = self.visualize_peaks(D_db, peaks)

        # Compute the perceptual hash of the image
        self.hash_hex = self.compute_phash(peak_image)

    def extract_peaks(self, D_db, neighborhood_size=3):
        """
        Extracts peaks using a max filter from the spectrogram.
        :param D_db: The decibel-scaled spectrogram.
        :param neighborhood_size: Size of the neighborhood for peak detection.
        :return: Peaks of the spectrogram.
        """
        # Apply a max filter to detect peaks (local maxima)
        peaks = scipy.ndimage.maximum_filter(D_db, size=neighborhood_size)
        return peaks

    def visualize_peaks(self, D_db, peaks, peak_intensity=255, surrounding_intensity=50):
        """
        Visualize the peaks in the spectrogram by highlighting them with specific intensity levels.
        :param D_db: The spectrogram in decibels.
        :param peaks: The detected peaks.
        :param peak_intensity: Intensity to assign to peak pixels.
        :param surrounding_intensity: Intensity to assign to pixels surrounding the peaks.
        :return: The image representing the spectrogram with peaks.
        """
        # Initialize an empty image for the peak visualization
        peak_image = np.zeros_like(D_db)

        # Normalize values in D_db to a consistent range if needed
        D_db_normalized = np.clip(D_db, -100, 100)  # Clip to ensure within a range

        # Set the pixels at the detected peaks to the desired intensity
        peak_image[peaks == D_db_normalized] = peak_intensity

        # Set the surrounding pixels to a lower intensity
        for i in range(D_db_normalized.shape[0]):
            for j in range(D_db_normalized.shape[1]):
                if peak_image[i, j] == 0:  # If it's not already a peak
                    peak_image[i, j] = surrounding_intensity

        return peak_image

    def compute_phash(self, peak_image):
        """
        Computes the perceptual hash of the spectrogram image.
        :param peak_image: The image of the spectrogram with peaks highlighted.
        :return: A perceptual hash in hexadecimal format.
        """
        # Convert the numpy array to a PIL image
        pil_image = Image.fromarray(peak_image)

        # Resize the image to a fixed size (e.g., 32x32)
        pil_image_resized = pil_image.resize((32, 32), Resampling.LANCZOS)  # Resize to 32x32 for consistency

        # Convert the image to grayscale (L mode)
        pil_image_grayscale = pil_image_resized.convert("L")  # Convert to grayscale

        # Normalize pixel values to a range of 0-255
        image_array = np.array(pil_image_grayscale)
        image_array = np.clip(image_array, 0, 255)  # Ensure pixel values are within the valid range

        # Convert back to PIL Image after normalization
        pil_image_normalized = Image.fromarray(image_array)

        # Compute the perceptual hash of the processed image
        hash_value = str(imagehash.phash(pil_image_normalized))

        return hash_value

    def get_hashed_features(self):
        """
        Return the perceptual hash for this audio's spectrogram.
        """
        return self.hash_hex



import librosa

# Example usage
audio_file_path = 'Music/Group18_RollingInTheDeep_Music.wav'

# Load the audio file using librosa
audio, sr = librosa.load(audio_file_path, sr=None)

# Create an instance of the Processing class with the loaded audio
audio_processing = Processing(audio=audio, title="Test Song", sr=sr)

# Get the perceptual hash of the spectrogram
hashed_features = audio_processing.get_hashed_features()

# Output the hash
print(f"Perceptual Hash of the Audio's Spectrogram: {hashed_features}")
