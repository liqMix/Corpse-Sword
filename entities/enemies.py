from entities.entity import *
from constants import *


class Enemy(Entity):
    def __init__(self, inmate=None):
        super(Enemy, self).__init__(name=inmate['name'], symbol=SYMBOLS['enemy'])
        self.color = COLORS['enemy']
        self.type = 'enemy'

        self.picture = inmate['mugshot']
        self.charges = inmate['charges']
        self.level = len(self.charges)

    def __repr__(self):
        print("Name: ", self.name)
        print("Level: ", self.level)
        print("Charges: ", self.charges)
        return ""

    def __lt__(self, other):
        return self.level < other.level

    def move(self, move):
        super(Enemy, self).move(move)
