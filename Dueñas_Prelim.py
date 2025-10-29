from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
QHBoxLayout, 
QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, 
QComboBox, QDateEdit) 
from PyQt6.QtCore import Qt, QDate 
import sys 

class recipe_organizer(QMainWindow): 
    def __init__(self): 
        super().__init__() 
        self.setWindowTitle("Recipe Organizer") 
        self.setFixedSize(700, 500) 
 
        self.setup_ui() 
 
    def setup_ui(self): 
        main_layout = QVBoxLayout() 
 
        #Input Layout 
        input_layout = QHBoxLayout()
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter...")
        add_button = QPushButton("Add")
        add_button.clicked.connect(self.add_recipe)
        input_layout.addWidget(self.task_input)
        input_layout.addWidget(add_button)


        self.category_combo = QComboBox() 
        self.category_combo.addItems(["Breakfast", "Lunch", "Dinner", "Dessert", "Side", "Other"]) 


        self.date_edit = QDateEdit() 
        self.date_edit.setDate(QDate.currentDate()) 
 
        reset_button = QPushButton("Reset") 
        reset_button.clicked.connect(self.reset_entries) 
 
        input_layout.addWidget(self.task_input) 
        input_layout.addWidget(self.category_combo) 
        input_layout.addWidget(self.date_edit) 
        input_layout.addWidget(add_button) 
        input_layout.addWidget(reset_button) 
 

        self.task_table = QTableWidget() 
        self.task_table.setColumnCount(4) 
        self.task_table.setHorizontalHeaderLabels(["Recipe Name", "Category", "Prep Time", "Last Made On"]) 
        self.task_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers) 
 
 
        main_layout.addLayout(input_layout) 
        main_layout.addWidget(self.task_table) 
 
        container = QWidget() 
        container.setLayout(main_layout) 
        self.setCentralWidget(container) 

        main_layout.addWidget(self.task_table)
 
    def add_recipe(self): 
        task_text = self.task_input.text().strip()
        if task_text:
            row = self.task_table.rowCount()
            self.task_table.insertRow(row)
            self.task_table.setItem(row, 0, QTableWidgetItem(task_text))
            self.task_input.clear()
 
        recipe_name = self.task_table.currentItem() 
        category = self.category_combo.currentText() 
        prep_time = self.date_edit.date().toString(Qt.DateFormat.ISODate) 
        last_made_on = self.date_edit.date().toString(Qt.DateFormat.ISODate)
 
        #basta insert 
        row = self.task_table.rowCount() 
        self.task_table.insertRow(row) 
        self.task_table.setItem(row, 0, QTableWidgetItem(recipe_name)) 
        self.task_table.setItem(row, 1, QTableWidgetItem(category)) 
        self.task_table.setItem(row, 2, QTableWidgetItem(prep_time))
        self.task_table.setItem(row, 3, QTableWidgetItem(last_made_on))

 
        self.task_input.clear() 
 
    def reset_entries(self): 
        self.task_table.setRowCount(0) 
 
 
 
if __name__ == "__main__": 
    app = QApplication(sys.argv) 
    window = recipe_organizer() 
    window.show() 
    sys.exit(app.exec())