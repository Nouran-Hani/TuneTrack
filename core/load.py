import librosa

class Load:
    def __init__(self, audio_path):
        self.audio_path = audio_path
        self.audio, self.sr = librosa.load(audio_path)

    def get_audio_data(self):
        return self.audio, self.sr