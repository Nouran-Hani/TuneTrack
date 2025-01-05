from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import Qt
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar, \
    QPushButton
import os
from PyQt5.QtCore import Qt, QUrl, QTimer, QSize 



class ResultCard(QWidget):
    def __init__(self, rank="1", songName="Song Name", singerName="Singer Name", similarity=22,file=None):
        super().__init__()
        self.original_file_name = file  # Store the original filename
        self.display_name = songName 
        self.initializeUI(rank, songName, singerName, similarity)
        self.initializeParameters()
        self.connectUI()

    def initializeParameters(self):
        self.player = QMediaPlayer()
        self.is_playing = False
        self.current_file = None

    def initializeUI(self, rank, songName, singerName, similarity):
        self.createUiElements(rank, songName, singerName, similarity)
        self.createLayout()
        self.styleUi()

    def createUiElements(self, rank, songName, singerName, similarity):
        self.rank = QLabel(rank)
        self.cover = QPushButton()
        self.songName = ScrollingLabel(songName) 
        self.singerName = QLabel(singerName)
        self.similarityBar = QProgressBar()
        self.similarityBar.setMinimum(0)
        self.similarityBar.setMaximum(100)
        self.similarityBar.setValue(similarity)  # passed value
        self.similarityResult = QLabel(f"{similarity}%")
        self.playButton = QPushButton(QIcon("Photos/Button Play.png"), "")

    def createLayout(self):
        self.mainLayout = QHBoxLayout()
        cardBody = QVBoxLayout()
        details = QHBoxLayout()
        songDetails = QVBoxLayout()

        songDetails.addWidget(self.songName)
        songDetails.addWidget(self.singerName)
        songDetails.addStretch()
        details.addLayout(songDetails)
        details.addWidget(self.similarityResult)

        cardBody.addStretch(1)
        cardBody.addLayout(details)
        cardBody.addWidget(self.similarityBar)
        cardBody.addStretch(1)

        # Adjust the proportions of the widgets in the main layout
        self.mainLayout.addWidget(self.rank, 3)
        self.mainLayout.addWidget(self.cover, 10)
        self.mainLayout.addLayout(cardBody, 30)
        self.mainLayout.addWidget(self.playButton, 5)

        self.setLayout(self.mainLayout)

    def styleUi(self):
        self.mainColor = "#FE7191"
        self.accentColor = "White"
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(f"background-color: #2a2a2a;  border-radius:12px;")

        self.setMinimumWidth(400)
        self.setMaximumHeight(200)

        # Style for the cover button
        self.cover.setStyleSheet("""
            QPushButton {
                background-color: White;
                border: 1px solid #405159;
                border-radius: 10px;
            }
        """)

        # Style for rank label
        self.rank.setAlignment(Qt.AlignCenter)
        self.rank.setStyleSheet(f"""
            QLabel {{
                color: {self.mainColor};
                font-family: 'Roboto';
                font-weight: Bold;
                font-size: 25px;
                border: 1px solid #FF0000;
                padding: 5px;
                border: none;
            }}
        """)

        # Style for song name label
        self.songName.setStyleSheet(f"""
            QLabel {{
                color: {self.mainColor};
                font-family: 'Roboto';
                font-weight: Bold;
                font-size: 20px;
                padding: 5px;
                border: none;
            }}
        """)

        # Style for singer name label
        self.singerName.setStyleSheet(f"""
            QLabel {{
                color: {self.accentColor};
                font-family: 'Roboto';
                font-weight: bodld;
                font-size: 12px;
                padding: 5px;
                border: none;
            }}
        """)

        # Style for similarity result label
        self.similarityResult.setStyleSheet(f"""
            QLabel {{
                color: {self.accentColor};
                font-family: 'Roboto';
                font-weight: semiBold;
                font-size: 25px;
                border: 1px solid #009688;
                padding: 5px;
                border: none;
            }}
        """)

        # Align similarity result to the right
        self.similarityResult.setAlignment(Qt.AlignRight | Qt.AlignCenter)

        # Style for similarity progress bar
        self.similarityBar.setStyleSheet(f"""
            QProgressBar {{
                min-height: 12px;
                max-height: 12px;
                border-radius: 6px;
                border: 1px solid {self.mainColor};
                background-color: White;
            }}
            QProgressBar::chunk {{
                border-radius: 6px;
                background-color: #FE7191;
            }}
        """)

        self.similarityBar.setFormat("")  # Remove the text from the QProgressBar
        self.playButton.setFlat(True)
        self.playButton.setStyleSheet("border: none;")


    def connectUI(self):
        self.playButton.clicked.connect(self.toggle_playback)
        self.player.stateChanged.connect(self.on_state_changed)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = self.cover.width()  # Use width as the reference to adjust the size
        self.cover.setFixedSize(size, size)
        self.cover.setIconSize(QSize(size, size))
        self.playButton.setFixedSize(int(size * 0.75), int(size * 0.75))
        self.playButton.setIconSize(QSize(int(size * 0.3), int(size * 0.3)))



    def on_state_changed(self, state):
        if state == QMediaPlayer.PlayingState:
            self.is_playing = True
        else:
            self.is_playing = False

    def stop_playback(self):
        if self.player:
            self.player.stop()
            self.is_playing = False
            self.playButton.setIcon(QIcon("Photos/Button Play.png"))
    
    def toggle_playback(self):
        # Stop all other cards' playback
        main_window = self.window()
        if hasattr(main_window, 'stop_all_cards_except'):
            main_window.stop_all_cards_except(self)

        # Construct the full path for the audio file
        base_path = "Music/"
        file_name = self.original_file_name
        extensions = ['.wav']
        found = False

        for ext in extensions:
            full_path = os.path.join(base_path, file_name + ext)  # Combine path, file name, and extension
            if os.path.exists(full_path):
                if self.current_file != full_path:
                    self.current_file = full_path
                    self.player.setMedia(QMediaContent(QUrl.fromLocalFile(full_path)))
                found = True
                break

        if not found:
            print(f"Could not find audio file: {file_name}")
            return

        # Toggle playback
        if self.is_playing:
            self.player.pause()
            self.is_playing = False
            self.playButton.setIcon(QIcon("Photos/Button Play.png"))
        else:
            self.player.play()
            self.is_playing = True
            self.playButton.setIcon(QIcon("Photos/Button Pause.png"))




    def updateCard(self, rank=None, songName=None, singerName=None, similarity=None, file=None, cover_path=None):
        self.stop_playback()
        if rank is not None:
            self.rank.setText(str(rank))
        if songName is not None:
            self.original_file_name = file  # Store the original filename
            self.display_name = songName 
            self.songName.updateText(songName)
            if cover_path is not None:
                self.cover.setIcon(QIcon(cover_path))
        if singerName is not None:
            self.singerName.setText(singerName)
        if similarity is not None:
            self.similarityBar.setValue(similarity)
            self.similarityResult.setText(f"{similarity}%")




