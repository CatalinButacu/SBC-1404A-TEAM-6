# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 16:15:36 2024

@authors: Catalin.BUTACU, Serban.VICOL, Nicu.TARADACIUC
"""

import sys
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QLabel, QPushButton, QGridLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap, QIcon, QCursor
from UI.DataController import *
from UI.UI_Elements import ShipPlacementButton, AbilityPlacementButtons


### TERRAIN CLASSES
"""
    TerrainWidget - BASIC MAP
    > init ground with bunch of buttons and connect each button with place_item
    > keep in focus one ship to be placed and check for condition if it can be placed
    > will use 'isShipPlaced' property to know if a button/cell on the map is already assigned

"""
class TerrainWidget(QWidget):
    signal_decrese_count = pyqtSignal(int)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_ship:Ship = None
        self.selected_ability:Ability = None
        self.ships = []
        self.grid_size = 40
        self.squares = 10
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout(self)
        layout.setObjectName("layoutGridTerrain")
        layout.setHorizontalSpacing(0)
        layout.setVerticalSpacing(0)
        self.setFixedSize(self.squares * self.grid_size, self.squares * self.grid_size)
        self.buttons = []
        for i in range(self.squares):
            row = []
            for j in range(self.squares):
                button = QPushButton(self)
                button.setObjectName("seaPosition")
                button.setFixedSize(self.grid_size, self.grid_size)
                button.setEnabled(True)
                button.setProperty("isShipPlaced","no")
                row.append(button)
                layout.addWidget(button, i, j)
                button.clicked.connect(lambda state, row = i, col = j: self.place_item(row, col))
            self.buttons.append(row)

    def place_item(self, row, col):
        # check for enemy terrain
        if self.parentWidget().objectName() == "EnemyTerrainWidget":
            if self.selected_ability:
                self.selected_ability.setRefPos(row, col)
                self.place_ability()
        # check for user terrain
        if self.parentWidget().objectName() == "UserTerrainWidget":
            self.parentWidget().check_ships_left()
            if self.parentWidget().all_ships_placed:
                print("All ships have been placed.")
                return False

            if self.selected_ship is None:
                print("No ship selected.")
                return

            self.selected_ship.setRefPos(row, col)
            self.place_ship()


    def place_ship(self):
        if self.can_place_ship(self.selected_ship) == False:
            self.parentWidget().setCursor(Qt.ArrowCursor)
            self.selected_ship = None
            return

        x, y = self.selected_ship.refX, self.selected_ship.refY
        size = self.selected_ship.size

        self.deactivate_ship_cells()
        ship_image = QPixmap(self.selected_ship.image_path)

        scaleX, scaleY = self.selected_ship.get_size_px()
        ship_image = ship_image.scaled(scaleX, scaleY)

        if self.selected_ship.orientation == Ship.HORIZONTAL:
            for i in range(size):
                self.buttons[x][y + i].setIcon(QIcon(ship_image.copy(i * 40, 0, 40, 40)))
                self.buttons[x][y + i].setIconSize(QSize(40,40))
        else:
            for i in range(size):
                self.buttons[x + i][y].setIcon(QIcon(ship_image.copy(0, i * 40, 40, 40)))
                self.buttons[x + i][y].setIconSize(QSize(40,40))

        self.signal_decrese_count.emit(size)
        self.parentWidget().addMessageToConsole.emit(f"Ship {self.selected_ship.name} of tier {self.selected_ship.size} was placed at ref position {x},{y}")


    def place_ability(self):
        x, y = self.selected_ability.refX, self.selected_ability.refY
        print(f"Placed_ability on {x},{y}")

        if self.selected_ability.id == 1:
            self.place_bomb(x, y)
        elif self.selected_ability.id == 2:
            self.place_scan(x, y)
        elif self.selected_ability.id == 3:
            self.place_line_assault(x, y)

        self.parentWidget().setCursor(Qt.ArrowCursor)
        self.signal_decrese_count.emit(self.selected_ability.id)
        self.selected_ability = None

    def place_bomb(self, x, y):
        button = self.buttons[x][y]
        button.setEnabled(False)
        button.setObjectName("seaEnemyAttacked")

    def place_scan(self, x, y):
        # add clips fact to execute (wainting for the mechanism)
        pass

    def place_line_assault(self, x, y):
        # add clips fact to execute (wainting for the mechanism)
        pass


    def deactivate_ship_cells(self):
        x, y = self.selected_ship.refX, self.selected_ship.refY

        if self.selected_ship.orientation == Ship.HORIZONTAL:
            for i in range(self.selected_ship.size):
                self.buttons[x][y + i].blockSignals(True)
                self.buttons[x][y + i].setProperty("isShipPlaced","yes")
        else:
            for i in range(self.selected_ship.size):
                self.buttons[x + i][y].blockSignals(True)
                self.buttons[x + i][y].setProperty("isShipPlaced","yes")

    def deactivate_all_buttons(self):
        for i in range(self.squares):
            for j in range(self.squares):
                self.buttons[i][j].setCheckable(False)


    def can_place_ship(self, ship):
        # check for available deploiments
        count = 0
        if ship.size == 1:
            count = self.parentWidget().buttonT1.getCount()
        elif ship.size == 2:
            count = self.parentWidget().buttonT2.getCount()
        elif ship.size == 3:
            count = self.parentWidget().buttonT3.getCount()
        elif ship.size == 4:
            count = self.parentWidget().buttonT4.getCount()

        if count == 1:
            self.parentWidget().setCursor(Qt.ArrowCursor)

        if count == 0:
            self.parentWidget().addMessageToConsole.emit(f"All ships of tier {ship.size} have been placed.")
            return False

        # check for not covering other ships already placed
        size = ship.size
        row, col = ship.refX, ship.refY
        orientation = ship.orientation
        # print(f"size={size}, row={row}, col={col}, orientation={orientation}")

        if orientation == Ship.HORIZONTAL:
            if col + size - 1 >= self.squares:
                return False
            for i in range(size):
                if self.buttons[row][col + i].property("isShipPlaced") == "yes" :
                    self.parentWidget().addMessageToConsole.emit(f"Collision with other ship at {row},{col+i}")
                    return False
        else:
            if row + size - 1 >= self.squares:
                return False
            for i in range(size - 1):
                if self.buttons[row + i][col].property("isShipPlaced") == "yes":
                    self.parentWidget().self.addMessageToConsole.emit(f"Collision with other ship at {row+i},{col}")
                    return False

        return True



"""
    UserTerrainWidget - BASIC Widget
    > init UI subcomponents and ensure communication between widgets
    > let user place ships on the own map

