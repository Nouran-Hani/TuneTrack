from PyQt5.QtCore import Qt, QSize
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
        self.styleUi(songName)

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

        self.mainLayout.addWidget(self.rank, 3)
        self.mainLayout.addWidget(self.cover, 10)
        self.mainLayout.addLayout(cardBody, 20)
        self.mainLayout.addWidget(self.playButton, 5)

        self.setLayout(self.mainLayout)

    def styleUi(self,songName):
        self.mainColor = "#FE7191"
        self.accentColor = "White"
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(f"background-color: #2a2a2a;  border-radius:12px;")

        self.setMinimumWidth(400)
        self.setMaximumWidth(500)
        self.setMaximumHeight(200)

        # Style for the cover button
        self.cover.setMinimumSize(70,70)
        self.cover.setIcon(QIcon(f"Photos/Covers/{songName}.jpeg"))
        self.cover.setIconSize(QSize(100, 100))  # Set icon size to match button width
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
                font-size: 35px;
                border: 1px solid #FF0000;
                padding: 5px;
                border: none;
            }}
        """)
        #
        # self.songName.setStyleSheet(f"""
        #     QLabel {{
        #         color: {self.mainColor};
        #         font-family: 'Roboto';
        #         font-weight: Bold;
        #         font-size: 20px;
        #         padding: 5px;
        #         border: none;
        #     }}
        # """)

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

        self.similarityResult.setStyleSheet(f"""
            QLabel {{
                color: {self.mainColor};
                font-family: 'Roboto';
                font-weight: Bold;
                font-size: 25px;
                border: 1px solid #009688;
                padding: 5px;
                border: none;
            }}
        """)
        self.similarityResult.setAlignment(Qt.AlignRight | Qt.AlignCenter)
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
        self.playButton.setMinimumSize(60,60)
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
        self.playButton.setIconSize(QSize(int(size * 0.3), int(size * 0.3)))




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
            self.timer.start(50)  # Adjust interval for smoother scrolling
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

if __name__ == "__main__":
    app = QApplication([])
    mainWindow = QMainWindow()
    resultCard = ResultCard()
    mainWindow.setCentralWidget(resultCard)
    mainWindow.setWindowTitle("Result Card Demo")
    mainWindow.resize(400, 100)  # You can adjust this as needed
    mainWindow.show()
    app.exec_()
