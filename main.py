from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, \
    QSpacerItem, QSlider, QSpinBox
from gui.audio_card_upload import AudioCardUpload
from gui.audio_card_playback import AudioCardPlayback
from gui.Results import ResultCard
from gui.style import weightSlider,logo,slogan,bestMatchLabel,NumberLabelPink,NumberLabelWhite
from core.load import Load
from core.audio_processing import Processing
from core.table import SimilarityCheck
import re

class TuneTrackApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("What's The Song!")
        self.initializeUI()
        self.connectUI()
        self.initailizeParameters()

    def initailizeParameters(self):
        self.audio1 = None
        self.audio2 = None
        self.audio = None
        self.updateSliderBasedOnUploads()

    def initializeUI(self):
        self.createUiElements()
        self.createLayout()
        self.styleUi()

    def createUiElements(self):
        self.logo = QLabel("WTS")
        self.slogan = QLabel("|What's The Song!")

        self.audioCard1 = AudioCardUpload("Audio 1")
        self.audioCard2 = AudioCardUpload("Audio 2")


        self.weightSlider = QSlider(Qt.Horizontal)
        self.audio1Weight = QLabel("50")
        self.audio2Weight = QLabel("50")
        self.weightSlider.setMinimum(0)
        self.weightSlider.setMaximum(100)
        self.weightSlider.setValue(50)


        self.playback_widget = AudioCardPlayback()

        self.bestMatchLabel = QLabel("Best Match")
        # should be in function
        self.bestMatchCard = ResultCard("1", "Song 1", "Remix", 55)
        self.MatchCard1 = ResultCard("2", "JSJ 2", "Remix", 40)
        self.MatchCard2 = ResultCard("3", "Song 3", "Remix", 30)
        self.MatchCard3 = ResultCard("4", "Song 4", "Remix", 25)
        self.MatchCard4 = ResultCard("5", "Song 5", "Remix", 10)

    def updateResults(self, song_similarity_data):

        def parse_song_name(song_file_name):
           
            type_keywords = {
                'vocals': 'Vocals',
                'lyrics': 'Vocals',
                'instrument': 'Instruments',
                'instruments': 'Instruments',
                'music': 'Instruments',
                'full': 'Full',
                'original': 'Full'
            }

            # Handle square brackets format
            bracket_match = re.search(r"\[\s*(music|vocals|instrument|instruments|lyrics)\s*\]", song_file_name, re.IGNORECASE)
            if bracket_match:
                raw_type = bracket_match.group(1).strip().lower()
                song_type = type_keywords.get(raw_type, "Full")
                return song_file_name.strip(), song_type

            # Handle underscore format 
            underscore_match = re.match(r"^.+_([^[\]]+)$", song_file_name)
            if underscore_match:
                raw_type = underscore_match.group(1).strip().lower()
                song_type = type_keywords.get(raw_type, "Full")
                return song_file_name.strip(), song_type

            # Handle parentheses format
            paren_match = re.match(r"(.+?)\(\s*(.+?)\s*\)(?:.*)?", song_file_name, re.IGNORECASE)
            if paren_match:
                song_name = paren_match.group(1).strip()
                raw_type = paren_match.group(2).strip().lower()
                song_type = type_keywords.get(raw_type, "Full")
                return song_name + f" ({raw_type})", song_type

            return song_file_name.strip(), "Full"


        """Update the result cards with new song similarity data."""
        # Loop through the array of tuples (songName, similarity)
        for idx, (song_file_name, similarity) in enumerate(song_similarity_data):
            song_name, artist = parse_song_name(song_file_name)

            # Update the best match
            if idx == 0:
                self.bestMatchCard.updateCard(rank="1", songName=song_name, singerName=artist, similarity=similarity,file=song_file_name)
            elif idx == 1:
                self.MatchCard1.updateCard(rank="2", songName=song_name, singerName=artist, similarity=similarity,file=song_file_name)
            elif idx == 2:
                self.MatchCard2.updateCard(rank="3", songName=song_name, singerName=artist, similarity=similarity,file=song_file_name)
            elif idx == 3:
                self.MatchCard3.updateCard(rank="4", songName=song_name, singerName=artist, similarity=similarity,file=song_file_name)
            elif idx == 4:
                self.MatchCard4.updateCard(rank="5", songName=song_name, singerName=artist, similarity=similarity,file=song_file_name)

    def stop_all_cards_except(self, active_card):
        """Stop playback on all cards except the active card."""
        for card in [self.bestMatchCard, self.MatchCard1, self.MatchCard2, self.MatchCard3, self.MatchCard4]:
            if card is not active_card:
                card.stop_playback()


    def createLayout(self):
        self.mainLayout = QVBoxLayout()

        logoLayout = QHBoxLayout()
        logoLayout.addWidget(self.logo)
        logoLayout.addWidget(self.slogan)
        logoLayout.addStretch()

        uploadLayout = QHBoxLayout()

        uploadLayout.addWidget(self.audioCard1)
        uploadLayout.addWidget(self.audioCard2)

        weightLayout = QHBoxLayout()
        weightLayout.addWidget(self.audio1Weight)
        weightLayout.addWidget(self.weightSlider)
        weightLayout.addWidget(self.audio2Weight)

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
        self.mainLayout.addSpacerItem(QSpacerItem(20, 10))
        self.mainLayout.addLayout(uploadLayout,5)
        self.mainLayout.addLayout(weightLayout,10)
        self.mainLayout.addLayout(playbackLayout,30)
        self.mainLayout.addWidget(self.bestMatchLabel,3)
        self.mainLayout.addLayout(bestMatchLayout,22)
        self.mainLayout.addLayout(resultsRow,20)

        centralWidget = QWidget()
        centralWidget.setLayout(self.mainLayout)
        self.setCentralWidget(centralWidget)

    def styleUi(self):
        self.setStyleSheet("background-color:#121212;")
        self.weightSlider.setStyleSheet(weightSlider)
        self.logo.setStyleSheet(logo)
        self.slogan.setStyleSheet(slogan)
        self.bestMatchLabel.setAlignment(Qt.AlignCenter)

        self.bestMatchLabel.setStyleSheet(bestMatchLabel)
        self.audio1Weight.setStyleSheet(NumberLabelPink)
        self.audio2Weight.setStyleSheet(NumberLabelWhite)
        self.audio1Weight.setAlignment(Qt.AlignCenter)
        self.audio2Weight.setAlignment(Qt.AlignCenter)
        # print("Style Done")

    def connectUI(self):
        self.audioCard1.upload_button.clicked.connect(
            lambda: self.playback_widget.add_audio(self.audioCard1)
        )
        self.audioCard1.upload_button.clicked.connect(self.load_audio1)

        self.audioCard2.upload_button.clicked.connect(
            lambda: self.playback_widget.add_audio(self.audioCard2)
        )
        self.audioCard2.upload_button.clicked.connect(self.load_audio2)
        self.weightSlider.sliderReleased.connect(self.updateWeightLabels)

    def updateSliderBasedOnUploads(self):
        if self.audio1 is not None and self.audio2 is None:
            slider_value = 100
        elif self.audio1 is None and self.audio2 is not None:
            slider_value = 0
        else:
            slider_value = 50

        self.weightSlider.setValue(slider_value)
        self.updateWeightLabels()

    def load_audio1(self):
        self.audio_path1 = self.audioCard1.get_file()
        self.audio1, self.sr1 = Load(self.audio_path1).get_audio_data()
        # print("audio1: ",self.audio1)
        self.updateSliderBasedOnUploads()
        self.setting_audio()

    def load_audio2(self):
        self.audio_path2 = self.audioCard2.get_file()
        self.audio2, self.sr2 = Load(self.audio_path2).get_audio_data()
        # print("audio1: ",self.audio2)
        self.updateSliderBasedOnUploads()
        self.setting_audio()

    def setting_audio(self):
        if self.audio1 is not None and self.audio2 is not None:
            v1 = int(self.audio1Weight.text())/100
            v2 = int(self.audio2Weight.text())/100
            min_len = min(len(self.audio1), len(self.audio2))
            self.audio = self.audio1[:min_len]*v1 + self.audio2[:min_len]*v2
        elif self.audio1 is not None:
            self.audio = self.audio1
        else:
            self.audio = self.audio2
        # self.processing()

    def processing(self):
        self.process = Processing(self.audio, title=None)
        self.hashed_features = self.process.get_hashed_features()
        check = SimilarityCheck()
        check.set_hashed_song(self.hashed_features)
        similar = check.get_similarities() # integrate with the results
        self.updateResults(similar)
        print(similar)

    def updateWeightLabels(self):
        value = self.weightSlider.value()
        self.audio1Weight.setText(f"{value}")
        self.audio2Weight.setText(f"{100 - value}")
        if self.audio1 is not None or self.audio2 is not None:
            self.setting_audio()
            self.processing()


if __name__ == "__main__":
    app = QApplication([])
    window = TuneTrackApp()
    window.resize(900, 750)
    window.show()
    app.exec_()
