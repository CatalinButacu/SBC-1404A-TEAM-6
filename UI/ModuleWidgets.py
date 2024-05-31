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

from UI.DataCollector import GameState

### STARTS SCENE
class StartGameWidget(QWidget):
    signal_name_changed = pyqtSignal(str)
    signal_level_changed = pyqtSignal(int)
    signal_start_game = pyqtSignal(bool)
    signal_change_state = pyqtSignal(int)

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

        self.signal_change_state.emit(GameState.FILLING_INFO)
        name_label = QLabel("Introduceți numele de jucator:")
        self.name_edit = QLineEdit()
        self.name_edit.editingFinished.connect(self.on_username_changed)

        difficulty_label = QLabel("Alege dificultatea:")
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
        print(F"Jucatorul a introdus numele: {username}")

    def on_difficulty_changed(self):
        difficulty = self.difficulty_combo.currentText()
        self.signal_level_changed.emit(int(difficulty))
        print(F"Nivelul de dificultate selectat este: {int(difficulty)}")

    def on_start_clicked(self):
        self.signal_start_game.emit(True)
        print("O nouă sesiune de joc a început.")


### GAME SCENE
class GamePlayWidget(QWidget):
    signal_rearm_start_button = pyqtSignal()
    signal_update_clips_map_request = pyqtSignal(dict)

    def __init__(self):
        # init game widgets
        super().__init__()
        print("GamePlayWidget created...")
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

        self.info_widget.ships_alive = {
            "Corvete": self.user_widget.buttonT1.getCount(),
            "Vanatoare": self.user_widget.buttonT2.getCount(),
            "Fregate": self.user_widget.buttonT3.getCount(),
            "Distrugatoare": self.user_widget.buttonT4.getCount()
        }

        self.enemy_widget.setEnabled(self.user_widget.all_ships_placed)
        self.user_widget.addMessageToConsole.connect(self.addMessage)
        self.user_widget.signal_all_ships_placed.connect(self.activate_enemy_terrain)
        self.signal_rearm_start_button.connect(self.info_widget.start_button_rearm)

        self.info_widget.start_button.clicked.connect(self.deactivate_enemy_terrain)

    def addMessage(self, message):
        self.message_area_widget.add_message(message)

    def set_username(self, name):
        self.info_widget.set_username(name)
        self.message_area_widget.add_message(f"Bine ai venit în joc: {name.upper()}")

    def set_difficulty(self, dif):
        self.info_widget.set_difficulty(dif)

    def activate_enemy_terrain(self):
        self.enemy_widget.setEnabled(True)
        self.enemy_widget.blockSignals(False)
        self.signal_rearm_start_button.emit()

    def deactivate_enemy_terrain(self):
        self.enemy_widget.blockSignals(True)
        self.signal_update_clips_map_request.emit(self.user_widget.terrain_widget.data)


    def decrease_ship_info(self, tier):
        if tier == 1:
            self.info_widget.ships_alive["Corvete"] -= 1
        elif tier == 2:
            self.info_widget.ships_alive["Vanatoare"] -= 1
        elif tier == 3:
            self.info_widget.ships_alive["Fregate"] -= 1
        elif tier == 4:
            self.info_widget.ships_alive["Distrugatoare"] -= 1

        self.info_widget.update_info()


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
