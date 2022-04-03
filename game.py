import pygame
import os
import numpy as np

pygame.init()

from male import Male
from female import Female

base_path = os.path.dirname(os.path.abspath(__file__))

game_board_path = os.path.join(base_path, "./agent_board.png")
game_board = pygame.image.load(game_board_path)

game_bool = True

width = 500
height = 500

q_values = np.zeros((5, 5, 4))

win = pygame.display.set_mode((width, height))

male = Male()
female = Female()

game_board_positions = {}

for x in range(0,5):
    for y in range(0, 5):
        game_board_positions['{}, {}'.format(x, y)] = {
            # "reward": -1,
            "occupied": False,
            "dropoff": False,
            "pickup": False
        }


while game_bool:
    win.fill((0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_bool = False
    
    win.blit(game_board, (125,125))
    win.blit(male.get_symbol(), male.get_pos())

    pygame.display.update()

pygame.quit()