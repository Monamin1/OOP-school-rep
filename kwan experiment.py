from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, 
                             QComboBox, QDateEdit, QProgressBar, QMenuBar, QMessageBox)

from PyQt6.QtCore import Qt, QDate
import sys



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Manager Lite")
        self.setFixedSize(600, 400)

        self.task = []

        self.create_menu()
        self.setup_ui()

    def create_menu(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)

        reset_menu = menu_bar.addMenu("Reset")
        reset_fuction = reset_menu.addAction("Reset All Entry")
        reset_fuction.triggered.connect(self.reset_entry)

    def setup_ui(self):
        main_layout = QVBoxLayout()

        #input selection
        input_layout = QHBoxLayout()
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Create...")
        add_button = QPushButton("Add")
        add_button.clicked.connect(self.add_task)
        input_layout.addWidget(self.task_input)
        input_layout.addWidget(add_button)

        add_button.clicked.connect(self.reset_entry)

        self.task_table = QTableWidget()
        self.task_table.setColumnCount(4)
        self.task_table.setHorizontalHeaderLabels(["Recipe Name", "Category", "Prep Time", "Last Made ON"])
        self.task_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)


        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.dateChanged.connect(self.set_due_date)

        self.progress_bar = QProgressBar()

        #progress bar
        self.progress_bar = QProgressBar()

        #assemble
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.task_table)
        main_layout.addWidget(self.progress_bar)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def add_task(self):
        task_text = self.task_input.text().strip()
        if task_text:
            row = self.task_table.rowCount()
            self.task_table.insertRow(row)
            self.task_table.setItem(row, 0, QTableWidgetItem(task_text))
            self.task_input.clear()
            self.update_progress()

    def update_status(self):
        row = self.task_table.currentRow()
        if row >= 0:
            new_status = self.status_combo.currentText()
            self.task_table.setItem(row, 1, QTableWidgetItem(new_status))
            self.update_progress()

    def set_due_date(self):
        row = self.task_table.currentRow()
        if row>=0:
            due_date = self.date_edit.date().toString(Qt.DateFormat.ISODate)
            QMessageBox.information(self, "Due Date Set", f"Task due date: {due_date}")

    def update_progress(self):
        total_tasks = self.task_table.rowCount()
        if total_tasks == 0:
            self.progress_bar.setValue(0)
            return
        completed_tasks = sum(1 for i in range(total_tasks) 
                              if self.task_table.item(i, 1).text() == "Completed")
        
        progress = int((completed_tasks / total_tasks) * 100)
        self.progress_bar.setValue(progress)

    def reset_entry(self):
        self.task_input.clear()
        self.status_combo.setCurrentIndex(0)
        self.date_edit.setDate(QDate.currentDate())
        self.progress_bar.setValue(0)
        self.task_table.clearContents()
        self.task_table.setRowCount(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

