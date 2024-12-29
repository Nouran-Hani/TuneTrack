from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QStyle
from PyQt5.QtCore import pyqtSignal, Qt, QUrl, QTimer, QSize
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from gui.style import cardStyle, songName, uploadButton, circleButton
from PyQt5.QtGui import QIcon


class AudioCardUpload(QWidget):
    mute_toggled = pyqtSignal(bool)
    audio_replaced = pyqtSignal()

    def __init__(self, title: str):
        super().__init__()
        self.title = title
        self.initializeParameters()
        self.createUiElements()
        self.connectingUI()
        self.styleUi()

    def initializeParameters(self):
        self.player = None
        self.is_muted = False
        self.file_path = None 

    def createUiElements(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0) 

        self.card_widget = QWidget(self)
         

        card_layout = QVBoxLayout(self.card_widget)
        card_layout.setContentsMargins(20, 15, 20, 15)  
        card_layout.setSpacing(10)

        header_row = QHBoxLayout()
        self.audio_name_label = QLabel(self.title)
        self.audio_name_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        

        self.upload_button = QPushButton("Upload")
        self.upload_button.setFixedWidth(80)

        self.mute_button = QPushButton()
        self.mute_button.setObjectName("muteButton")
        self.mute_button.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))

        header_row.addWidget(self.audio_name_label)
        header_row.addStretch()
        header_row.addWidget(self.upload_button)
        header_row.addWidget(self.mute_button)

        card_layout.addLayout(header_row)

        main_layout.addWidget(self.card_widget)

    def styleUi(self):
        self.card_widget.setStyleSheet(cardStyle) 
        self.audio_name_label.setStyleSheet(songName)
        self.upload_button.setStyleSheet(uploadButton)   

    def connectingUI(self):
        self.upload_button.clicked.connect(self.upload_audio)
        self.mute_button.clicked.connect(self.toggle_mute)

    def upload_audio(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Upload Audio File", "", "Audio Files (*.mp3 *.wav)"
        )
        if file_name:
            current_file_path = self.file_path
            self.audio_name_label.setText(file_name.split('/')[-1])
            self.file_path = file_name
            
            if self.player:
                self.player.stop()
                self.player.setMedia(QMediaContent(QUrl.fromLocalFile(file_name)))
            
            if current_file_path is not None:
                self.audio_replaced.emit()

    def connect_player(self, player):
        self.player = player
        self.mute_toggled.connect(self.toggle_player_mute)

    def toggle_mute(self):
        self.is_muted = not self.is_muted
        mute_icon = QStyle.SP_MediaVolumeMuted if self.is_muted else QStyle.SP_MediaVolume
        self.mute_button.setIcon(self.style().standardIcon(mute_icon))
        self.mute_toggled.emit(self.is_muted)

    def toggle_player_mute(self, is_muted):
        if hasattr(self, 'player'):
            self.player.setMuted(is_muted)

    def get_file(self):
        return self.file_path
