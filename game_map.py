import tcod.map
import tcod.path
import tcod.random
from item import *
from window import *
import numpy as np
import math


class GameMap(Frame):
    class Cell:
        def __init__(self):
            self.entities = []

    def __init__(self, anchor=(0,0), size_x=80, size_y=24, entities=[]):
        super(GameMap, self).__init__(anchor=anchor, name='gamemap')
        self.map = tcod.map.Map(width=size_x, height=size_y)
        self.cells = [[self.Cell() for y in range(size_y+1)] for x in range(size_x+1)]
        self.entities = entities
        self.size_x = size_x // 2
        self.size_y = size_y // 2
        self.items = []
        self.top_left = (self.x - self.size_x, self.y - self.size_y)
        self.populate()

    # Check is move to destination is legal for entity
    def check_move(self, move, entity):
        dest_x, dest_y = move
        dest_x = entity.x + dest_x
        dest_y = entity.y + dest_y

        # Find walkable path to destination
        astar = tcod.path.AStar(self.map.walkable)
        if astar.get_path(entity.x, entity.y, dest_x, dest_y) is None:
            return False

        elif (dest_x > (self.x + self.size_x)) or (dest_x < (self.x - self.size_x)):
            return False

        elif (dest_y > (self.y + self.size_y)) or (dest_y < (self.y - self.size_y)):
            return False

        return True

    # Return list of items and remove from map
    def get_items(self, entity):

        # Get relative position of entity
        x, y = entity.pos
        x = x - self.top_left[0]
        y = y - self.top_left[1]

        items_to_get = self.cells[x][y].entities
        if items_to_get is not None:
            entity.add_items(items_to_get)
            for i in items_to_get:
                self.items.pop(self.items.index(i))
            self.cells[x][y].entities = []

    # Add items to map
    def populate(self):
        for item in ITEMS.keys():
            rand_x = math.floor(np.random.random() * (self.size_x*2 - 1) + 1)
            rand_y = math.floor(np.random.random() * (self.size_y*2 - 1) + 1)
            new_item = Item(item, (rand_x+self.top_left[0], rand_y+self.top_left[1]))
            self.cells[rand_x][rand_y].entities.append(new_item)
            self.items.append(new_item)

    # Draw map to screen
    def draw(self, con):
        top_edge_y = self.y - self.size_y - 1
        bot_edge_y = self.y + self.size_y + 1
        left_edge_x = self.x - self.size_x - 1
        right_edge_x = self.x + self.size_x + 1

        # Draw border of map
        hash = ord('#')
        for x in range(self.size_x*2 + 2):
            con.put_char(x + left_edge_x, top_edge_y, hash, tcod.BKGND_NONE)
            con.put_char(x + left_edge_x, bot_edge_y, hash, tcod.BKGND_NONE)

        for y in range(self.size_y*2 + 3):
            con.put_char(left_edge_x, y + top_edge_y, hash, tcod.BKGND_NONE)
            con.put_char(right_edge_x, y + top_edge_y, hash, tcod.BKGND_NONE)

        # Draw entities
        for entity in self.entities:
            entity.draw(con)

        # Draw items
        for item in self.items:
            item.draw(con)
