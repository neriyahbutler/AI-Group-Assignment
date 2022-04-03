import os
import pygame

base_path = os.path.dirname(os.path.abspath(__file__))

font_path = os.path.join(base_path, "./font/Joystix.ttf")
font = pygame.font.Font(font_path, 35)


class Agent(object):
    x_move = 0
    y_move = 0

    block_count = 0

    movement = 40

    def move_left(self):
        if self.x_move != 0:
            self.x_move -= 1

    def move_right(self):
        if self.x_move != 4:
            self.x_move += 1

    def move_down(self):
        if self.y_move != 4:
            self.y_move += 1
            
    def move_up(self):
        if self.y_move != 0:
            self.y_move -= 1

    def get_pos(self):
        return (150 + self.x_move * self.movement, 140 + self.y_move * self.movement)

    def get_block_count(self):
        return self.block_count

    def increase_block_count(self):
        self.block_count += 1

    def decrase_block_count(self):
        self.block_count -= 1