# import json
# import os
# from core.audio_processing import Processing
# import numpy as np
# from load import Load
#
# class Training(Processing):
#     def __init__(self, audio, title, sr):
#         super().__init__(audio, title, sr)
#         self.file_path = "TuneTrack/hashed_data.json"
#         self.save_hash_to_file()
#
#     def save_hash_to_file(self):
#         audio_hash = self.compute_hash(self.feature_vector)
#         spectro_hash = self.compute_hash(np.mean(self.spectrogram, axis=1))
#         new_data = {
#             "title": self.title,
#             "specrogram": spectro_hash,
#             "zero crossing": self.zero_crossing,
#             "spectral banwidth": self.spectral_bandwidth,
#             "spectral centroid": self.spectral_centroid,
#             "spectral contrast": self.spectral_contrast,
#             "spectral flatness": float(self.spectral_flatness),
#             "mfccs": self.mfccs.tolist(),
#             "features": audio_hash
#         }
#
#         # Check if the file exists
#         if os.path.exists(self.file_path):
#             # Load existing data
#             try:
#                 with open(self.file_path, 'r') as file:
#                     data = json.load(file)
#             except json.JSONDecodeError:
#                 data = []  # If the file is corrupted, start fresh
#         else:
#             data = []  # Create a new list if the file doesn't exist
#
#         # Append the new data
#         data.append(new_data)
#
#         # Save back to the file
#         try:
#             with open(self.file_path, 'w') as file:
#                 json.dump(data, file, indent=4)
#             print(f"{self.title} is successufly saved")
#         except Exception as e:
#             print(f"Failed to save {self.title}: {e}")
#
# # Training
# audio_folder = "TuneTrack/Music"
#
# for filename in os.listdir(audio_folder):
#     file_path = os.path.join(audio_folder, filename)
#     title = os.path.splitext(filename)[0]
#     try:
#         audio, sr = Load(file_path).get_audio_data()
#         training_instance = Training(audio, title, sr)
#     except Exception as e:
#         print(f"Failed to process {title}: {e}")
import json
import os
from core.audio_processing import Processing
import numpy as np
import librosa.display
import matplotlib.pyplot as plt
import imagehash
from PIL import Image
from load import Load
# from spectrogram_processor import SpectrogramProcessor  # Assuming this is the other class

#
# import os
# import json
# import librosa
# import librosa.display
# import matplotlib.pyplot as plt
# from PIL import Image
# # from your_module import Load  # Assuming Load is imported from a module
#
# class Training(Processing):
#     def __init__(self, audio, title, sr):
#         super().__init__(audio, title, sr)
#         # Updated relative paths to handle 'core' beside 'music' folder
#         self.file_path = os.path.join(os.path.dirname(__file__), '..', 'hashed_data3.json')
#         self.spectrogram_image_path = os.path.join(os.path.dirname(__file__), '..', f'{self.title}_spectrogram.png')
#         self.peaks_image_path = os.path.join(os.path.dirname(__file__), '..', f'{self.title}_peaks.png')
#         self.save_hash_to_file()
#
#     def save_hash_to_file(self):
#         # Generate and save the spectrogram image
#         self.save_spectrogram_image()
#
#         # Generate the peak-highlighted image
#         self.save_peaks_image()
#
#         # Create a dictionary to store the relevant data (title, hashes, images)
#         new_data = {
#             "title": self.title,
#             "spectrogram_image": self.spectrogram_image_path,
#             "peaks_image": self.peaks_image_path,
#             "spectrogram_hash": self.hash_hex
#         }
#
#         # Check if the file exists
#         if os.path.exists(self.file_path):
#             # Load existing data
#             try:
#                 with open(self.file_path, 'r') as file:
#                     data = json.load(file)
#             except json.JSONDecodeError:
#                 data = []  # If the file is corrupted, start fresh
#         else:
#             data = []  # Create a new list if the file doesn't exist
#
#         # Append the new data
#         data.append(new_data)
#
#         # Save back to the file
#         try:
#             with open(self.file_path, 'w') as file:
#                 json.dump(data, file, indent=4)
#             print(f"{self.title} successfully saved")
#         except Exception as e:
#             print(f"Failed to save {self.title}: {e}")
#
#     def save_spectrogram_image(self):
#         """ Save the spectrogram as an image. """
#         D_db = librosa.amplitude_to_db(self.spectrogram, ref=np.max)
#         plt.figure(figsize=(10, 4))
#         librosa.display.specshow(D_db, sr=self.sr, x_axis='time', y_axis='log')
#         plt.colorbar(format='%+2.0f dB')
#         plt.title(f'Spectrogram of {self.title}')
#         plt.tight_layout()
#         plt.savefig(self.spectrogram_image_path, bbox_inches='tight')
#         plt.close()
#
#
#     def save_peaks_image(self):
#         """ Save the spectrogram image with peaks highlighted using functions from SpectrogramProcessor. """
#         D_db = librosa.amplitude_to_db(self.spectrogram, ref=np.max)
#         peaks = self.extract_peaks(D_db)  # Using method from SpectrogramProcessor
#
#         # Create the image with peaks and surrounding regions
#         peak_image = self.visualize_peaks(D_db, peaks)  # Using method from SpectrogramProcessor
#
#         # Convert the peak image to an 8-bit format (uint8) and then save it as PNG
#         peak_image_uint8 = np.uint8(np.clip(peak_image, 0, 255))  # Clip values and convert to uint8
#
#         # Convert the peak image to a PIL Image and save it
#         peak_image_pil = Image.fromarray(peak_image_uint8)
#         peak_image_pil.save(self.peaks_image_path)
#
#
# # Training
# audio_folder = os.path.join(os.path.dirname(__file__), '..', 'music')  # Update path to 'music' folder
#
# for filename in os.listdir(audio_folder):
#     file_path = os.path.join(audio_folder, filename)
#     title = os.path.splitext(filename)[0]
#     try:
#         audio, sr = Load(file_path).get_audio_data()
#         training_instance = Training(audio, title, sr)
#     except Exception as e:
#         print(f"Failed to process {title}: {e}")

