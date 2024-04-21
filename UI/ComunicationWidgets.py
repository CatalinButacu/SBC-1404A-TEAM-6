# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 10:06:56 2024

@author: Catalin.BUTACU
"""

import sys
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit
from PyQt5.QtCore import QTimer, QDateTime, QPropertyAnimation, QEasingCurve


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
        
        self.info_layout = QVBoxLayout()

        self.info_label = QLabel("Game Information")
        self.info_label.setFont(QFont("Arial", 8, QFont.Bold))
        self.info_layout.addWidget(self.info_label)

        self.info_text = QLabel()  # Create QLabel without text for now
        self.info_layout.addWidget(self.info_text)

        self.hint_label = QLabel("Hints")
        self.hint_label.setFont(QFont("Arial", 8, QFont.Bold))
        self.info_layout.addWidget(self.hint_label)

        self.status_label = QLabel()
        self.update_status()
        self.info_layout.addWidget(self.status_label)

        self.setLayout(self.info_layout)

    def set_username(self, username):
        self.current_name = username
        self.update_status()

    def set_difficulty(self, difficulty):
        self.current_level = int(difficulty)
        self.update_status()

    def update_status(self):
        if self.current_name is not None:
            status_text = f"Status for {self.current_name}, level {self.current_level}: {self.level_hints[self.current_level]}"
        else:
            status_text = "Waiting for user information..."
        self.status_label.setText(status_text)



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
    #test_infoarea()
    test_scrollarea()


# ### RETAIN ALL DATA IN SAME PIN SPACE
# class Singleton(type):
#     _instances = {}

#     def __call__(cls, *args, **kwargs):
#         if cls not in cls._instances:
#             cls._instances[cls] = super().__call__(*args, **kwargs)
#         return cls._instances[cls]

# class InitDataApp(metaclass=Singleton):
#     _instances = {}

#     def __init__(self):
#         self.user_name = "Guest"
#         self.difficulty = 1

#     @classmethod
#     def getUserName(cls):
#         return cls._instances[cls].user_name

#     @classmethod
#     def getUserDifficulty(cls):
#         return cls._instances[cls].difficulty
    
#     @classmethod
#     def setUserName(cls, name):
#         cls._instances[cls].user_name = name
    
#     @classmethod
#     def setUserDifficulty(cls, lv):
#         cls._instances[cls].difficulty = lv
