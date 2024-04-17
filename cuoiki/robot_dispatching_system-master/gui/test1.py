import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QToolBox


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.button_is_checked = True
        self.setWindowTitle("RDS")
        
        # button = QPushButton("Press Me!")
        # self.setMinimumSize(QSize(200, 200))
        # self.setMaximumSize(QSize(500, 500))
        self.setFixedSize(QSize(300, 200))
        # button.setCheckable(True)
        # button.clicked.connect(self.the_button_was_clicked)
        # button.clicked.connect(self.the_button_was_toggled)
        # button.setChecked(self.button_is_checked)
        self.button = QPushButton("Press Me!")
        self.button.setCheckable(True)
        self.button.released.connect(self.the_button_was_released)
        self.button.setChecked(self.button_is_checked)
        # Set the central widget of the Window.
        self.setCentralWidget(self.button)
    def the_button_was_clicked(self):
        print("Clicked!")
    def the_button_was_toggled(self, checked):
        self.button_is_checked = checked

        print(self.button_is_checked)
    def the_button_was_released(self):
        self.button_is_checked = self.button.isChecked()

        print(self.button_is_checked)

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.setWindowTitle("My App")

#         self.button = QPushButton("Press Me!")
#         self.button.clicked.connect(self.the_button_was_clicked)

#         self.setCentralWidget(self.button)

#     def the_button_was_clicked(self):
#         self.button.setText("You already clicked me.")
#         # self.button.setEnabled(False)

#         # Also change the window title.
#         self.setWindowTitle("My Oneshot App")

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()

# import sys

# from PyQt6.QtCore import Qt
# from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QTextEdit


# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.label = QLabel("Click in this window")
#         self.setCentralWidget(self.label)

#     def mousePressEvent(self, e):
#         if e.button() == Qt.MouseButton.LeftButton:
#             # handle the left-button press in here
#             self.label.setText("mousePressEvent LEFT")

#         elif e.button() == Qt.MouseButton.MiddleButton:
#             # handle the middle-button press in here.
#             self.label.setText("mousePressEvent MIDDLE")

#         elif e.button() == Qt.MouseButton.RightButton:
#             # handle the right-button press in here.
#             self.label.setText("mousePressEvent RIGHT")

#     def mouseReleaseEvent(self, e):
#         if e.button() == Qt.MouseButton.LeftButton:
#             self.label.setText("mouseReleaseEvent LEFT")

#         elif e.button() == Qt.MouseButton.MiddleButton:
#             self.label.setText("mouseReleaseEvent MIDDLE")

#         elif e.button() == Qt.MouseButton.RightButton:
#             self.label.setText("mouseReleaseEvent RIGHT")

#     def mouseDoubleClickEvent(self, e):
#         if e.button() == Qt.MouseButton.LeftButton:
#             self.label.setText("mouseDoubleClickEvent LEFT")

#         elif e.button() == Qt.MouseButton.MiddleButton:
#             self.label.setText("mouseDoubleClickEvent MIDDLE")

#         elif e.button() == Qt.MouseButton.RightButton:
#             self.label.setText("mouseDoubleClickEvent RIGHT")


# app = QApplication(sys.argv)

# window = MainWindow()
# window.show()

# app.exec()

# import sys

# from PyQt6.QtCore import Qt
# from PyQt6.QtGui import QAction
# from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QMenu


# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.show()

#         self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
#         self.customContextMenuRequested.connect(self.on_context_menu)

#     def on_context_menu(self, pos):
#         context = QMenu(self)
#         context.addAction(QAction("test 1", self))
#         context.addAction(QAction("test 2", self))
#         context.addAction(QAction("test 3", self))
#         context.exec(self.mapToGlobal(pos))


# app = QApplication(sys.argv)

# window = MainWindow()
# window.show()

# app.exec()