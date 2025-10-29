from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QLabel, QVBoxLayout
from PyQt6.QtCore import QSize, Qt
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        self.setFixedSize(QSize(400, 300))
       
        self.label = QLabel("Hello, welcome to my app!")
        self.button = QPushButton("Click me")
        self.button.clicked.connect(self.button_clicked)
       
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
       
        container = QWidget()
        container.setLayout(layout)
       
        self.setCentralWidget(container)
       
    def button_clicked(self):
        self.label.setText("Button was clicked!")
        self.statusBar().showMessage("You clicked the button")


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()