import sys
import random
import matplotlib
matplotlib.use('QtAgg')

from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QFrame
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class RDS_GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set up the layout
        layout = QVBoxLayout()

        # Create input boxes for float numbers
        self.input1 = QLineEdit(self)
        self.input2 = QLineEdit(self)

        # Create buttons
        self.button1 = QPushButton('Start', self)
        self.button2 = QPushButton('Stop', self)
        self.button1.setGeometry(10, 20, 30, 30)
        # Connect buttons to their functions
        # self.button1.clicked.connect(self.onButton1Clicked)
        # self.button2.clicked.connect(self.onButton2Clicked)

        # Create a label to display the image within a frame
        self.imageLabel = QLabel(self)
        self.imageLabel.setContentsMargins(10, 10, 10, 10)
        self.imageLabel.setFixedSize(200, 200)
        self.imageLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        self.pixmap = QPixmap('G:/My Drive/Temas/costmap_navigation/maps/factory.png')  # Replace with your image path
        self.imageLabel.setPixmap(self.pixmap.scaled(200, 200))
        self.imageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Add widgets to the layout
        layout.addWidget(self.input1)
        layout.addWidget(self.input2)
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.imageLabel)

        # Set the layout to the QWidget
        self.setLayout(layout)
app = QtWidgets.QApplication(sys.argv)
w = RDS_GUI()
w.show()
app.exec()