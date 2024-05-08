# -*- coding: utf-8 -*-
"""
Created on Wed May  8 21:30:26 2024

@authors: Catalin.BUTACU, Serban.VICOL, Nicu.TARADACIUC
"""

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QPixmap, QCursor

from UI.DataController import *

### UI ELEMENTS

"""
    CountedButton - UI Element
    > informing user about remained ship available to place on the map
    > change mouse icon with ship selected click
    > emit signal to inform other widgets about selected ship

"""
class ShipPlacementButton(QPushButton):
    signal_ship_selected = pyqtSignal(int, bool)

    def __init__(self, tier, count, parent=None):
        super().__init__(parent)
        self._count = count
        self.ship = Ship(tier)
        self.update_text_button()
        self.cursor_pixmap = QPixmap(self.ship.image_path)
        width, height = self.ship.get_size_px()
        self.cursor_pixmap = self.cursor_pixmap.scaled(width, height)

    def decrease_count(self):
        if self._count > 0:
            self._count -= 1
            self.update_text_button()

    def update_text_button(self):
        new_state = self._count > 0
        if self.isEnabled() != new_state:
            self.setEnabled(new_state)
        new_text = f"{self.ship.name} ({self._count})"
        if self.text() != new_text:
            self.setText(new_text)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            width, height = 40, 40 # self.ship.get_size_px()
            self.parent().setCursor(QCursor(self.cursor_pixmap, width // 2, height // 2))
            self.signal_ship_selected.emit(self.ship.size, self.ship.orientation)

    def getCount(self):
        return self._count


class AbilityPlacementButtons(QPushButton):
    signal_ability_selected = pyqtSignal(int)

    def __init__(self, tier, count, parent=None):
        super().__init__(parent)
        self._count = count
        self.ability = Ability(tier)
        self.update_text_button()
        self.cursor_pixmap = QPixmap(self.ability.image_path)
        self.cursor_pixmap = self.cursor_pixmap.scaled(40, 40) if self.ability.id > 2 else self.cursor_pixmap.scaled(30, 30)

    def decrease_count(self):
        if self._count > 0:
            self._count -= 1
            self.update_text_button()

    def update_text_button(self):
        new_state = self._count > 0
        if self.isEnabled() != new_state:
            self.setEnabled(new_state)
        new_text = f"{self.ability.name} ({self._count})" if self._count<10 else f"{self.ability.name} (∞)"
        if self.text() != new_text:
            self.setText(new_text)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            width, height = 40, 40
            if self.ability.id < 3:
                width, height = 30, 30
            self.parent().setCursor(QCursor(self.cursor_pixmap, width // 2, height // 2))
            self.signal_ability_selected.emit(self.ability.id)

    def getCount(self):
        return self._count
