import re
import pygame
import os
import numpy as np

pygame.init()

from male import Male
from female import Female

from pickup_block import PickupBlock
from dropoff_block import DropoffBlock

import helper_functions

# This is for handling loading the images and the font we use for making the symbols that represent the different aspect of the program, like the "male" and "female" agent and etc
base_path = os.path.dirname(os.path.abspath(__file__))

game_board_path = os.path.join(base_path, "./agent_board.png")
game_board = pygame.image.load(game_board_path)

game_bool = True

# Sets up the dimensions of the game/visualization window
width = 500
height = 500

win = pygame.display.set_mode((width, height))


# Creates male and female agent
male = Male()
female = Female()


# Creates q table we need
q_table = helper_functions.generate_qtable()


#  All the positions we need for the pickup and dropoff blocks
#  In addition to this, it sets all the positions in the "game_board_positions" dictionary to have
#  the rewards/dropff and pickup status that match the position

pickup_positions = [[4,2], [1,3]]
dropoff_positions = [[4,0], [2,2]]

male_start_position = [0,0]

male.set_coor(male_start_position)

pickup_count = 2
dropoff_count_max = 2


# Goes through every position in the matrix and sets up its respected position in the map
game_board_positions = {}
for x in range(0,5):
    for y in range(0, 5):
        game_board_positions['{},{}'.format(x, y)] = {
            "reward": -1,
            "occupied": False,
            "dropoff": False,
            "pickup": False
        }

for pos in pickup_positions:
    temp_pickup_block = PickupBlock(count=2, color=(50, 205, 50)) # Green
    temp_pickup_block.set_block_count(pickup_count)
    temp_pickup_block.update_symbol()
    temp_pickup_block.set_pos(pos)
    game_board_positions['{},{}'.format(pos[0], pos[1])]["special_block"] = temp_pickup_block
    game_board_positions['{},{}'.format(pos[0], pos[1])]["pickup"] = True
    game_board_positions['{},{}'.format(pos[0], pos[1])]["reward"] = 13

for pos in dropoff_positions:
    temp_dropoff_block = DropoffBlock(2, (138, 43, 226)) # Purple
    temp_dropoff_block.set_capacity(dropoff_count_max)
    temp_dropoff_block.update_symbol()
    temp_dropoff_block.set_pos(pos)
    game_board_positions['{},{}'.format(pos[0], pos[1])]["special_block"] = temp_dropoff_block
    game_board_positions['{},{}'.format(pos[0], pos[1])]["dropoff"] = True
    game_board_positions['{},{}'.format(pos[0], pos[1])]["reward"] = 13


# Defines variables necessary for handling 2 aspects of the game.
# "test_bool" is for testing out/running the q learning algorithm.
# As for "male_turn_bool", this is for handling the various turns between male and female agents
test_bool = True
male_turn_bool = True



while game_bool:
    # Fills out the background of the visualization window with black
    win.fill((0))

    # For handling closing out the visualization window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_bool = False
            print(q_table)
    

    # This is for drawing the objects onto the vizualization window (the "win" variable)
    # Basically "win.blit(...)"" is just for drawing objects in the first parameter at the position
    # specified in the 2nd parameter
    win.blit(game_board, (125,125))
    win.blit(male.get_symbol(), male.get_pos())


    for pos in pickup_positions:
        win.blit(
            game_board_positions['{},{}'.format(pos[0], pos[1])]["special_block"].get_symbol(),
            game_board_positions['{},{}'.format(pos[0], pos[1])]["special_block"].get_pos()
        )

    for pos in dropoff_positions:
        win.blit(
            game_board_positions['{},{}'.format(pos[0], pos[1])]["special_block"].get_symbol(),
            game_board_positions['{},{}'.format(pos[0], pos[1])]["special_block"].get_pos()
        )


    # Pauses the script for 50 miliseconds so it can be easier to follow but not take forever. If you want to change the amount of pauses behind
    # each move, modify the number
    pygame.time.wait(1)
    

    if test_bool:
        if male_turn_bool:
            # Q learning algorithm returns updated q table, updated gmae board positions dictionary and the action of the agent to take
            q_table, game_board_positions, action_to_take = helper_functions.q_learning(male, q_table, game_board_positions, 0.5, 0.5)
            # male_turn_bool = False <---- This is ideally what will handle the male and female taking turns moving


            # Checks the males current position to see if it is in a dropoff/pickup position. If it is, then
            # we check to see if the agent is able to pickup/dropoff in the first place (like "Does the agent have
            # 1 block and is the dropoff spot not at full capacity?")
            current_pos = male.get_coor()
            current_pos_as_key = "{},{}".format(current_pos[0], current_pos[1])

            # Checking if position is pickup spot
            if game_board_positions[current_pos_as_key]["pickup"] == True:
                # Checks to see if pickup action is possible
                if game_board_positions[current_pos_as_key]["special_block"].get_block_count() > 0 and male.get_block_count() == 0:
                    # Decreases the pickup spot's block count + updates the graphic that displays it's block count 
                    # while increasing the agent's block count
                    game_board_positions[current_pos_as_key]["special_block"].decrease_block_count()
                    game_board_positions[current_pos_as_key]["special_block"].update_symbol()
                    male.increase_block_count()

            # Checking if position is dropoff spot
            elif game_board_positions[current_pos_as_key]["dropoff"] == True:
                # Checks to see if dropoff action is possible
                if game_board_positions[current_pos_as_key]["special_block"].get_block_count() < game_board_positions[current_pos_as_key]["special_block"].get_capacity() \
                and male.get_block_count() == 1:
                    # Increases the dropoff spot's block count and updates the graphic that displays it's block count 
                    # while decreasing the agent's block count
                    game_board_positions[current_pos_as_key]["special_block"].increase_block_count()
                    game_board_positions[current_pos_as_key]["special_block"].update_symbol()
                    male.decrease_block_count()

            if action_to_take == "north":
                male.move_up()
            elif action_to_take == "south":
                male.move_down()
            elif action_to_take == "east":
                male.move_right()
            else:
                male.move_left()
        else:
            # Runs q learning algorithm and gets the updated values produced from said function
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

    # This is responsible for updating the graphics that represent the pickup and dropoff spots
    if helper_functions.check_dropoff_capacity(game_board_positions, dropoff_positions):
        male, female, game_board_positions = helper_functions.reset_world(male, female, game_board_positions, pickup_positions, dropoff_positions, pickup_count, male_start_position)
        for pos in pickup_positions:
            game_board_positions['{},{}'.format(pos[0], pos[1])]["special_block"].update_symbol()
        for pos in dropoff_positions:
            game_board_positions['{},{}'.format(pos[0], pos[1])]["special_block"].update_symbol()

    pygame.display.update()

pygame.quit()