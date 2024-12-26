from core import Core
import librosa
import librosa.display
import numpy as np
from PIL import Image
import imagehash
import matplotlib.pyplot as plt
import os
import json
import hashlib

class Train(Core):
    def __init__(self, audio_path):
        super().__init__(audio_path=audio_path)
        self.audio_path = audio_path
        self.image_path = "TuneTrack/images/spectro.png"
        self.hashed = {}
        self.datafeatures = []
        self.contrast = None
        self.bandwidth = None
        self.flatness = None
        self.mfccs = None


        self.generate_spectrogram()
        # self.compute_perceptual_hash()
        self.save_hashes()

    def generate_spectrogram(self):
        audio_data, sr = librosa.load(self.audio_path, sr=None)
        spectrogram = np.abs(librosa.stft(audio_data, n_fft=1024, hop_length=512))
        spectrogram_db = librosa.amplitude_to_db(spectrogram, ref=np.max)
        # contrast
        self.contrast = librosa.feature.spectral_contrast(y=spectrogram, sr=sr)
        self.datafeatures.append(self.contrast)
                # Flatten the array and pad or truncate as necessary
        flattened = self.contrast.flatten()
        desired_size = np.prod((513, 1, 40))

        # Pad or truncate to fit the target size
        if flattened.size < desired_size:
            flattened = np.pad(flattened, (0, desired_size - flattened.size), mode='constant')
        elif flattened.size > desired_size:
            flattened = flattened[:desired_size]

        # Reshape to the target shape
        self.contrast = flattened.reshape((513, 1, 40))
        print(self.contrast.shape)

        # flatness
        self.flatness = librosa.feature.spectral_flatness(y=spectrogram)
        self.datafeatures.append(self.flatness)
        print(self.flatness.shape)
        # bandwidth
        self.bandwidth = librosa.feature.spectral_bandwidth(y=spectrogram, sr=sr)
        self.datafeatures.append(self.bandwidth)
        print(self.bandwidth.shape)
        # mfcc
        self.mfccs = librosa.feature.mfcc(y=spectrogram, sr=sr)
        # Flatten the array and pad or truncate as necessary
        flattened = self.mfccs.flatten()
        desired_size = np.prod((513, 1, 40))

        # Pad or truncate to fit the target size
        if flattened.size < desired_size:
            flattened = np.pad(flattened, (0, desired_size - flattened.size), mode='constant')
        elif flattened.size > desired_size:
            flattened = flattened[:desired_size]

        # Reshape to the target shape
        self.mfccs = flattened.reshape((513, 1, 40))
        self.datafeatures.append(self.mfccs)
        print(self.mfccs.shape)

        plt.figure(figsize=(10, 6))
        librosa.display.specshow(spectrogram_db, sr=sr, hop_length=512, x_axis='time', y_axis='log', cmap='viridis')
        plt.axis('off')
        plt.savefig(self.image_path, bbox_inches='tight', pad_inches=0)
        plt.close()
        print("saved spectro")

    def compute_perceptual_hash(self):
        image = Image.open(self.image_path)
        self.hashed[self.image_path] = str(imagehash.phash(image))
        print("compute hash")

    def save_hashes(self):
        feature_vector = np.concatenate((self.contrast, self.bandwidth, self.mfccs, self.flatness), axis=0) 
        feature_hash = hashlib.sha256(feature_vector).hexdigest() 

        with open("TuneTrack/hashed_data.json", "w") as f:
            json.dump({"feature_hash2": feature_hash}, f, indent=4)
            print("saved features, feature hash, and spectrogram hash")


train = Train("TuneTrack/Music/Group1_Save-your-tears(original).wav")
