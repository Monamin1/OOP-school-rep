import sys
import math
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QGridLayout, QLineEdit, QPushButton,
    QVBoxLayout, QMenuBar, QAction, QTextEdit, QMessageBox
)
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.history_file = "history.txt"
        self.initUI()
        self.loadHistory()

    def initUI(self):
        mainLayout = QVBoxLayout()
        grid = QGridLayout()
        self.textLine = QLineEdit(self)
        self.textLine.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.textLine.setReadOnly(True)
        self.textLine.setStyleSheet("font-size: 20px; padding: 10px;")

        menuBar = QMenuBar(self)
        fileMenu = menuBar.addMenu("File")

        clearAction = QAction("Clear", self)
        clearAction.triggered.connect(self.clearDisplay)

        saveAction = QAction("Save History", self)
        saveAction.triggered.connect(self.saveHistoryManually)

        clearHistoryAction = QAction("Clear History", self)
        clearHistoryAction.triggered.connect(self.clearHistory)

        exitAction = QAction("Exit", self)
        exitAction.setShortcut(QKeySequence("Ctrl+Q"))
        exitAction.triggered.connect(self.close)

        fileMenu.addAction(clearAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(clearHistoryAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)

        mainLayout.setMenuBar(menuBar)
        mainLayout.addWidget(self.textLine)

        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('^', 4, 2), ('+', 4, 3),
            ('sin', 5, 0), ('cos', 5, 1), ('C', 5, 2), ('=', 5, 3)
        ]

        for text, row, col in buttons:
            button = QPushButton(text)
            button.setFixedHeight(45)
            button.setStyleSheet("font-size: 16px;")
            button.clicked.connect(self.onButtonClick)
            grid.addWidget(button, row, col)

        mainLayout.addLayout(grid)

        self.historyDisplay = QTextEdit()
        self.historyDisplay.setReadOnly(True)
        self.historyDisplay.setStyleSheet(
            "font-size: 14px; background-color: #f7f7f7; border: 1px solid #ccc;"
        )
        mainLayout.addWidget(self.historyDisplay)

        self.setLayout(mainLayout)

        self.setWindowTitle("Scientific Calculator with History")
        self.setGeometry(300, 200, 400, 500)
        self.show()

    def onButtonClick(self):
        sender = self.sender()
        text = sender.text()

        if text == 'C':
            self.clearDisplay()
        elif text == '=':
            self.evaluateExpression()
        elif text in ('sin', 'cos'):
            self.addTrigFunction(text)
        else:
            current = self.textLine.text()
            self.textLine.setText(current + text)

    def clearDisplay(self):
        self.textLine.clear()

    def addTrigFunction(self, func):
        try:
            expression = self.textLine.text()
            if expression:
                value = eval(expression)
                if func == 'sin':
                    result = math.sin(math.radians(value))
                else:
                    result = math.cos(math.radians(value))
                result = round(result, 6)
                self.textLine.setText(str(result))
                record = f"{func}({value}) = {result}"
                self.updateHistory(record)
        except Exception:
            self.textLine.setText("Error")

    def evaluateExpression(self):
        expression = self.textLine.text()
        try:
            expression = expression.replace('^', '**')
            result = eval(expression)
            record = f"{expression} = {result}"
            self.textLine.setText(str(result))
            self.updateHistory(record)
        except Exception:
            self.textLine.setText("Error")

    def updateHistory(self, record):
        """Append a record to the display and save file"""
        self.historyDisplay.append(record)
        self.saveToFile(record)

    def saveToFile(self, record):
        """Append to history.txt"""
        try:
            with open(self.history_file, "a") as f:
                f.write(record + "\n")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to save history:\n{e}")

    def loadHistory(self):
        """Load previous history from file if exists"""
        if os.path.exists(self.history_file):
            with open(self.history_file, "r") as f:
                content = f.read().strip()
                if content:
                    self.historyDisplay.setText(content)

    def saveHistoryManually(self):
        """Triggered from File > Save History"""
        try:
            with open(self.history_file, "w") as f:
                f.write(self.historyDisplay.toPlainText())
            QMessageBox.information(self, "Saved", "History saved successfully!")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to save history:\n{e}")

    def clearHistory(self):
        """Clear both on-screen and saved history"""
        confirm = QMessageBox.question(
            self,
            "Confirm Clear",
            "Are you sure you want to clear all history?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.historyDisplay.clear()
            try:
                open(self.history_file, "w").close()  # clear file
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to clear history:\n{e}")

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.evaluateExpression()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Calculator()
    sys.exit(app.exec_())
