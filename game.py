import pygame
import os
import numpy as np

pygame.init()

from male import Male
from female import Female
import helper_functions

base_path = os.path.dirname(os.path.abspath(__file__))

game_board_path = os.path.join(base_path, "./agent_board.png")
game_board = pygame.image.load(game_board_path)

game_bool = True

width = 500
height = 500

win = pygame.display.set_mode((width, height))

male = Male()
female = Female()

game_board_positions = {}
q_table = helper_functions.generate_qtable()

for x in range(0,5):
    for y in range(0, 5):
        game_board_positions['{},{}'.format(x, y)] = {
            "reward": -1,
            "occupied": False,
            "dropoff": False,
            "pickup": False
        }

test_bool = True
male_turn_bool = True

while game_bool:
    win.fill((0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_bool = False
    
    win.blit(game_board, (125,125))
    win.blit(male.get_symbol(), male.get_pos())

    pygame.time.wait(50)
    if test_bool:
        if male_turn_bool:
            q_table, game_board_positions, action_to_take = helper_functions.q_learning(male, q_table, game_board_positions, 0.5, 0.5)
            # male_turn_bool = False

            if action_to_take == "north":
                male.move_up()
            elif action_to_take == "south":
                male.move_down()
            elif action_to_take == "east":
                male.move_right()
            else:
                male.move_left()
        else:
            q_table, game_board_positions, action_to_take = helper_functions.q_learning(female, q_table, game_board_positions, 0.5, 0.5)
            male_turn_bool = True

            if action_to_take == "north":
                female.move_up()
            elif action_to_take == "south":
                female.move_down()
            elif action_to_take == "east":
                female.move_right()
            else:
                female.move_left()
    pygame.display.update()

pygame.quit()