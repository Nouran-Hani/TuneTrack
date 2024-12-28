from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar, \
    QPushButton


class ResultCard(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeAttribute()
        self.initializeUI()
        self.connectUI()

    def initializeAttribute(self):
        print(" initializeAttribute Done")

    def initializeUI(self):
        self.createUiElements()
        self.createLayout()
        self.styleUi()
        print(" initializeUi Done")

    def createUiElements(self):
        self.cover = QPushButton()
        self.cover.setIcon(QIcon("Photos/placeholder98.jpeg"))
        self.cover.setIconSize(self.cover.sizeHint())  # Adjust the size of the icon based on button size
        self.cover.setFlat(True)  # Make the button flat so it appears like a label

        self.songName = QLabel("Song Name")
        self.singerName = QLabel("singer lil Name")
        self.similarity = QProgressBar()
        self.playButton = QPushButton(">")
        print(" UI elements created Done")


    def createLayout(self):
        self.mainLayout = QHBoxLayout()
        details = QVBoxLayout()
        details.addWidget(self.songName)
        details.addWidget(self.singerName)
        details.addWidget(self.similarity)

        self.mainLayout.addWidget(self.cover,10)
        self.mainLayout.addLayout(details,30)
        self.mainLayout.addWidget(self.playButton,5)

        self.setLayout(self.mainLayout)


        print(" UI Layout Done")

    def styleUi(self):
        # self.similarity.setOrientation(Qt.Vertical)  # Set orientation to vertical
        self.similarity.setMinimum(0)  # Minimum value
        self.similarity.setMaximum(100)  # Maximum value
        self.similarity.setValue(50)  # passed value

        print(" UI Styled Done")

    def connectUI(self):
        print(" UI Connection Done")

if __name__ == "__main__":
        import sys

        app = QApplication(sys.argv)
        mainWindow = QMainWindow()
        resultCard = ResultCard()  # Create an instance of your custom widget
        mainWindow.setCentralWidget(resultCard)  # Set your widget as the central widget of the main window
        mainWindow.setWindowTitle("Result Card Demo")
        mainWindow.resize(400, 100)  # Adjust the window size as needed
        mainWindow.show()
        sys.exit(app.exec_())


