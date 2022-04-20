import random

import numpy as np
import random
from datetime import datetime

import os
import pygame

import math

base_path = os.path.dirname(os.path.abspath(__file__))

font_path = os.path.join(base_path, "./font/Joystix.ttf")
font = pygame.font.Font(font_path, 35)

font_details = pygame.font.Font(font_path, 12)


def set_points_pickup(points_map, points_to_change_arr):
    for point in points_to_change_arr:
        points_map[point]["pickup"] = True

    return points_map


def set_points_dropoff(points_map, points_to_change_arr):
    for point in points_to_change_arr:
        points_map[point]["dropoff"] = True

    return points_map

def policy_verify(current_policy):
    if not isinstance(current_policy, (str)):
        return False
    elif current_policy == "PRandom":
        return True
    elif current_policy == "PExploit":
        return True
    elif current_policy == "PGreedy":
        return True
    else:
        return False

def step_verify(steps):
    if not isinstance(steps, int):
        return False
    elif steps < 1:
        return False
    else:
        return True

def return_position_reward(agent, pos_in_state_map):
    if pos_in_state_map["pickup"] == True:
        if pos_in_state_map["special_block"].get_block_count() > 0 and agent.get_block_count() == 0:
            return 13
    elif pos_in_state_map["dropoff"] == True:
        if pos_in_state_map["special_block"].get_block_count() < pos_in_state_map["special_block"].get_capacity() and agent.get_block_count() == 1:
            return 13
    return -1


def q_learning(mode, agent, q_table, state_map, learning_rate, discount_factor):
    agent_pos = agent.get_coor()
    actions = []
    
    # Checks to see what actions are possible for the current agent
    if agent_pos[0] < 4 and state_map["{},{}".format(agent_pos[0] + 1, agent_pos[1])]["occupied"] == False:
        actions.append("east")
    if agent_pos[0] > 0 and state_map["{},{}".format(agent_pos[0] - 1, agent_pos[1])]["occupied"] == False:
        actions.append("west")
    if agent_pos[1] < 4 and state_map["{},{}".format(agent_pos[0], agent_pos[1] + 1)]["occupied"] == False:
        actions.append("south")
    if agent_pos[1] > 0 and state_map["{},{}".format(agent_pos[0], agent_pos[1] - 1)]["occupied"] == False:
        actions.append("north")
        
    max_val = -99
    prev_max_val = max_val
    val_to_use = 0
    best_action = ""
    action_to_perform = ""

    duplicate_actions = [best_action]

    # Gets the agent with the max q value while collecting a list of actions 
    # that have duplicate q values
    for action in actions:
        max_val = max(max_val, q_table[agent_pos[0]][agent_pos[1]][action])
        if max_val > prev_max_val:
            prev_max_val = max_val
            best_action = action
            duplicate_actions = [best_action]
        elif max_val == q_table[agent_pos[0]][agent_pos[1]][action]:
            duplicate_actions.append(action)
        
    if len(duplicate_actions) > 1 and max_val == prev_max_val:
        best_action = random.choice(duplicate_actions)


    if mode == "PRandom":
        action_to_perform = random.choice(actions)
        val_to_use = q_table[agent_pos[0]][agent_pos[1]][action_to_perform]
    else:
        if mode == "PGreedy":
            action_to_perform = best_action
            val_to_use = max_val

        elif mode == "PExploit":
            other_actions = actions.remove(best_action)
            random_action = random.choice(other_actions)
            random_val = q_table[agent_pos[0]][agent_pos[1]][random_action]

            exploit_choice = random.randint(1,100)
            if exploit_choice <= 80:
                action_to_perform, val_to_use = best_action, max_val
            else:
                action_to_perform, val_to_use = random_action, random_val

    # If there's more than one action with the assigned max q value, we randomly
    # pick an action to use
    if len(duplicate_actions) > 1:
        action_to_perform = random.choice(duplicate_actions)

    # Applys the q learning equation
    temp_reward = -1

    # Checks to see if current position is a pickup spot or dropoff spot
    # If so, it checks to see if it should give a reward of 13 if it's able to
    # dropoff/pickup a block
    if state_map["{},{}".format(agent_pos[0], agent_pos[1])]["pickup"] == True or state_map["{},{}".format(agent_pos[0], agent_pos[1])]["dropoff"] == True:
        temp_reward = return_position_reward(agent, state_map["{},{}".format(agent_pos[0], agent_pos[1])])
        
    temporal_difference = temp_reward + discount_factor * val_to_use - q_table[agent_pos[0]][agent_pos[1]][action_to_perform]
    new_q_value = q_table[agent_pos[0]][agent_pos[1]][action_to_perform] + learning_rate * temporal_difference

    q_table[agent_pos[0]][agent_pos[1]][action_to_perform] = new_q_value

    # Returns updated q table, updated map containing the information about each point, as well as the action that is to be performed by the agent
    return q_table, state_map, action_to_perform

