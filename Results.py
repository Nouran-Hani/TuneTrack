from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar, \
    QPushButton


class ResultCard(QWidget):
    def __init__(self, rank="1", songName="Song Name", singerName="Singer Name", similarity=22):
        super().__init__()
        self.initializeUI(rank, songName, singerName, similarity)
        self.connectUI()

    def initializeUI(self, rank, songName, singerName, similarity):
        self.createUiElements(rank, songName, singerName, similarity)
        self.createLayout()
        self.styleUi()

    def createUiElements(self, rank, songName, singerName, similarity):
        self.rank = QLabel(rank)
        self.cover = QPushButton()
        self.songName = QLabel(songName)
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
        self.mainColor = "red"
        self.accentColor = "blue"
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color: #2d2d2d; border: 2px solid black; border-radius:12px;")

        self.setMinimumWidth(400)
        self.setMaximumHeight(200)

        # Style for the cover button
        self.cover.setStyleSheet("""
            QPushButton {
                background-color: red;
                border: 1px solid #FF0000;
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
                font-weight: semiBold;
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
                font-weight: semiBold;
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
        self.similarityBar.setStyleSheet("""
            QProgressBar {
                min-height: 12px;
                max-height: 12px;
                border-radius: 6px;
                border: 1px solid #EFEFEF;
                background-color: #EFEFEF;
            }
            QProgressBar::chunk {
                border-radius: 6px;
                background-color: #009688;
            }
        """)

        self.similarityBar.setFormat("")  # Remove the text from the QProgressBar
        self.playButton.setFlat(True)
        self.playButton.setStyleSheet("border: none;")

    def connectUI(self):
        # This function can be used to connect any buttons or actions
        print("UI Connection Done")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = self.cover.width()  # Use width as the reference to adjust the size
        self.cover.setFixedSize(size, size)
        self.playButton.setFixedSize(int(size * 0.75), int(size * 0.75))


if __name__ == "__main__":
    app = QApplication([])
    mainWindow = QMainWindow()
    resultCard = ResultCard()
    mainWindow.setCentralWidget(resultCard)
    mainWindow.setWindowTitle("Result Card Demo")
    mainWindow.resize(400, 100)  # You can adjust this as needed
    mainWindow.show()
    app.exec_()
