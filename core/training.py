import json
import os
from TuneTrack.core.audio_processing import Processing
import numpy as np
from load import Load

class Training(Processing):
    def __init__(self, audio, title, sr):
        super().__init__(audio, title, sr)
        self.file_path = "TuneTrack/hashed_data.json"
        self.save_hash_to_file()

    def save_hash_to_file(self):
        audio_hash = self.compute_hash(self.feature_vector)
        spectro_hash = self.compute_hash(np.mean(self.spectrogram, axis=1))
        new_data = {
            "title": self.title,
            "specrogram": spectro_hash,
            "zero crossing": self.zero_crossing,
            "spectral banwidth": self.spectral_bandwidth,
            "spectral centroid": self.spectral_centroid,
            "spectral contrast": self.spectral_contrast,
            "spectral flatness": float(self.spectral_flatness),
            "mfccs": self.mfccs.tolist(),
            "features": audio_hash
        }

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

        # Append the new data
        data.append(new_data)

        # Save back to the file
        try:
            with open(self.file_path, 'w') as file:
                json.dump(data, file, indent=4)
            print(f"{self.title} is successufly saved")
        except Exception as e:
            print(f"Failed to save {self.title}: {e}")

# Training
audio_folder = "TuneTrack/Music"

for filename in os.listdir(audio_folder):
    file_path = os.path.join(audio_folder, filename)
    title = os.path.splitext(filename)[0]
    try:
        audio, sr = Load(file_path).get_audio_data()
        training_instance = Training(audio, title, sr)
    except Exception as e:
        print(f"Failed to process {title}: {e}")