"""
class UserTerrainWidget(QWidget):
    signal_all_ships_placed = pyqtSignal()  # will be used later to start the game
    addMessageToConsole = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("UserTerrainWidget")
        self.init_ui()
        self.all_ships_placed = False

    def init_ui(self):
        layout = QVBoxLayout(self)

        user_label = QLabel("Your Terrain   ", self)
        user_label.setObjectName("userLabel")
        user_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(user_label)

        self.terrain_widget = TerrainWidget(self)
        layout.addWidget(self.terrain_widget)
        self.terrain_widget.signal_decrese_count.connect(self.decrease_count)

        navy_label = QLabel("Select a navy to deploy", self)
        navy_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(navy_label)

        button_layout = QHBoxLayout()

        self.buttonT1 = ShipPlacementButton(tier=1, count=4, parent=self)
        self.buttonT2 = ShipPlacementButton(tier=2, count=3, parent=self)
        self.buttonT3 = ShipPlacementButton(tier=3, count=2, parent=self)
        self.buttonT4 = ShipPlacementButton(tier=4, count=1, parent=self)

        self.buttonT1.setObjectName("placeNavyTier1")
        self.buttonT2.setObjectName("placeNavyTier2")
        self.buttonT3.setObjectName("placeNavyTier3")
        self.buttonT4.setObjectName("placeNavyTier4")

        button_layout.addWidget(self.buttonT1)
        button_layout.addWidget(self.buttonT2)
        button_layout.addWidget(self.buttonT3)
        button_layout.addWidget(self.buttonT4)

        self.buttonT1.signal_ship_selected.connect(self.setSelectionShip)
        self.buttonT2.signal_ship_selected.connect(self.setSelectionShip)
        self.buttonT3.signal_ship_selected.connect(self.setSelectionShip)
        self.buttonT4.signal_ship_selected.connect(self.setSelectionShip)

        layout.addLayout(button_layout)

    def setSelectionShip(self, size:int, orientation:bool):
        self.terrain_widget.selected_ship = Ship(size, orientation)

    def check_ships_left(self):
        if self.buttonT1.getCount() == 0 and self.buttonT2.getCount() == 0 and self.buttonT3.getCount() == 0 and self.buttonT4.getCount() == 0:
            self.signal_all_ships_placed.emit()
            self.all_ships_placed = True
            self.addMessageToConsole.emit("All ships have been placed.")

    def decrease_count(self, size:int):
        if size == 1:
            self.buttonT1.decrease_count()
        elif size == 2:
            self.buttonT2.decrease_count()
        elif size == 3:
            self.buttonT3.decrease_count()
        elif size == 4:
            self.buttonT4.decrease_count()

    def mouseReleaseEvent(self, event):
        self.check_ships_left()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_R and self.terrain_widget.selected_ship:
            self.terrain_widget.selected_ship.rotate()
            width, height = self.terrain_widget.selected_ship.get_size_px()
            self.setCursor(QCursor(QPixmap(self.terrain_widget.selected_ship.image_path).scaled(width, height), -1, -1))


"""
    EnemyTerrainWidget - BASIC Widget
    > init UI subcomponents and ensure communication between widgets
    > let user use abilities on the enemy map

