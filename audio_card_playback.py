from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSlider, QLabel
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import Qt, QUrl, QTimer, QSize 
from style import cardStyle,circleButton, slider_style, timeLabel
from PyQt5.QtGui import QIcon

class AudioCardPlayback(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeParameters()
        self.initializeUi()
        self.styleUi()

    def initializeParameters(self):
        self.players = []
        self.max_duration = 30000  
        self.timer = QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_progress)
        self.was_playing = False

    def initializeUi(self):
        self.createUIElements()
        self.connectingUI()
    
    def createUIElements(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)  

        self.card_widget = QWidget(self)

        self.card_layout = QVBoxLayout(self.card_widget)
        self.card_layout.setContentsMargins(20, 20, 20, 20) 
        self.card_layout.setSpacing(15)

        self.play_button = QPushButton()
        self.play_button.setIcon(QIcon('Photos/Button Play.png'))  
        self.play_button.setIconSize(QSize(40, 40))
        self.card_layout.addWidget(self.play_button, alignment=Qt.AlignCenter)

        self.progress_layout = QHBoxLayout()
        self.progress_layout.setSpacing(10)

        self.time_label = QLabel("0:00")
        self.progress = QSlider(Qt.Horizontal)
        self.progress.setRange(0, self.max_duration)
        self.duration_label = QLabel("0:30")

        self.progress_layout.addWidget(self.time_label)
        self.progress_layout.addWidget(self.progress)
        self.progress_layout.addWidget(self.duration_label)

        self.card_layout.addLayout(self.progress_layout)

        self.main_layout.addWidget(self.card_widget)

    def connectingUI(self):
        self.play_button.clicked.connect(self.toggle_playback)

    def styleUi(self):
        self.play_button.setStyleSheet(circleButton) 
        self.time_label.setStyleSheet(timeLabel)  
        self.progress.setStyleSheet(slider_style)  
        self.duration_label.setStyleSheet(timeLabel)  
        self.card_widget.setStyleSheet(cardStyle)

    def add_audio(self, uploader):
        file_path = uploader.get_file()
        if file_path:
            self.was_playing = self.timer.isActive()
            
            if uploader.player in self.players:
                self.players.remove(uploader.player)
            
            player = QMediaPlayer()
            player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
            self.players.append(player)
            uploader.connect_player(player)
            
            uploader.audio_replaced.connect(self.restart_playback)
            
            if self.was_playing:
                self.restart_playback()

    def toggle_mute(self, is_muted):
        for player in self.players:
            player.setMuted(is_muted)

    def update_progress(self):
        max_position = max(
            (player.position() for player in self.players if player.state() != QMediaPlayer.StoppedState),
            default=0,
        )
        max_position = min(max_position, self.max_duration)

        self.progress.setValue(max_position)
        self.time_label.setText(self.format_time(max_position))

        if max_position >= self.max_duration:
            self.stop_playback()

    def toggle_playback(self):
        if any(player.state() == QMediaPlayer.PlayingState for player in self.players):
            for player in self.players:
                player.pause()
            self.timer.stop()
            self.was_playing = False
        else:
            current_pos = self.progress.value()
            for player in self.players:
                player.setPosition(current_pos)
                player.play()
            self.timer.start()
            self.was_playing = True
            

    def stop_playback(self):
        for player in self.players:
            player.stop()
        self.timer.stop()
        self.progress.setValue(0)
        self.time_label.setText("0:00")

    def restart_playback(self):
        self.timer.stop()
        for player in self.players:
            player.stop()
        
        self.progress.setValue(0)
        self.time_label.setText("0:00")
        
        for player in self.players:
            player.setPosition(0)
            player.play()
        
        self.timer.start()

    @staticmethod
    def format_time(ms):
        s = ms // 1000
        m = s // 60
        s = s % 60
        return f"{m}:{s:02d}"
