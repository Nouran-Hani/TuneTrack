from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, \
    QSpacerItem
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
        self.logo = QLabel("WTS")
        self.slogan = QLabel("|What The Song!")

        self.audioCard1 = AudioCardUpload("Audio 1")
        self.audioCard2 = AudioCardUpload("Audio 2")
        self.playback_widget = AudioCardPlayback()


        self.bestMatchLabel = QLabel("Best Match")
        # should be in function
        self.bestMatchCard = ResultCard()
        self.MatchCard1 = ResultCard("2")
        self.MatchCard2 = ResultCard("3")
        self.MatchCard3 = ResultCard("4")
        self.MatchCard4 = ResultCard("5")

    def createLayout(self):
        self.mainLayout = QVBoxLayout()

        logoLayout = QHBoxLayout()
        logoLayout.addWidget(self.logo)
        logoLayout.addWidget(self.slogan)
        logoLayout.addStretch()

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

        self.mainLayout.addLayout(logoLayout,5)
        self.mainLayout.addSpacerItem(QSpacerItem(20, 40))
        self.mainLayout.addLayout(uploadLayout,20)
        self.mainLayout.addLayout(playbackLayout,25)
        self.mainLayout.addWidget(self.bestMatchLabel,3)
        self.mainLayout.addLayout(bestMatchLayout,22)
        self.mainLayout.addLayout(resultsRow,20)

        centralWidget = QWidget()
        centralWidget.setLayout(self.mainLayout)
        self.setCentralWidget(centralWidget)



    def styleUi(self):
        self.logo.setStyleSheet("""
            QLabel {
                font-family: 'Roboto';
                font-weight: Bold;
                font-size: 50px;
                padding-left: 10px;
                border: none;
            }
        """)
        self.slogan.setStyleSheet("""
            QLabel {
                font-family: 'Roboto';
                font-weight: Bold;
                font-size: 20px;
                border: none;
            }
        """)
        self.bestMatchLabel.setAlignment(Qt.AlignCenter)
        self.bestMatchLabel.setStyleSheet("""
            QLabel {
                font-family: 'Roboto';
                font-weight: Bold;
                font-size: 30px;
                padding: 5px;
                border: none;
            }
        """)

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
