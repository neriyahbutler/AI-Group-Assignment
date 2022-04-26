import pygame
import os
import numpy as np
import sys
import time
import random

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

same_pos_cnt = 0

# Creates q table we need
q_table_male_pickup = helper_functions.generate_qtable()
q_table_male_dropoff = helper_functions.generate_qtable()

q_table_female_pickup = helper_functions.generate_qtable()
q_table_female_dropoff = helper_functions.generate_qtable()

#Creates tables for Position Mapping

heatmap_male_pickup = helper_functions.generate_heatMap()
heatmap_male_dropoff = helper_functions.generate_heatMap()

heatmap_female_pickup = helper_functions.generate_heatMap()
heatmap_female_dropoff = helper_functions.generate_heatMap()

#  All the positions we need for the pickup and dropoff blocks
#  In addition to this, it sets all the positions in the "game_board_positions" dictionary to have
#  the rewards/dropff and pickup status that match the position

pickup_positions = [[4,2], [1,3]]
dropoff_positions = [[4,0], [2,2], [0,0], [4,4]]

male_start_position = [2,4]
female_start_position = [2,0]

male.set_coor(male_start_position)
female.set_coor(female_start_position)

# Changes the amount of blocks at that pickup spot and capacity of the dropoff spot
pickup_count = 10
dropoff_count_max = 5

# Goes through every position in the matrix and sets up its respected position in the map
game_board_positions = {}
for x in range(0,5):
    for y in range(0,5):
        game_board_positions['{},{}'.format(x, y)] = {
            "reward": -1,
            "occupied": False,
            "dropoff": False,
            "pickup": False
        }

game_board_positions['{},{}'.format(male_start_position[0], male_start_position[1])]['occupied'] = True
game_board_positions['{},{}'.format(female_start_position[0], female_start_position[1])]['occupied'] = True

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

policy_provided = False
steps_provided = False

current_policy = ""
steps = 8000
experiment_input = ""

#Experiment 4 defined variables necessary for execution
doing_experiment_4 = False
new_pickup_positions = [[0,1], [3,4]]

seed_value = random.randrange(sys.maxsize)
random.seed(seed_value)


while policy_provided is False:
    experiment_input = input("Choose a experiment ('1a', '1b', '1c', '2', '3', '4'): ")
    if experiment_input not in ["1a", "1b", "1c", "2", "3", "4"]:
        print("Not valid input")
        continue
    else:
        policy_provided = True

# Loads the settings defined under the experiment_settings variable in the helper_functions.py file
if experiment_input != "2" or experiment_input != "4":
    current_policy = helper_functions.experiment_settings[experiment_input][0][1]

learning_rate = 0.3
discount_factor = 0.5
policy_epsilon = 0.2
male_next_action = ""
female_next_action = ""
next_action = ""
time_array = []
start_time = 0
if experiment_input == "3":
    learning_rate = helper_functions.experiment_settings[experiment_input][2][0]
    discount_factor = helper_functions.experiment_settings[experiment_input][2][1]

if experiment_input == "4":
    doing_experiment_4 = True

helper_functions.wipe_experiment_stats("exp-{}".format(experiment_input))
print("Working. This will take a moment!")

start_time = time.time()

