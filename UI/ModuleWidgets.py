# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 22:48:51 2024

@authors: Catalin.BUTACU, Serban.VICOL, Nicu.TARADACIUC
"""

# LIBS
import sys
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QLineEdit, QDesktopWidget

# LOCAL WIDGETS
from UI.ComunicationWidgets import ScrollableMessageBox, InfoWidget
from UI.GameWidgets import UserTerrainWidget, EnemyTerrainWidget


### STARTS SCENE
class StartGameWidget(QWidget):
    signal_name_changed = pyqtSignal(str)
    signal_level_changed = pyqtSignal(int)
    signal_start_game = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        print("StartGameWidget created...")
        self.setObjectName("StartGameWidget")
        self.setWindowTitle("Start Game")
        self.setFixedSize(1000, 820)
        self.center_window()

        main_layout = QHBoxLayout()
        main_layout.addStretch(3)

        # Adding the interesting area
        interesting_area_layout = QVBoxLayout()
        interesting_area_layout.addStretch(1)

        name_label = QLabel("Insert your name:")
        self.name_edit = QLineEdit()
        self.name_edit.editingFinished.connect(self.on_username_changed)

        difficulty_label = QLabel("Choose difficulty:")
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(["1", "2", "3"])
        self.difficulty_combo.currentIndexChanged.connect(self.on_difficulty_changed)


        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.on_start_clicked)

        interesting_area_layout.addWidget(name_label)
        interesting_area_layout.addWidget(self.name_edit)
        interesting_area_layout.addWidget(difficulty_label)
        interesting_area_layout.addWidget(self.difficulty_combo)
        interesting_area_layout.addWidget(self.start_button)

        interesting_area_layout.addStretch(1)

        main_layout.addLayout(interesting_area_layout, 4)
        main_layout.addStretch(3)

        self.setLayout(main_layout)

    def center_window(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def on_username_changed(self):
        username = self.name_edit.text()
        self.signal_name_changed.emit(username)
        print(F"Client just inserted usernam: {username}")

    def on_difficulty_changed(self):
        difficulty = self.difficulty_combo.currentText()
        self.signal_level_changed.emit(int(difficulty))
        print(F"Client just changed level difficulty: {int(difficulty)}")

    def on_start_clicked(self):
        self.signal_start_game.emit(True)
        print("Client just initiated a new sesion game")


### GAME SCENE
class GamePlayWidget(QWidget):
    def __init__(self):
        # init game widgets
        super().__init__()
        print("BattleshipUI created...")
        self.user_widget = UserTerrainWidget()
        self.enemy_widget = EnemyTerrainWidget()
        self.message_area_widget = ScrollableMessageBox()
        self.info_widget = InfoWidget()

        # init layouts
        layout = QVBoxLayout(self)
        layout.addWidget(self.message_area_widget)
        terrain_widget = QWidget()
        terrain_layout = QHBoxLayout(terrain_widget)
        terrain_layout.addWidget(self.user_widget)
        terrain_layout.addWidget(self.enemy_widget)
        terrain_layout.setAlignment(self.user_widget, Qt.AlignCenter)
        terrain_layout.setAlignment(self.enemy_widget, Qt.AlignCenter)
        layout.addWidget(terrain_widget)
        layout.addWidget(self.info_widget)
        # notify user that game is ready to continue

        print("GamePlayWidget created...")
        self.message_area_widget.add_message("Welcome to the game")

        self.user_widget.addMessageToConsole.connect(self.addMessage)

    def addMessage(self, message):
        self.message_area_widget.add_message(message)


### END SCENE
class EndGameWidget(QWidget):
    def __init__(self, result):
        super().__init__()
        print("EndGameWidget created...")
        self.setWindowTitle("End Game")
        self.setFixedSize(1000, 820)
        self.center_window()

        main_layout = QVBoxLayout()

        result_label = QLabel("You Win!" if result == "win" else "You Lose!")
        result_label.setObjectName("winResult" if result == "win" else "loseResult")
        main_layout.addWidget(result_label)

        restart_button = QPushButton("Restart")
        restart_button.setObjectName("restartButton")
        restart_button.clicked.connect(self.restart_game)
        main_layout.addWidget(restart_button)

        self.setLayout(main_layout)

    def center_window(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def restart_game(self):
        self.parent().restart_game()


### TEST THE WIDGET
if __name__ == "__main__":
    app = QApplication(sys.argv)
    setup_widget = StartGameWidget()
    #setup_widget = EndGameWidget("win")
    setup_widget.show()
    sys.exit(app.exec_())
