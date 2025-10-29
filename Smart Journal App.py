from PyQt6.QtWidgets import(QApplication, QMainWindow, QWidget, QPushButton, QTextEdit,
QLabel, QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox, QStatusBar)
import sys, os
from datetime import datetime
class smartJournalApp(QMainWindow):
    def __init__(self):
        super().__init__()
       
        # Window properties
        self.setWindowTitle("Smart Journal App")
        self.setFixedSize(600,400)
       
        # Widgets
        self.title_label = QLabel("Smart Journal App")
        self.text_area = QTextEdit()
        self.load_button = QPushButton("Load File")      
        self.save_button =  QPushButton("Save File")
        self.clear_button = QPushButton("Clear Text")
       
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
       
        # Layouts
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.clear_button)
       
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.text_area)
        main_layout.addLayout(button_layout)
       
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
       
        # Signal Collection
        self.load_button.clicked.connect(self.load_file)
        self.save_button.clicked.connect(self.save_file)
        self.clear_button.clicked.connect(self.clear_text)
       
       
    def load_file(self):
          try:
              path, _ = QFileDialog.getOpenFileName(self, "Open File", "" , "Text Files (*.txt)")
              if path and os.path.exists(path):
                  with open(path , "r") as file:
                      content = file.read()
                  self.text_area.setPlainText(content)
                  self.status_bar.showMessage(f"Loaded: {os.path.basename(path)}")
              else:
                  self.status_bar.showMessage("No File selected.")
          except Exception as e:
              QMessageBox.warning("Error", f"Cannot Load file: \n {e}")
   
    def save_file(self):
        try:
            journals_folder = "journals_Dueñas"
            if not os.path.exists(journals_folder):
                 os.makedirs(journals_folder)

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_name = f"journal_entry_{timestamp}.txt"
            file_path = os.path.join(journals_folder, file_name)
             
            with open(file_path, "w") as file:
                file.write(self.text_area.toPlainText())
             
            QMessageBox.information(self, "Success", f"Journal Entry Saved!\nFile: {file_name}")
            self.text_area.clear()
            self.status_bar.showMessage(f"Entry saved as: {file_name}")

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to save entry: {e}")      
           
    def clear_text(self):
        self.text_area.clear()
        self.status_bar.showMessage("Text Cleared")
       
       
app = QApplication(sys.argv)
window = smartJournalApp()  
window.show()
app.exec()    