def sarsa_learning(agent, q_table, state_map, learning_rate, discount_factor, policy,steps):
    agent_pos = agent.get_coor()
    actions = []
    print("steps: " + str(steps))
    
    print("\nCurrent pos is {}, {}".format(agent_pos[0], agent_pos[1]))
    
    # Checks to see what actions are possible for the current agent
    if agent_pos[0] < 4 and state_map["{},{}".format(agent_pos[0], agent_pos[1])]["occupied"] == False:
        actions.append("east")
    if agent_pos[0] > 0 and state_map["{},{}".format(agent_pos[0], agent_pos[1])]["occupied"] == False:
        actions.append("west")
    if agent_pos[1] < 4 and state_map["{},{}".format(agent_pos[0], agent_pos[1])]["occupied"] == False:
        actions.append("south")
    if agent_pos[1] > 0 and state_map["{},{}".format(agent_pos[0], agent_pos[1])]["occupied"] == False:
        actions.append("north")
        
    max_val = -99
    prev_max_val = max_val
    val_to_use = 0
    best_action = ""
    action_to_perform = ""

    duplicate_actions = [best_action]

    # Gets the agent with the max q value while collecting a list of actions 
    # that have duplicate q values
    for action in actions:
        max_val = max(max_val, q_table[agent_pos[0]][agent_pos[1]][action])
        if max_val != prev_max_val:
            prev_max_val = max_val
            best_action = action
            duplicate_actions = [best_action]
        else:
            duplicate_actions.append(action)
        
    if len(duplicate_actions) > 1:
        best_action = random.choice(duplicate_actions)

    print("max action :" + best_action + "\n max val: " + str(max_val))
    print("Action choices are", actions)
    #if policy = .8 then 80% of the time algorithm would pick max_val
    random.seed(datetime.now())
    randomgen = random.uniform(0,1)
    #print("PRANDOM active")
    
    print("policy is " + str(policy) + "\n probability is: " + str(randomgen))
    if randomgen < policy:
        actions.remove(best_action)
        Next_val, action_to_perform = random_action(actions,q_table,agent_pos)
    else:
        Next_val = max_val
        action_to_perform = best_action
    
    
    print("Current action is", action_to_perform)
    
    #apply q learning equation
    temporal_difference = state_map["{},{}".format(agent_pos[0], agent_pos[1])]["reward"] + discount_factor * Next_val - q_table[agent_pos[0]][agent_pos[1]][action_to_perform]
    new_q_value = q_table[agent_pos[0]][agent_pos[1]][action_to_perform] + learning_rate * temporal_difference
    
    return q_table, state_map, action_to_perform

    
def random_action(actions, q_table, agent_pos):
    num = len(actions)
    
    random.seed(datetime.now())
    index = random.randrange(0,num)
    
    
    
    return q_table[agent_pos[0]][agent_pos[1]][actions[index]], actions[index]

def generate_qtable():
    q_table = []

    for x in range(0, 5):
        q_table.append([])
        for y in range(0, 5):
            q_table[x].append({
                "north": 0,
                "south": 0,
                "east": 0,
                "west": 0
            })

    return q_table


