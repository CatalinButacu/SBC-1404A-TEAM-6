# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 10:06:56 2024

@authors: Catalin.BUTACU, Serban.VICOL, Nicu.TARADACIUC
"""

import sys
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton
from PyQt5.QtCore import QTimer, QDateTime, QPropertyAnimation, QEasingCurve, pyqtSignal

### ENABLE DISPLAY TO ACTION HISTORY
class ScrollableMessageBox(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.message_queue = []

    def init_ui(self):
        self.setWindowTitle('Scrollable Message Box')

        layout = QVBoxLayout(self)

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)

        # Timer for displaying messages from the queue
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.display_next_message)

        self.load_styles_from_file("UI/styles.qss")

    def load_styles_from_file(self, file_path):
        try:
            with open(file_path, "r") as file:
                style_sheet = file.read()
                self.setStyleSheet(style_sheet)
        except FileNotFoundError:
            print(f"Stylesheet file not found: {file_path}")

    def add_message(self, message):
        current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        self.message_queue.append((current_time, message))
        if not self.timer.isActive():
            self.timer.start(1000)  # Adjust delay between messages as needed

    def display_next_message(self):
        if self.message_queue:
            time, message = self.message_queue.pop(0)
            self.text_edit.moveCursor(self.text_edit.textCursor().End)
            self.text_edit.insertPlainText(f"{time}: {message}\n")
            self.setFocus()

            # Apply fade animation
            animation = QPropertyAnimation(self.text_edit.viewport(), b"opacity")
            animation.setDuration(500)
            animation.setStartValue(0.0)
            animation.setEndValue(1.0)
            animation.setEasingCurve(QEasingCurve.OutQuad)
            animation.start()
        else:
            self.timer.stop()

### HINTS AREA
class InfoWidget(QWidget):
    _instance = None
    signal_next_button_pressed = pyqtSignal()

    def __init__(self):
        super().__init__()
        print("InfoWidget created...")
        self.current_name = None
        self.current_level = 1
        self.level_hints = {
            1: "<Some hints for level 1/>",  # get hints on using abilities and see all type of navies remained
            2: "<Some hints for level 2/>",  # see only navy remained
            3: "<Some hints for level 3/>"   # i think at no hints at all
        }
        self.ships_alive = {
            "Corvete": 0,
            "Vânătoare": 0,
            "Fregate": 0,
            "Distrugatoare": 0
        }

        self.info_layout = QVBoxLayout()

        self.info_label = QLabel("Înformații despre joc")
        self.info_label.setFont(QFont("Arial", 8, QFont.Bold))
        self.info_layout.addWidget(self.info_label)

        self.info_text = QLabel()  # Create QLabel without text for now
        self.info_layout.addWidget(self.info_text)

        self.hint_label = QLabel("Hints")
        self.hint_label.setFont(QFont("Arial", 8, QFont.Bold))
        self.info_layout.addWidget(self.hint_label)

        # Create a horizontal layout for the hints and the start button
        self.hint_button_layout = QHBoxLayout()

        self.status_label = QLabel()
        self.hint_button_layout.addWidget(self.status_label)

        # Add start button
        self.start_button = QPushButton("Poziționează toate navele în teren pentru a începe.")
        self.start_button.setFixedSize(350, 40)
        self.start_button.blockSignals(True)
        self.start_button.setObjectName("start_button_loading") # start_button_working, start_button_waiting, start_button_loading
        self.start_button.clicked.connect(self.start_button_consumed)
        self.hint_button_layout.addWidget(self.start_button)

        # Add the hint_button_layout to the main info_layout
        self.info_layout.addLayout(self.hint_button_layout)

        self.setLayout(self.info_layout)
        self.update_status()
        InfoWidget._instance = self

    def start_button_consumed(self):
        self.signal_next_button_pressed.emit()
        self.start_button.blockSignals(True)
        self.start_button.setObjectName("start_button_waiting")
        self.start_button.setText("În așteptare...")
        self.start_button.setStyleSheet("background-color: #4682B4;")
        self.start_button.updateGeometry()

    def start_button_rearm(self):
        self.start_button.setObjectName("start_button_working")
        self.start_button.setText("Următorul pas...")
        self.start_button.setStyleSheet("background-color: #4CAF50;")
        self.start_button.blockSignals(False)
        self.start_button.updateGeometry()

    def set_username(self, username):
        self.current_name = username
        print("Username setat in InfoWidget")
        self.update_status()

    def set_difficulty(self, difficulty):
        self.current_level = int(difficulty)
        print("Dificultate setat in InfoWidget")
        self.update_status()

    def update_status(self):
        if self.current_name is not None:
            status_text = f"Hints for {self.current_name.upper()} on level {self.current_level} \n {self.level_hints[self.current_level]}"
        else:
            status_text = "Waiting for user information..."
        self.status_label.setText(status_text)
        self.update_info()

    def update_info(self):
        txt = "Nave în viață: \t"
        txt += f"Corvete : {self.ships_alive['Corvete']}  --  "
        txt += f"Vânătoare : {self.ships_alive['Vânătoare']}  --  "
        txt += f"Fregate : {self.ships_alive['Fregate']}  --  "
        txt += f"Distrugatoare : {self.ships_alive['Distrugatoare']} "
        self.info_text.setText(txt)

    @staticmethod
    def get_instance():
        if InfoWidget._instance is None:
            InfoWidget._instance = InfoWidget()
        return InfoWidget._instance


def test_scrollarea():
    app = QApplication(sys.argv)
    window = ScrollableMessageBox()
    window.setGeometry(100, 100, 400, 300)
    window.show()
    for i in range(25):
        window.add_message(f"Message test {i}")
    sys.exit(app.exec_())

def test_infoarea():
    app = QApplication(sys.argv)
    window = InfoWidget()
    window.setGeometry(100, 100, 300, 100)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    test_infoarea()
    #test_scrollarea()
