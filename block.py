import os
import pygame

base_path = os.path.dirname(os.path.abspath(__file__))

font_path = os.path.join(base_path, "./font/Joystix.ttf")
font = pygame.font.Font(font_path, 20)

class Block(object):
    x_move = 0
    y_move = 0

    movement = 40

    def __init__(self, count = 0, color = (0,0,0)):
        self.block_count = 0
        self.color = color
        self.symbol = font.render(str(self.block_count), 1, self.color)

    def set_capacity(self, capacity):
        self.capacity = capacity

    def get_capacity(self):
        return self.capacity

    def get_symbol(self):
        return self.symbol

    def set_block_count(self, count):
        self.block_count = count

    def update_symbol(self):
        self.symbol = font.render(str(self.block_count), 1, self.color)

    def get_block_count(self):
        return self.block_count

    def set_pos(self, pos):
        self.x_move = pos[0]
        self.y_move = pos[1]
        self.pos = [150 + self.x_move * self.movement, 140 + self.y_move * self.movement]

    def get_pos(self):
        return self.pos