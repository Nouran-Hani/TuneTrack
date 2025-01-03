import librosa
import numpy as np
import scipy.ndimage
import imagehash
from PIL import Image
from PIL.Image import Resampling

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


class Processing:
    def __init__(self, audio, title):
        self.title = title
        self.audio = audio

        self.spectrogram = np.abs(librosa.stft(self.audio, n_fft=4096, hop_length=512))
        self.feature_vector = []
        self.hash_hex = None

        # Compute features
        self.compute_features()

    def compute_features(self):
        D_db = librosa.amplitude_to_db(self.spectrogram, ref=np.max)
        peaks = self.extract_peaks(D_db)
        peak_image = self.visualize_peaks(D_db, peaks)
        self.hash_hex = self.compute_phash(peak_image)

    def extract_peaks(self, D_db, threshold=1,neighborhood_size=25):
        filtered_peaks = scipy.ndimage.maximum_filter(D_db, size=neighborhood_size)
        # Create a binary mask for peaks, where the value equals the local maximum
        peaks = (D_db == filtered_peaks)

        # Apply threshold to remove less significant peaks
        peaks = peaks & (D_db >= threshold)
        return peaks

    def visualize_peaks(self, D_db, peaks, peak_intensity=255, region_size=10,surrounding_intensity=0):

        # Initialize the peak map with zeros
        peak_image = np.zeros_like(D_db)
        # Set the pixels at the detected peaks to the desired intensity
        peak_image[peaks == D_db] = peak_intensity

        # Assign surrounding areas a lower intensity (non-peaks)
        peak_image[peak_image == 0] = surrounding_intensity

        # Create a copy of the peak map to visualize around peaks
        visualized_peak_image = np.copy(peak_image)

        # Set the surrounding pixels to a lower intensity
        for i in range(D_db.shape[0]):
            for j in range(D_db.shape[1]):
                if peak_image[i, j] == 0:  # If it's not already a peak
                    peak_image[i, j] = surrounding_intensity
        for row in range(D_db.shape[0]):
            for col in range(D_db.shape[1]):
                if peak_image[row, col] == peak_intensity:  # If it's a peak
                    # Define the start and end of the region around the peak
                    y_start = max(0, row - region_size)
                    y_end = min(D_db.shape[0], row + region_size)
                    x_start = max(0, col - region_size)
                    x_end = min(D_db.shape[1], col + region_size)

                    # Fill the target region with a fixed intensity (200), keeping the peak as 255
                    visualized_peak_image[y_start:y_end, x_start:x_end] = 200
                    visualized_peak_image[row, col] = peak_intensity  # Ensure the peak remains at the center

        return visualized_peak_image



    def compute_phash(self, peak_image):
        # pil_image = Image.fromarray(peak_image)
        # # pil_image_resized = pil_image.resize((32, 32), Resampling.LANCZOS)  # Resize to 32x32 for consistency
        # # pil_image_grayscale = pil_image_resized.convert("L")  # Convert to grayscale
        # image_array = np.array(pil_image)
        # image_array = np.clip(image_array, 0, 255)  # Ensure pixel values are within the valid range
        #
        # # Convert back to PIL Image after normalization
        # pil_image_normalized = Image.fromarray(image_array)
        #
        # # Compute the perceptual hash of the processed image
        # hash_value = str(imagehash.phash(pil_image_normalized))
        # print("processing class", hash_value)
        # Convert the numpy array to a PIL Image
        pil_image = Image.fromarray(peak_image)

        # Optionally resize the image for consistency (e.g., resizing to 32x32)
        pil_image_resized = pil_image.resize((32, 32), Image.Resampling.LANCZOS)

        # Convert the resized image to grayscale (single channel)
        pil_image_grayscale = pil_image_resized.convert("L")

        # Compute the perceptual hash of the grayscale image
        hash_value = str(imagehash.phash(pil_image_grayscale))
        return hash_value

    def get_hashed_features(self):
        return self.hash_hex



# import librosa

# # Example usage
# audio_file_path = 'TuneTrack/Music/A Thousand Years(instruments).wav'

# # Load the audio file using librosa
# audio, sr = librosa.load(audio_file_path, sr=None)

# # Create an instance of the Processing class with the loaded audio
# audio_processing = Processing(audio=audio, title="A Thousand Years(instruments)", sr=sr)

# # Get the perceptual hash of the spectrogram
# hashed_features = audio_processing.get_hashed_features()

# # Output the hash
# print(f"Perceptual Hash of the Audio's Spectrogram: {hashed_features}")
