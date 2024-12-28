from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel
from audio_card_upload import AudioCardUpload
from audio_card_playback import AudioCardPlayback
from Results import ResultCard

class AudioPlayerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initializeUI()
        self.connectUI()

    def initializeUI(self):
        self.createUiElements()
        self.createLayout()
        self.styleUi()


    def createUiElements(self):
        self.audioCard1 = AudioCardUpload("Audio 1")
        self.audioCard2 = AudioCardUpload("Audio 2")
        self.playback_widget = AudioCardPlayback()

        self.bestMatchCard = ResultCard()
        self.MatchCard1 = ResultCard()
        self.MatchCard2 = ResultCard()
        self.MatchCard3 = ResultCard()
        self.MatchCard4 = ResultCard()

    def createLayout(self):
        self.mainLayout = QVBoxLayout()

        uploadLayout = QHBoxLayout()

        uploadLayout.addStretch()
        uploadLayout.addWidget(self.audioCard1)
        uploadLayout.addWidget(self.audioCard2)
        uploadLayout.addStretch()

        playbackLayout = QHBoxLayout()
        playbackLayout.addWidget(self.playback_widget)

        bestMatchLayout = QHBoxLayout()
        bestMatchLayout.addStretch()
        bestMatchLayout.addWidget(self.bestMatchCard)
        bestMatchLayout.addStretch()

        resultsRow = QHBoxLayout()
        resultsLayout = QGridLayout()
        resultsLayout.addWidget(self.MatchCard1, 0, 0)
        resultsLayout.addWidget(self.MatchCard2, 0, 1)
        resultsLayout.addWidget(self.MatchCard3, 1, 0)
        resultsLayout.addWidget(self.MatchCard4, 1, 1)

        resultsLayout.setHorizontalSpacing(50)

        resultsRow.addStretch()
        resultsRow.addLayout(resultsLayout)
        resultsRow.addStretch()

        self.mainLayout.addLayout(uploadLayout,25)
        self.mainLayout.addLayout(playbackLayout,25)
        self.mainLayout.addLayout(bestMatchLayout,25)
        self.mainLayout.addLayout(resultsRow,20)

        centralWidget = QWidget()
        centralWidget.setLayout(self.mainLayout)
        self.setCentralWidget(centralWidget)



    def styleUi(self):
        print("Style Done")

    def connectUI(self):
        self.audioCard1.upload_button.clicked.connect(
            lambda: self.playback_widget.add_audio(self.AudioCard1)
        )
        self.audioCard2.upload_button.clicked.connect(
            lambda: self.playback_widget.add_audio(self.AudioCard2)
        )

if __name__ == "__main__":
    app = QApplication([])
    window = AudioPlayerApp()
    window.show()
    app.exec_()