def check_dropoff_capacity(state_map, dropoff_pos):
    for pos in dropoff_pos:
        if state_map['{},{}'.format(pos[0], pos[1])]["special_block"].get_capacity() != state_map['{},{}'.format(pos[0], pos[1])]["special_block"].get_block_count():
            return False
    return True


def reset_world(male, female, state_map, pickup_positions, dropoff_positions, pickup_max_count, init_positions):
    # Resets the block count for the pickup spots
    for pos in pickup_positions:
        state_map['{},{}'.format(pos[0], pos[1])]["special_block"].set_block_count(pickup_max_count)

    # Resets block count back to 0 for the dropoff spots
    for pos in dropoff_positions:
        state_map['{},{}'.format(pos[0], pos[1])]["special_block"].set_block_count(0)

    for key in state_map:
        state_map[key]["occupied"] = False

    # Resets the agent's position back to its initial spot
    male.set_block_count(0)
    male.set_coor(init_positions[0])
    state_map["{},{}".format(init_positions[0][0], init_positions[0][1])]["occupied"] = True

    female.set_block_count(0)
    female.set_coor(init_positions[1])
    state_map["{},{}".format(init_positions[1][0], init_positions[1][1])]["occupied"] = True

    return male, female, state_map


def display_game_details(male, female, dropoff_capacity, pickup_capacity, window):
    male_count = font_details.render("Male block count = {}".format(male.get_block_count()), 1, (255, 255, 255))
    female_count = font_details.render("Female block count = {}".format(female.get_block_count()), 1, (255, 255, 255))

    dropoff_capacity_details = font_details.render("Dropoff capacity = {}".format(dropoff_capacity), 1, (255, 255, 255))
    pickup_capacity_details = font_details.render("Pickup max count = {}".format(pickup_capacity), 1, (255, 255, 255))

    male_details = font_details.render("Male = Blue", 1, (0, 0, 255))
    female_details = font_details.render("Female = Pink", 1, (255, 105, 180))
    pickup_details = font_details.render("Pickup = Green", 1, (50, 205, 50))
    dropoff_details = font_details.render("Dropoff = Purple", 1, (138, 43, 226))

    window.blit(male_count, (20,420))
    window.blit(female_count, (20, 440))

    window.blit(dropoff_capacity_details, (280, 420))
    window.blit(pickup_capacity_details, (280, 440))

    window.blit(pickup_details, (80, 40))
    window.blit(dropoff_details, (80, 60))
    window.blit(male_details, (290, 40))
    window.blit(female_details, (290, 60))


def draw_arrow(screen, color, start, end):
    pygame.draw.line(screen, color, start, end, 2)
    rotation = math.degrees(math.atan2(start[1]-end[1], end[0]-start[0])) + 90
    pygame.draw.polygon(screen, color, ((end[0] + 5 * math.sin(math.radians(rotation)), end[1] + 5 * math.cos(math.radians(rotation))), (end[0] + 5 * math.sin(math.radians(rotation - 120)), end[1]+ 5 *math.cos(math.radians(rotation-120))), (end[0]+ 5 *math.sin(math.radians(rotation+120)), end[1]+ 5 *math.cos(math.radians(rotation+120)))))


def calculate_new_pos(action, pos):
    x = pos[0]
    y = pos[1]

    if action == "north":
        return ((165 + x * 40), (155 + (y - 0.25) * 40))
    if action == "south":
        return ((165 + x * 40), (155 + (y + 0.25) * 40))
    if action == "east":
        return ((165 + (x + 0.25) * 40), (155 + y * 40))
    return ((165+ (x - 0.25) * 40), (155 + y * 40))


