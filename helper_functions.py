from turtle import pos
import numpy as np
import random

def set_points_pickup(points_map, points_to_change_arr):
    for point in points_to_change_arr:
        points_map[point]["pickup"] = True

    return points_map


def set_points_dropoff(points_map, points_to_change_arr):
    for point in points_to_change_arr:
        points_map[point]["dropoff"] = True

    return points_map


def return_position_reward(agent, pos_in_state_map):
    if pos_in_state_map["pickup"] == True:
        if pos_in_state_map["special_block"].get_block_count() > 0 and agent.get_block_count() == 0:
            return 13
    elif pos_in_state_map["dropoff"] == True:
        if pos_in_state_map["special_block"].get_block_count() < pos_in_state_map["special_block"].get_capacity() and agent.get_block_count() == 1:
            return 13

    return -1


def q_learning(agent, q_table, state_map, learning_rate, discount_factor):
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
    action_to_perform = ""

    duplicate_actions = [action_to_perform]

    # Gets the agent with the max q value while collecting a list of actions 
    # that have duplicate q values
    for action in actions:
        max_val = max(max_val, q_table[agent_pos[0]][agent_pos[1]][action])
        if max_val != prev_max_val:
            prev_max_val = max_val
            action_to_perform = action
            duplicate_actions = [action_to_perform]
        else:
            duplicate_actions.append(action)

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

    if action_to_perform == '':
        print("ACTION TO PERFORM IS BLANK!\n")
        print("Position of the agent: {}\n".format(agent.get_coor()))
        print("The list of actions:", actions)
        print("The state map:\n", state_map)

    temporal_difference = temp_reward + discount_factor * max_val - q_table[agent_pos[0]][agent_pos[1]][action_to_perform]
    new_q_value = q_table[agent_pos[0]][agent_pos[1]][action_to_perform] + learning_rate * temporal_difference

    q_table[agent_pos[0]][agent_pos[1]][action_to_perform] = new_q_value

    # Returns updated q table, updated map containing the information about each point, as well as the action that is to be performed by the agent
    return q_table, state_map, action_to_perform


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

    female.set_block_count(0)
    female.set_coor(init_positions[1])

    return male, female, state_map