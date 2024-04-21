# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 16:15:36 2024

@author: Catalin.BUTACU
"""

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QLabel, QPushButton, QGridLayout, QHBoxLayout


class CountedButton(QPushButton):
    def __init__(self, text, count, parent=None):
        super().__init__(text, parent)
        self.origin_name = text
        self._count = count
        self.update_text()

    def decrease_count(self):
        self._count -= 1
        self.update_text()

    def update_text(self):
        self.setEnabled(self._count > 0)
        self.setText(f"{self.origin_name} ({self._count})")

class TerrainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout(self)
        layout.setObjectName("layoutGridTerrain")
        layout.setHorizontalSpacing(0)
        layout.setVerticalSpacing(0)
        self.setFixedSize(400,400)
        # Terrain widget
        self.buttons = []
        for i in range(10):
            row = []
            for j in range(10):
                button = QPushButton(self)
                button.setObjectName("seaPosition")
                button.setFixedSize(40, 40)
                button.setEnabled(True)
                row.append(button)
                layout.addWidget(button, i, j)
            self.buttons.append(row)

class UserTerrainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        user_label = QLabel("Your Terrain", self)
        user_label.setObjectName("userLabel")
        user_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(user_label)

        self.terrain_widget = TerrainWidget(self)
        layout.addWidget(self.terrain_widget)
        
        navy_label = QLabel("Select a navy to deploy", self)
        navy_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(navy_label)

        button_layout = QHBoxLayout()
        
        buttonT1 = CountedButton("Corvete", 3, self)
        buttonT2 = CountedButton("Canoniere", 2, self)
        buttonT3 = CountedButton("Fregate", 1, self)
        buttonT4 = CountedButton("Distrugatoare", 1, self)
        
        buttonT1.setObjectName("placeNavyTier1")
        buttonT2.setObjectName("placeNavyTier2")
        buttonT3.setObjectName("placeNavyTier3")
        buttonT4.setObjectName("placeNavyTier4")
        
        button_layout.addWidget(buttonT1)
        button_layout.addWidget(buttonT2)
        button_layout.addWidget(buttonT3)
        button_layout.addWidget(buttonT4)
        
        buttonT1.clicked.connect(lambda state, s="Corvete": self.place_ship(s, buttonT1))
        buttonT2.clicked.connect(lambda state, s="Canoniere": self.place_ship(s, buttonT2))
        buttonT3.clicked.connect(lambda state, s="Fregate": self.place_ship(s, buttonT3))
        buttonT4.clicked.connect(lambda state, s="Distrugatoare": self.place_ship(s, buttonT4))

        layout.addLayout(button_layout)

    def place_ship(self, ship_type, button):
        button.decrease_count()
        print(f"Placing {ship_type}...")


class EnemyTerrainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        enemy_label = QLabel("Enemy Terrain", self)
        enemy_label.setObjectName("enemyLabel")
        enemy_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(enemy_label)

        self.terrain_widget = TerrainWidget(self)
        layout.addWidget(self.terrain_widget)
        
        action_label = QLabel("Select an action", self)
        action_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(action_label)

        button_layout = QHBoxLayout()
        
        bomb_button = QPushButton("Bomb", self)
        bomb_button.setObjectName("bombButton")
        bomb_button.clicked.connect(self.drop_bomb)
        button_layout.addWidget(bomb_button)
        
        scan_button = QPushButton("Scan", self)
        scan_button.setObjectName("scanButton")
        scan_button.clicked.connect(self.perform_scan)
        button_layout.addWidget(scan_button)
        
        line_assault_button = QPushButton("Line Assault", self)
        line_assault_button.setObjectName("lineAssaultButton")
        line_assault_button.clicked.connect(self.perform_line_assault)
        button_layout.addWidget(line_assault_button)

        layout.addLayout(button_layout)

    def drop_bomb(self):
        print("Dropping bomb...")

    def perform_scan(self):
        print("Performing scan...")

    def perform_line_assault(self):
        print("Performing line assault...")


def load_styles_from_file(root, file_path):
    try:
        with open(file_path, "r") as file:
            style_sheet = file.read()
            root.setStyleSheet(style_sheet)
    except FileNotFoundError:
        print(f"Stylesheet file not found: {file_path}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    window = QWidget()
    layout = QVBoxLayout(window)

    user_terrain = UserTerrainWidget() # EnemyTerrainWidget(window)
    layout.addWidget(user_terrain)
    load_styles_from_file(window, "UI/styles.qss")

    window.show()
    sys.exit(app.exec_())