while game_bool:
    # Fills out the background of the visualization window with black
    win.fill((0))
    
    # For handling closing out the visualization window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_bool = False
            print("Male Q-Table Dropoff\n", q_table_male_dropoff, "\n")
            print("Male Q-Table Pickup\n", q_table_male_pickup, "\n")

            print("Female Q-Table Dropoff\n", q_table_female_dropoff, "\n")
            print("Female Q-Table Pickup\n", q_table_female_pickup, "\n")
    

    # This is for drawing the objects onto the vizualization window (the "win" variable)
    # Basically "win.blit(...)"" is just for drawing objects in the first parameter at the position
    # specified in the 2nd parameter
    win.blit(game_board, (125,125))
    win.blit(male.get_symbol(), male.get_pos())
    win.blit(female.get_symbol(), female.get_pos())

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
        # Fills out the background of the visualization window with black
        win.fill((0))

        # This is for drawing the objects onto the vizualization window (the "win" variable)
        # Basically "win.blit(...)"" is just for drawing objects in the first parameter at the position
        # specified in the 2nd parameter
        helper_functions.display_game_board(win, game_board)
        helper_functions.display_male_female_agents(win, male, female)
        helper_functions.display_dropoff_pickup_locations(win, pickup_positions, dropoff_positions, game_board_positions)
        helper_functions.display_game_details(male, female, dropoff_count_max, pickup_count, len(male.get_steps_list()) + 1, win)     

        if male_turn_bool:

            current_pos = male.get_coor()
            current_pos_as_key = "{},{}".format(current_pos[0], current_pos[1])

            # Sets the current position that the agent is one to not be occupied as the q learning function will move it to another position
            game_board_positions[current_pos_as_key]["occupied"] = False

            # Q learning algorithm returns updated q table, updated gmae board positions dictionary and the action of the agent to take
            # If the male has at least one block, we use the dropoff qtable. Otherwise we use pickup


            if male.get_block_count() == 0:
                heatmap_male_pickup = helper_functions.update_heatmap(current_pos, heatmap_male_pickup)
                if experiment_input == "2" or experiment_input == "4":
                    q_table_male_pickup, game_board_positions, action_to_take, next_action = helper_functions.sarsa_learning(male, q_table_male_pickup, game_board_positions, learning_rate, discount_factor, policy_epsilon, 8000-steps, male_next_action)
                else:
                    q_table_male_pickup, game_board_positions, action_to_take = helper_functions.q_learning(current_policy, male, q_table_male_pickup, game_board_positions, learning_rate, discount_factor)
            else:
                heatmap_male_dropoff = helper_functions.update_heatmap(current_pos, heatmap_male_dropoff)
                if experiment_input == "2" or experiment_input == "4":
                    q_table_male_dropoff, game_board_positions, action_to_take, next_action = helper_functions.sarsa_learning(male, q_table_male_dropoff, game_board_positions, learning_rate, discount_factor, policy_epsilon, 8000-steps, male_next_action)
                else:
                    q_table_male_dropoff, game_board_positions, action_to_take = helper_functions.q_learning(current_policy, male, q_table_male_dropoff, game_board_positions, learning_rate, discount_factor)

            # Checks the males current position to see if it is in a dropoff/pickup position. If it is, then
            # we check to see if the agent is able to pickup/dropoff in the first place (like "Does the agent have
            # 1 block and is the dropoff spot not at full capacity?")
            
            # Checking if position is pickup spot
            if game_board_positions[current_pos_as_key]["pickup"] == True:
                # Checks to see if pickup action is possible
                if game_board_positions[current_pos_as_key]["special_block"].get_block_count() > 0 and male.get_block_count() == 0:
                    # Decreases the pickup spot's block count + updates the graphic that displays it's block count 
                    # while increasing the agent's block count
                    game_board_positions[current_pos_as_key]["special_block"].decrease_block_count()
                    game_board_positions[current_pos_as_key]["special_block"].update_symbol()
                    male.increase_block_count()
                    male.add_to_pickup_list()
                    heatmap_male_pickup = helper_functions.update_heatmap(current_pos, heatmap_male_pickup)
                    steps -= 1
                    male.increment_step()

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
                    male.add_to_dropoff_list()
                    heatmap_male_dropoff = helper_functions.update_heatmap(current_pos, heatmap_male_dropoff)
                    steps -= 1
                    male.dropoff_visit(current_pos, dropoff_positions)
                    male.increment_dropoff_count()
                    male.increment_step()

            # Sets the new position that the agent is one to be specified as occupied
            
            if action_to_take == "north":
                male.move_up()
            elif action_to_take == "south":
                male.move_down()
            elif action_to_take == "east":
                male.move_right()
            else:
                male.move_left()
            steps -= 1
            
            male.increment_step()
            
            current_pos = male.get_coor()
            current_pos_as_key = "{},{}".format(current_pos[0], current_pos[1])

            if male.get_coor() == female.get_coor():
                pygame.time.wait(1000)
                print("stacked")
            game_board_positions[current_pos_as_key]["occupied"] = True
            male_next_action = next_action
            male_turn_bool = False
            
        else:
            current_pos = female.get_coor()
            current_pos_as_key = "{},{}".format(current_pos[0], current_pos[1])

            # Sets the current position that the agent is one to not be occupied as the q learning function will move it to another position
            game_board_positions[current_pos_as_key]["occupied"] = False

            # Q learning algorithm returns updated q table, updated gmae board positions dictionary and the action of the agent to take
            # If the male has at least one block, we use the dropoff qtable. Otherwise we use pickup
            
            if female.get_block_count() == 0:
                heatmap_female_pickup = helper_functions.update_heatmap(current_pos, heatmap_female_pickup)
                if experiment_input == "2" or experiment_input == "4":
                    q_table_female_pickup, game_board_positions, action_to_take, next_action = helper_functions.sarsa_learning(female, q_table_female_pickup, game_board_positions, learning_rate, discount_factor, policy_epsilon,8000-steps, female_next_action)
                else:
                    q_table_female_pickup, game_board_positions, action_to_take = helper_functions.q_learning(current_policy, female, q_table_female_pickup, game_board_positions, learning_rate, discount_factor)
            else:
                heatmap_female_dropoff = helper_functions.update_heatmap(current_pos, heatmap_female_dropoff)
                if experiment_input == "2" or experiment_input == "4":
                    q_table_female_dropoff, game_board_positions, action_to_take, next_action = helper_functions.sarsa_learning(female, q_table_female_dropoff, game_board_positions, learning_rate, discount_factor, policy_epsilon, 8000-steps, female_next_action)
                else:
                    q_table_female_dropoff, game_board_positions, action_to_take = helper_functions.q_learning(current_policy, female, q_table_female_dropoff, game_board_positions, learning_rate, discount_factor)
                
                

            # Checks the males current position to see if it is in a dropoff/pickup position. If it is, then
            # we check to see if the agent is able to pickup/dropoff in the first place (like "Does the agent have
            # 1 block and is the dropoff spot not at full capacity?")
                         
            # Checking if position is pickup spot
            if game_board_positions[current_pos_as_key]["pickup"] == True:
                # Checks to see if pickup action is possible
                if game_board_positions[current_pos_as_key]["special_block"].get_block_count() > 0 and female.get_block_count() == 0:
                    # Decreases the pickup spot's block count + updates the graphic that displays it's block count 
                    # while increasing the agent's block count
                    game_board_positions[current_pos_as_key]["special_block"].decrease_block_count()
                    game_board_positions[current_pos_as_key]["special_block"].update_symbol()
                    female.increase_block_count()
                    female.add_to_pickup_list()
                    heatmap_female_pickup = helper_functions.update_heatmap(current_pos, heatmap_female_pickup)
                    steps -= 1
                    female.increment_step()

            # Checking if position is dropoff spot
            elif game_board_positions[current_pos_as_key]["dropoff"] == True:
                # Checks to see if dropoff action is possible
                if game_board_positions[current_pos_as_key]["special_block"].get_block_count() < game_board_positions[current_pos_as_key]["special_block"].get_capacity() \
                and female.get_block_count() == 1:
                    # Increases the dropoff spot's block count and updates the graphic that displays it's block count 
                    # while decreasing the agent's block count
                    game_board_positions[current_pos_as_key]["special_block"].increase_block_count()
                    game_board_positions[current_pos_as_key]["special_block"].update_symbol()
                    female.decrease_block_count()
                    female.add_to_dropoff_list()
                    heatmap_female_dropoff = helper_functions.update_heatmap(current_pos, heatmap_female_dropoff)
                    steps -= 1
                    female.dropoff_visit(current_pos, dropoff_positions)
                    female.increment_dropoff_count()
                    female.increment_step()

            if action_to_take == "north":
                female.move_up()
            elif action_to_take == "south":
                female.move_down()
            elif action_to_take == "east":
                female.move_right()
            else:
                female.move_left()
            
            steps -= 1

            female.increment_step()
            
            current_pos = female.get_coor()
            current_pos_as_key = "{},{}".format(current_pos[0], current_pos[1])

            game_board_positions[current_pos_as_key]["occupied"] = True
            female_next_action = next_action
            male_turn_bool = True

            if (8000-steps) == 500:
                pygame.time.wait(1000)
            
 
    # This is responsible for updating the graphics that represent the pickup and dropoff spots
    if helper_functions.check_dropoff_capacity(game_board_positions, dropoff_positions):
        helper_functions.write_run_stats(male, female, len(male.get_steps_list())+1, "exp-{}".format(experiment_input), dropoff_positions)
        male_next_action = ""
        female_next_action = ""
        male.add_steps_to_list()
        female.add_steps_to_list()
        male.add_blocking_to_list()
        female.add_blocking_to_list()
        time_array.append(time.time()-start_time)
        start_time = time.time()
        male, female, game_board_positions = helper_functions.reset_world(male, female, game_board_positions, pickup_positions, dropoff_positions, pickup_count, [male_start_position, female_start_position])
        for pos in pickup_positions:
            game_board_positions['{},{}'.format(pos[0], pos[1])]["special_block"].update_symbol()
        for pos in dropoff_positions:
            game_board_positions['{},{}'.format(pos[0], pos[1])]["special_block"].update_symbol()

        #Experiment 4 game conditions
    if(doing_experiment_4 and len(male.get_steps_list()) == 3):
        pickup_positions = new_pickup_positions #change the pickup positions if 3 games have been played
        for pos in pickup_positions:
            temp_pickup_block = PickupBlock(count=2, color=(50, 205, 50)) # Green
            temp_pickup_block.set_block_count(pickup_count)
            temp_pickup_block.update_symbol()
            temp_pickup_block.set_pos(pos)
            game_board_positions['{},{}'.format(pos[0], pos[1])]["special_block"] = temp_pickup_block
            game_board_positions['{},{}'.format(pos[0], pos[1])]["pickup"] = True
            game_board_positions['{},{}'.format(pos[0], pos[1])]["reward"] = 13

    if(doing_experiment_4 and len(male.get_steps_list()) == 6):
        steps = 0 #end the game if 6 games have been run
    
    if steps <= 0:
        test_bool = False
        game_bool = False
        if(experiment_input == '2' or experiment_input == '1c'):
            helper_functions.make_graphs_exp2(male,female,experiment_input)
        helper_functions.save_qtables_in_text_file(q_table_male_pickup, "exp-{}".format(experiment_input), "q_table_male_pickup.txt")
        helper_functions.save_qtables_in_text_file(q_table_male_dropoff, "exp-{}".format(experiment_input), "q_table_male_dropoff.txt")
        helper_functions.save_qtables_in_text_file(q_table_female_pickup, "exp-{}".format(experiment_input), "q_table_female_pickup.txt")
        helper_functions.save_qtables_in_text_file(q_table_female_dropoff, "exp-{}".format(experiment_input), "q_table_female_dropoff.txt")
        helper_functions.save_heatmaps_in_text_file(heatmap_male_dropoff, heatmap_male_pickup, heatmap_female_dropoff, heatmap_female_pickup, "exp-{}".format(experiment_input))

        helper_functions.generate_attractive_paths_image(win, male, female,
            game_board_positions, game_board,
            pickup_positions, dropoff_positions,
            q_table_male_pickup, q_table_male_dropoff,
            q_table_female_pickup, q_table_female_dropoff, './exp-{}/'.format(experiment_input))

        helper_functions.write_final_stats(male, female, "exp-{}".format(experiment_input), dropoff_positions)

    if steps > 8000 - helper_functions.experiment_settings[experiment_input][0][0]:
        current_policy = helper_functions.experiment_settings[experiment_input][0][1]
    else:
        current_policy = helper_functions.experiment_settings[experiment_input][1][1]

    if male.get_coor() == female.get_coor():
        same_pos_cnt += 1
    
    pygame.display.update()

pygame.quit()
