# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 11:14:16 2024

@authors: Catalin.BUTACU, Serban.VICOL, Nicu.TARADACIUC
"""

# LIBS DEPENDENCIES
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QCoreApplication

# LOCAL WIDGETS
from UI.ModuleWidgets import StartGameWidget, GamePlayWidget, EndGameWidget
from UI.DataCollector import GameState

class BattleshipUI(QMainWindow):
    def __init__(self):
        super().__init__()
        print("BattleshipUI created...")
        self.state = GameState.LOADING
        self.setWindowTitle("Battleship Game SBC")
        self.setFixedSize(980, 820)
        self.center_window()
        self.scene_start = None
        self.scene_play = None
        self.scene_stop = None
        #self.end_game("lose")
        self.launch_game()
        self.raise_()
        self.activateWindow()

    def center_window(self):
        screen_geometry = QCoreApplication.instance().desktop().screenGeometry()
        center_x = screen_geometry.width() // 2 - self.width() // 2
        center_y = screen_geometry.height() // 2 - self.height() // 1.8
        self.move(int(center_x), int(center_y))

    def launch_game(self):
        self.scene_start = StartGameWidget()
        self.scene_play = GamePlayWidget()
        self.setCentralWidget(self.scene_start)
        self.connect_signals()

    def connect_signals(self):
        self.scene_start.signal_start_game.connect(self.start_game)
        self.scene_start.signal_name_changed.connect(self.scene_play.set_username)
        self.scene_start.signal_level_changed.connect(self.scene_play.set_difficulty)
        self.scene_start.signal_change_state.connect(self.update_state)


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

    def update_state(self, state):
        self.state = state

    def update_map(self, isUser=False):
        path = "map_user.txt" if isUser else "map_system.txt"
        with open(path, "r+"):
            pass




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
