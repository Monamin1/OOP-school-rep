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

        help_menu = menu_bar.addMenu("Help")
        about_action = help_menu.addAction("About")
        about_action.triggered.connect(lambda: QMessageBox.information(
            self, "About", "Task Manager Lite\nDeveloped by Ranzel Dueñas"
        ))

    def setup_ui(self):
        main_layout = QVBoxLayout()

        #input selection
        input_layout = QHBoxLayout()
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter a new task")
        add_button = QPushButton("Add Task")
        add_button.clicked.connect(self.add_task)
        input_layout.addWidget(self.task_input)
        input_layout.addWidget(add_button)

        self.task_table = QTableWidget()
        self.task_table.setColumnCount(2)
        self.task_table.setHorizontalHeaderLabels(["Task", "Status"])
        self.task_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        #controls
        controls_layout = QHBoxLayout()
        self.status_combo = QComboBox()
        self.status_combo.addItems(["Pending", "In Progress", "Completed"])
        self.status_combo.currentTextChanged.connect(self.update_status)

        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.dateChanged.connect(self.set_due_date)

        controls_layout.addWidget(self.status_combo)
        controls_layout.addWidget(self.date_edit)
        self.progress_bar = QProgressBar()

        #progress bar
        self.progress_bar = QProgressBar()

        #assemble
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.task_table)
        main_layout.addLayout(controls_layout)
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
            self.task_table.setItem(row, 1, QTableWidgetItem("Pending"))
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

