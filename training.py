import json
import os
from audio_processing import Processing

class Training(Processing):
    def __init__(self, audio_path, title):
        super().__init__(audio_path, title)
        self.file_path = "TuneTrack/hashed_data.json"
        self.save_hash_to_file()

    def save_hash_to_file(self):
        audio_hash = self.compute_hash()
        new_data = {
            "title": self.title,
            "hash": audio_hash
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
            print(f"{self.audio_path} is successufly saved")
        except Exception as e:
            print(f"Failed to save {self.audio_path}: {e}")

# Training
audio_folder = "TuneTrack/Music"

for filename in os.listdir(audio_folder):
    file_path = os.path.join(audio_folder, filename)
    title = os.path.splitext(filename)[0]
    try:
        training_instance = Training(file_path, title)
    except Exception as e:
        print(f"Failed to process {file_path}: {e}")