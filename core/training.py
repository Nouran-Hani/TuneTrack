import json
import os
from audio_processing import Processing
import numpy as np
from load import Load

class Training(Processing):
    def __init__(self, audio, title):
        super().__init__(audio, title)
        self.file_path = "TuneTrack/data/spectrohash.json"
        self.save_hash_to_file()

    def save_hash_to_file(self):
        audio_hash = self.get_hashed_features()
        new_data = {
            "title": self.title,
            "features": audio_hash
        }

        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r') as file:
                    data = json.load(file)
            except json.JSONDecodeError:
                data = []
        else:
            data = [] 

        data.append(new_data)

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
        training_instance = Training(audio, title)
    except Exception as e:
        print(f"Failed to process {title}: {e}")