import json
import os
from core.audio_processing import Processing
import librosa
from load import Load


class Training:
    def __init__(self, audio_folder, file_path):
        """
        Initializes the Training class and processes all audio files in the folder.

        :param audio_folder: Path to the folder containing audio files.
        :param file_path: Path to the JSON file where hashes will be saved.
        """
        self.audio_folder = audio_folder
        self.file_path = file_path
        self.process_files()

    def process_files(self):
        """
        Processes all audio files in the given folder and saves their perceptual hashes.
        """
        # Check if the file exists
        if os.path.exists(self.file_path):
            # Load existing data
            try:
                with open(self.file_path, 'r') as file:
                    data = json.load(file)
            except json.JSONDecodeError:
                data = []  # If the file is corrupted, start fresh
        else:
            data = []  # Create a new list if the file doesn't exist

        # Process each audio file in the folder
        for filename in os.listdir(self.audio_folder):
            file_path = os.path.join(self.audio_folder, filename)
            title = os.path.splitext(filename)[0]

            try:
                # Load audio data
                audio, sr = librosa.load(file_path, sr=None)

                # Create an instance of Processing to get the hash
                audio_processing = Processing(audio=audio, title=title, sr=sr)

                # Create a new entry with the title and hash
                new_data = {
                    "title": title,
                    "spectrogram_hash": audio_processing.get_hashed_features()
                }

                # Append new data to the list
                data.append(new_data)

                print(f"Processed {title} successfully")

            except Exception as e:
                print(f"Failed to process {title}: {e}")

        # Save the hashes to the file
        self.save_hashes_to_file(data)

    def save_hashes_to_file(self, data):
        """
        Saves the perceptual hashes to a JSON file.

        :param data: List of dictionaries containing titles and hashes.
        """
        try:
            with open(self.file_path, 'w') as file:
                json.dump(data, file, indent=4)
            print(f"Hashes saved successfully to {self.file_path}")
        except Exception as e:
            print(f"Failed to save hashes: {e}")


# Usage example:
audio_folder = os.path.join(os.path.dirname(__file__), '..', 'Music')  # Path to the music folder
file_path = os.path.join(os.path.dirname(__file__), '..', 'hashed_data4.json')  # Path to save hashes

# Create an instance of Training and process all files in the audio folder
training_instance = Training(audio_folder, file_path)
