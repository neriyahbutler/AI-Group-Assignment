import random

import numpy as np

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

def q_learning(mode, agent, q_table, state_map, learning_rate, discount_factor):
    agent_pos = agent.get_coor()
    actions = []
    
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
    val_to_use = 0
    best_action = ""
    action_to_perform = ""

    if mode == "PRandom":
        action_to_perform = random.choice(actions)
        val_to_use = q_table[agent_pos[0]][agent_pos[1]][action_to_perform]
    else:
        # Gets the agent with the max q value
        for action in actions:
            if max_val != max(max_val, q_table[agent_pos[0]][agent_pos[1]][action]):
                max_val = q_table[agent_pos[0]][agent_pos[1]][action]
                best_action = action

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



    print("Action choices are", actions)
    print("Current action is", action_to_perform)

    # Applys the q learning equation
    temporal_difference = state_map["{},{}".format(agent_pos[0], agent_pos[1])]["reward"] + discount_factor * val_to_use - q_table[agent_pos[0]][agent_pos[1]][action_to_perform]
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