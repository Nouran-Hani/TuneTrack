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

class AudioPlayerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initializeUI()
        self.connectUI()
        self.initailizeParameters()

    def initailizeParameters(self):
        self.audio1 = None
        self.audio2 = None
        self.audio = None

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
        self.MatchCard1 = ResultCard("2", "Song 2", "Remix", 55)
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
        self.weightSlider.valueChanged.connect(self.updateWeightLabels)
    
    def load_audio1(self):
        self.audio_path1 = self.audioCard1.get_file()
        self.audio1, self.sr1 = Load(self.audio_path1).get_audio_data()
        # print("audio1: ",self.audio1)
        self.processing()
        
    def load_audio2(self):    
        self.audio_path2 = self.audioCard2.get_file()
        self.audio2, self.sr2 = Load(self.audio_path2).get_audio_data()
        # print("audio1: ",self.audio2)
        self.processing()

    def processing(self):
        if self.audio1 is not None and self.audio2 is not None:
            self.audio = self.audio1 + self.audio2
        elif self.audio1 is not None:
            self.audio = self.audio1
        else:
            self.audio = self.audio2
        self.process = Processing(self.audio, title=None)
        self.hashed_features = self.process.get_hashed_features()
        check = SimilarityCheck()
        check.set_hashed_song(self.hashed_features)
        similar = check.get_similarities()
        print(similar)        
    


    def updateWeightLabels(self):
        value = self.weightSlider.value()
        self.audio1Weight.setText(f"{value}")
        self.audio2Weight.setText(f"{100 - value}") 

if __name__ == "__main__":
    app = QApplication([])
    window = AudioPlayerApp()
    window.resize(900, 750)
    window.show()
    app.exec_()
