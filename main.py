from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
from audio_card_upload import AudioCardUpload
from audio_card_playback import AudioCardPlayback

class AudioPlayerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initializeUI()
        self.connectUI()

    def initializeUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15) 

        upload_layout = QHBoxLayout()
        upload_layout.setSpacing(15)  

        playback_layout = QVBoxLayout()

        self.AudioCard1 = AudioCardUpload("Audio 1")
        self.AudioCard2 = AudioCardUpload("Audio 2")

        upload_layout.addWidget(self.AudioCard1)
        upload_layout.addWidget(self.AudioCard2)

        self.playback_widget = AudioCardPlayback()

        main_layout.addLayout(upload_layout)
        main_layout.addLayout(playback_layout)
        playback_layout.addWidget(self.playback_widget)

        self.setWindowTitle("Shazam")
      

    def connectUI(self):
        self.AudioCard1.upload_button.clicked.connect(
            lambda: self.playback_widget.add_audio(self.AudioCard1)
        )
        self.AudioCard2.upload_button.clicked.connect(
            lambda: self.playback_widget.add_audio(self.AudioCard2)
        )

if __name__ == "__main__":
    app = QApplication([])
    window = AudioPlayerApp()
    window.show()
    app.exec_()
