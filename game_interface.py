# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 11:14:16 2024

@authors: Catalin.BUTACU, Serban.VICOL, Nicu.TARADACIUC
"""

# LIBS DEPENDENCIES
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import QCoreApplication, Qt

# LOCAL WIDGETS
from UI.ModuleWidgets import StartGameWidget, EndGameWidget
from UI.GameWidgets import UserTerrainWidget, EnemyTerrainWidget
from UI.ComunicationWidgets import ScrollableMessageBox, InfoWidget


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

class BattleshipUI(QMainWindow):
    def __init__(self):
        super().__init__()
        print("BattleshipUI created...")
        self.setWindowTitle("Battleship Game SBC")
        self.setFixedSize(1000, 820)
        self.center_window() 
        self.scene_start = None
        self.scene_play = None
        self.scene_stop = None
        #self.end_game("lose")
        self.launch_game() 

    def center_window(self):
        screen_geometry = QCoreApplication.instance().desktop().screenGeometry()
        center_x = screen_geometry.width() // 2 - self.width() // 2
        center_y = screen_geometry.height() // 2 - self.height() // 1.8
        self.move(int(center_x), int(center_y))

    def launch_game(self):
        self.scene_start = StartGameWidget()
        self.scene_play = GamePlayWidget()
        self.scene_start.signal_start_game.connect(self.start_game)
        self.scene_start.signal_name_changed.connect(self.scene_play.info_widget.set_username)
        self.scene_start.signal_level_changed.connect(self.scene_play.info_widget.set_difficulty)
        self.setCentralWidget(self.scene_start)

    def start_game(self):
        if self.scene_start:
            self.scene_start.deleteLater()
        self.setCentralWidget(self.scene_play)
        self.center_window()

    def end_game(self, result):
        if self.scene_play:
            self.scene_play.deleteLater()
        self.scene_stop = EndGameWidget(result)
        self.setCentralWidget(self.scene_stop)
        self.center_window()

    def restart_game(self):
        if self.scene_stop:
            self.scene_stop.deleteLater()
        self.launch_game()


def load_styles_from_file(root, file_path):
    try:
        with open(file_path, "r") as file:
            style_sheet = file.read()
            root.setStyleSheet(style_sheet)
    except FileNotFoundError:
        print(f"Stylesheet file not found: {file_path}")


def main():
    app = QApplication(sys.argv)
    load_styles_from_file(app, "UI/styles.qss")
    
    game_ui = BattleshipUI()
    game_ui.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
    
