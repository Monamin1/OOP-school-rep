from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QLabel, QVBoxLayout
from PyQt6.QtCore import QSize
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Profile Card")
        self.setFixedSize(QSize(450, 250))
       
        self.greeting_label = QLabel("Welcome!")
        self.name_label = QLabel()
        self.status_label = QLabel()
       
        self.show_profile_button = QPushButton("Show My Profile")
        self.show_profile_button.clicked.connect(self.show_profile)
       
        layout = QVBoxLayout()
        layout.addWidget(self.greeting_label)
        layout.addWidget(self.name_label)
        layout.addWidget(self.status_label)
        layout.addWidget(self.show_profile_button)
       
        container = QWidget()
        container.setLayout(layout)
       
        self.setCentralWidget(container)
       
    def show_profile(self):
        self.name_label.setText("Hello, Ranzel Dueñas")
        self.status_label.setText("Profile loaded")
        self.statusBar().showMessage("Profile loaded successfully!")


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