"""
class EnemyTerrainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("EnemyTerrainWidget")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        enemy_label = QLabel("Enemy Terrain", self)
        enemy_label.setObjectName("enemyLabel")
        enemy_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(enemy_label)

        self.terrain_widget = TerrainWidget(self)
        layout.addWidget(self.terrain_widget)
        self.terrain_widget.signal_decrese_count.connect(self.decrease_count)

        action_label = QLabel("Select an action", self)
        action_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(action_label)

        button_layout = QHBoxLayout()

        self.bomb_button = AbilityPlacementButtons(1, 200, self)
        self.bomb_button.setObjectName("bombButton")
        self.bomb_button.signal_ability_selected.connect(self.drop_ability)
        button_layout.addWidget(self.bomb_button)

        self.scan_button = AbilityPlacementButtons(2, 1, self)
        self.scan_button.setObjectName("scanButton")
        self.scan_button.signal_ability_selected.connect(self.drop_ability)
        button_layout.addWidget(self.scan_button)

        self.line_assault_button = AbilityPlacementButtons(3, 2,  self)
        self.line_assault_button.setObjectName("lineAssaultButton")
        self.line_assault_button.signal_ability_selected.connect(self.drop_ability)
        button_layout.addWidget(self.line_assault_button)

        layout.addLayout(button_layout)

    def drop_ability(self, id_ability:int):
        self.terrain_widget.selected_ability = Ability(id_ability)

    def decrease_count(self, id_ability:int):
        if id_ability == 1:
            self.bomb_button.decrease_count()
        elif id_ability == 2:
            self.scan_button.decrease_count()
        elif id_ability == 3:
            self.line_assault_button.decrease_count()


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

    user_terrain = EnemyTerrainWidget() # UserTerrainWidget() # EnemyTerrainWidget(window)
    layout.addWidget(user_terrain)
    load_styles_from_file(window, "UI/styles.qss")

    window.show()
    sys.exit(app.exec_())
