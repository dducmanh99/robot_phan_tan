from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QFrame
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class ImageApp(QWidget):
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
        self.button1 = QPushButton('Button 1', self)
        self.button2 = QPushButton('Button 2', self)

        # Connect buttons to their functions
        self.button1.clicked.connect(self.onButton1Clicked)
        self.button2.clicked.connect(self.onButton2Clicked)

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

    def onButton1Clicked(self):
        # Functionality for button 1
        try:
            value = float(self.input1.text())
            print(f'Button 1 clicked with value: {value}')
        except ValueError:
            print('Please enter a valid float number in input box 1')

    def onButton2Clicked(self):
        # Functionality for button 2
        try:
            value = float(self.input2.text())
            print(f'Button 2 clicked with value: {value}')
        except ValueError:
            print('Please enter a valid float number in input box 2')

if __name__ == '__main__':
    app = QApplication([])
    ex = ImageApp()
    ex.show()
    app.exec()
