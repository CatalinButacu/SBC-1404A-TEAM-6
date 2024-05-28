# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 11:14:16 2024

@authors: Catalin.BUTACU, Serban.VICOL, Nicu.TARADACIUC
"""

# LIBS DEPENDENCIES
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QCoreApplication, QTimer

# LOCAL WIDGETS
from UI.ModuleWidgets import StartGameWidget, GamePlayWidget, EndGameWidget
from UI.DataCollector import GameState, MapState

# CLIPS ENV
import clips
from game_engine import init_sistem_env, write_matrix_to_file 
from game_engine import get_clips_state, get_all_facts_list, get_agenda_list
from game_engine import execute_update_file_map_using_matrix
from game_engine import execute_update_matrix_using_file_map

class BattleshipUI(QMainWindow):
    def __init__(self):
        super().__init__()
        print("BattleshipUI created...")
        self.state = GameState.LOADING
        self.init_window()
        self.scene_start = None
        self.scene_play = None
        self.scene_stop = None
        self.launch_game()

    def init_window(self):
        self.setWindowTitle("Battleship Game SBC")
        self.setFixedSize(980, 820)
        self.center_window()
        self.activateWindow()
        self.raise_()
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.wait_responses = 10

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
        init_sistem_env()
        self.isFirstTime = True


    def connect_signals(self):
        self.scene_start.signal_start_game.connect(self.start_game)
        self.scene_start.signal_name_changed.connect(self.scene_play.set_username)
        self.scene_start.signal_level_changed.connect(self.scene_play.set_difficulty)
        self.scene_start.signal_change_state.connect(self.update_state)
        self.scene_play.signal_update_clips_map_request.connect(self.update_into_clips_map)
        self.timer.timeout.connect(self.update_from_clips_map)

    def update_into_clips_map(self, matrix:dict):
        execute_update_file_map_using_matrix(matrix)
        self.timer.start()
        if self.isFirstTime == True:
            write_matrix_to_file("map_start.txt", matrix)

        self.isFirstTime = False

    def update_from_clips_map(self):
        wait_user_input = get_clips_state()
        if wait_user_input:
            print("Matrice sistem actualizata")
            matrix = execute_update_matrix_using_file_map()
            self.scene_play.user_widget.update_map_from_file(matrix)
            self.timer.stop()

        self.wait_responses -= 1
        if self.wait_responses != 0:
            print("\n\nWaiting for Expert System to respond...")
        else:
            print("\n\nExpert System failed to respond...")



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

    def check_ships_still_alive(self):
        user_data = self.scene_play.user_widget.terrain_widget.data
        sistem_data = self.scene_play.enemy_widget.terrain_widget.data

        ships_user = sum(row.count(MapState.SHIP_PLACED) for row in user_data["state"])
        ships_sistem = sum(row.count(MapState.SHIP_PLACED) for row in sistem_data["state"])

        if ships_user == 0:
            self.end_game("LOSE")
        elif ships_sistem == 0:
            self.end_game("WIN")




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