from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QLabel

class ScrollingLabel(QLabel):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.fullText = text
        self.offset = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.scrollText)
        self.setStyleSheet("""
            QLabel {
                color: #FE7191;
                font-family: 'Roboto';
                font-weight: Bold;
                font-size: 20px;
                padding: 5px;
                border: none;
                overflow: hidden;
            }
        """)
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

    def enterEvent(self, event):
        """Start scrolling when the mouse hovers over the label."""
        if self.fontMetrics().width(self.fullText) > self.width():  # Only scroll if the text is wider
            self.offset = 0  # Reset offset
            self.timer.start(150)  # Adjust interval for smoother scrolling
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Stop scrolling and reset the text when the mouse leaves."""
        self.timer.stop()
        self.setText(self.fullText)  # Reset text to original
        super().leaveEvent(event)

    def scrollText(self):
        """Animate the text by updating the displayed portion."""
        if self.fontMetrics().width(self.fullText) > self.width():  # Check if scrolling is needed
            self.offset += 1
            if self.offset > len(self.fullText):
                self.offset = 0  # Reset offset to loop the text
            visibleText = self.fullText[self.offset:] + " " + self.fullText[:self.offset]
            self.setText(visibleText)

    def updateText(self, new_text):
        """Update the text and restart scrolling if necessary."""
        self.fullText = new_text
        self.setText(self.fullText)  # Update the label's text
        if self.fontMetrics().width(self.fullText) > self.width():  # Only start scrolling if the text is wide enough
            self.offset = 0  # Reset offset
            self.timer.start(50)  # Restart scrolling

if __name__ == "__main__":
    app = QApplication([])
    mainWindow = QMainWindow()
    resultCard = ResultCard()
    mainWindow.setCentralWidget(resultCard)
    mainWindow.setWindowTitle("Result Card Demo")
    mainWindow.resize(400, 100)
    mainWindow.show()
    app.exec_()