def display_arrows(win, q_table):
    for x in range(0, len(q_table)):
        for y in range(0, len(q_table)):
            actions = []
            if x != 0:
                actions.append("west")
            if y != 0:
                actions.append("north")
            if x != 4:
                actions.append("east")
            if y != 4:
                actions.append("south")

            if len(actions) > 0:
                max_val = -99
                prev_max_val = max_val
                duplicate_actions = [max_val]

                for action in actions:
                    max_val = max(max_val, q_table[x][y][action])
                    if max_val > prev_max_val:
                        prev_max_val = max_val
                        best_action = action
                        duplicate_actions = [best_action]
                    elif max_val == q_table[x][y][action]:
                        duplicate_actions.append(action)

                if len(duplicate_actions) > 1:
                    for action in duplicate_actions:
                        pos_after_action = calculate_new_pos(action, (x, y))
                        draw_arrow(win, (255, 0, 0), ((165 + x * 40), (155 + y * 40)), pos_after_action)
                else:
                    pos_after_action = calculate_new_pos(best_action, (x,y))
                    draw_arrow(win, (255, 0, 0), ((165 + x * 40), (155 + y * 40)), pos_after_action)


def display_dropoff_pickup_locations(win, pickup_positions, dropoff_positions, state_map):
    for pos in pickup_positions:
            win.blit(
                state_map['{},{}'.format(pos[0], pos[1])]["special_block"].get_symbol(),
                state_map['{},{}'.format(pos[0], pos[1])]["special_block"].get_pos()
            )

    for pos in dropoff_positions:
        win.blit(
            state_map['{},{}'.format(pos[0], pos[1])]["special_block"].get_symbol(),
            state_map['{},{}'.format(pos[0], pos[1])]["special_block"].get_pos()
        )


def display_male_female_agents(win, male, female):
    win.blit(male.get_symbol(), male.get_pos())
    win.blit(female.get_symbol(), female.get_pos())


def display_game_board(win, game_board):
    win.blit(game_board, (125, 125))


def generate_attractive_paths_image(win, male, female, state_map, game_board, 
            pickup_positions, dropoff_positions, 
            q_table_male_pickup, q_table_male_dropoff, 
            q_table_female_pickup, q_table_female_dropoff, path="./test/"):

        print("Male Q-Table Dropoff\n", q_table_male_dropoff, "\n")
        print("Male Q-Table Pickup\n", q_table_male_pickup, "\n")

        print("Female Q-Table Dropoff\n", q_table_female_dropoff, "\n")
        print("Female Q-Table Pickup\n", q_table_female_pickup, "\n")
        
        display_dropoff_pickup_locations(win, pickup_positions, dropoff_positions, state_map)
        display_arrows(win, q_table_male_pickup)

        pygame.image.save(win, "{}attractive_paths_pickup_male.jpeg".format(path))

        display_game_board(win, game_board)
        display_dropoff_pickup_locations(win, pickup_positions, dropoff_positions, state_map)
        display_male_female_agents(win, male, female)
        display_arrows(win, q_table_male_dropoff)

        pygame.image.save(win, "{}attractive_paths_dropoff_male.jpeg".format(path))

        display_game_board(win, game_board)
        display_dropoff_pickup_locations(win, pickup_positions, dropoff_positions, state_map)
        display_male_female_agents(win, male, female)
        display_arrows(win, q_table_female_pickup)

        pygame.image.save(win, "{}attractive_paths_pickup_female.jpeg".format(path))
        

        display_game_board(win, game_board)
        display_dropoff_pickup_locations(win, pickup_positions, dropoff_positions, state_map)
        display_male_female_agents(win, male, female)
        display_arrows(win, q_table_female_dropoff)

        pygame.image.save(win, "{}attractive_paths_dropoff_female.jpeg".format(path))


def save_qtables_in_text_file(q_table, filedir="test", filename="test.txt"):
    try:
        os.mkdir(filedir)
    except:
        print("Directory {} already exists, saving file there".format(filedir))
    updated_filedir = "./{}/{}".format(filedir, filename)
    with open(updated_filedir, "w") as f:
        for x in range(0, len(q_table)):
            for y in range(0, len(q_table)):
                f.write("({}, {}) = {}\n".format(x, y, q_table[x][y]))