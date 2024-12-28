from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar, QPushButton


class ResultCard(QWidget):
    def __init__(self,rank = "1", songName = "Song Name" , singerName = "singer Name", similarity = 22):
        super().__init__()
        self.initializeUI( rank, songName  , singerName , similarity)
        self.connectUI()

    def initializeUI(self, rank , songName  , singerName , similarity):
        self.createUiElements(rank, songName  , singerName , similarity)
        self.createLayout()
        self.styleUi()
        print(" initializeUi Done")

    def createUiElements(self,rank,songName  , singerName , similarity):
        self.rank = QLabel(rank)
        self.cover = QPushButton()
        self.songName = QLabel(songName)
        self.singerName = QLabel(singerName)
        self.similarityBar = QProgressBar()
        self.similarityBar.setMinimum(0)
        self.similarityBar.setMaximum(100)
        self.similarityBar.setValue(similarity)  # passed value
        self.similarityResult = QLabel(f"{similarity}%")
        self.playButton = QPushButton(QIcon("Photos/Button Play.png"),"")
        print(" UI elements created Done")

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

        cardBody.addLayout(details)
        cardBody.addWidget(self.similarityBar)

        self.mainLayout.addWidget(self.rank, 3)
        self.mainLayout.addWidget(self.cover, 10)
        self.mainLayout.addLayout(cardBody, 30)
        self.mainLayout.addWidget(self.playButton, 5)

        self.setLayout(self.mainLayout)

        print(" UI Layout Done")

    def styleUi(self):
        self.mainColor = "red"
        self.accentColor = "blue"

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color:#EFEFEF;")

        self.cover.setStyleSheet("background-color: red;")

        self.rank.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        self.rank.setStyleSheet(f"""
                QLabel {{
                    color: {self.mainColor};
                    font-family: 'Roboto';
                    font-weight: semiBold;
                    font-size: 25px;
                }}
            """)
        self.songName.setStyleSheet(f"""
                QLabel {{
                    color: {self.mainColor};
                    font-family: 'Roboto';
                    font-weight: semiBold;
                    font-size: 20px;
                }}
            """)
        self.singerName.setStyleSheet(f"""
                        QLabel {{
                            color: {self.accentColor};
                            font-family: 'Roboto';
                            font-weight: semiBold;
                            font-size: 12px;
                        }}
                    """)

        self.similarityResult.setStyleSheet(f"""
                        QLabel {{
                            color: {self.accentColor};
                            font-family: 'Roboto';
                            font-weight: semiBold;
                            font-size: 25px;
                        }}
                    """)

        self.similarityResult.setAlignment(Qt.AlignRight | Qt.AlignCenter)


        self.similarityBar.setStyleSheet("""
              QProgressBar {
                  min-height: 12px;
                  max-height: 12px;
                  border-radius: 6px;
                  color:red;
                  background-color:blue;
              }
              QProgressBar::chunk {
                  border-radius: 6px;
                  background-color: #009688;  # Set chunk color
              }
          """)

        self.similarityBar.setFormat("")  # This will remove the text from the QProgressBar
        self.playButton.setFlat(True)

        print(" UI Styled Done")

    def connectUI(self):
        print(" UI Connection Done")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = self.cover.width()  # Use height as the reference
        self.cover.setFixedSize(size, size)
        self.playButton.setFixedSize(int(size*.75), int(size*.75))
        print(" resizeEvent called, cover size adjusted")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    resultCard = ResultCard()
    mainWindow.setCentralWidget(resultCard)
    mainWindow.setWindowTitle("Result Card Demo")
    mainWindow.resize(400, 100)
    mainWindow.show()
    sys.exit(app.exec_())
