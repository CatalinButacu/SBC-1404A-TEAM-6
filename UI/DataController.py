# -*- coding: utf-8 -*-
"""
Created on Wed May  8 21:31:25 2024

@authors: Catalin.BUTACU, Serban.VICOL, Nicu.TARADACIUC
"""


### SOME DICTIONARIES FOR THE CLASSES
SHIP_NAME = {
    1:"Corvete",
    2:"Canoniere",
    3:"Fregate",
    4:"Distrugatoare",
}
PATH_V = {
    1:"Resources\components\V-Monitoare.png",
    2:"Resources\components\V-Canoniera.png",
    3:"Resources\components\V-Fregate.png",
    4:"Resources\components\V-Distroyer.png",
}
PATH_H = {
    1:"Resources\components\H-Monitoare.png",
    2:"Resources\components\H-Canoniera.png",
    3:"Resources\components\H-Fregate.png",
    4:"Resources\components\H-Distroyer.png",
}

ABILITY_NAME = {
    1:"Bomb",
    2:"Scan",
    3:"Line Assault",
}
PATH_ABILITY = {
    1:"Resources\components\TARGET.png",
    2:"Resources\components\SCAN.png",
    3:"Resources\components\ASSAULT.png",
}


"""
    Ship
    > just let us keep more info about type of ship in interactions

"""
class Ship:
    HORIZONTAL = 0
    VERTICAL = 1

    def __init__(self, size, orientation=HORIZONTAL):
        self.size = size
        self.orientation = orientation
        self.refX = -1
        self.refY = -1
        self.name = SHIP_NAME.get(size,'Not a ship')
        self.image_path = PATH_H.get(size,'Not a ship') if self.orientation == self.HORIZONTAL else PATH_V.get(size,'Not a ship')

    def rotate(self):
        self.orientation = self.VERTICAL if self.orientation == self.HORIZONTAL else self.HORIZONTAL
        self.image_path = PATH_H.get(self.size,'Not a ship') if self.orientation == self.HORIZONTAL else PATH_V.get(self.size,'Not a ship')

    def setRefPos(self, x, y):
        self.refX = x
        self.refY = y

    def get_size_px(self):
        size_px = (self.size * 40, 40)
        return size_px if self.orientation == self.HORIZONTAL else size_px[::-1]


"""
    Ability
    > just let us keep more info about type of ability that user could interact with

"""
class Ability:
    def __init__(self, id_ability):
        self.id = id_ability
        self.refX = -1
        self.refY = -1
        self.name = ABILITY_NAME.get(id_ability,'No ability selected')
        self.image_path = PATH_ABILITY.get(id_ability,'No ability selected')

    def setRefPos(self, x, y):
        self.refX = x
        self.refY = y
