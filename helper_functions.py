import numpy as np

def set_points_pickup(points_map, points_to_change_arr):
    for point in points_to_change_arr:
        points_map[point]["pickup"] = True

    return points_map


def set_points_dropoff(points_map, points_to_change_arr):
    for point in points_to_change_arr:
        points_map[point]["dropoff"] = True

    return points_map


def q_learning(agent, q_table, state_map, learning_rate, discount_factor):
    agent_pos = agent.get_coor()
    actions = []
    
    if agent_pos[0] + 1 <= 4 and state_map["{},{}".format(agent_pos[0] + 1, agent_pos[1])]["occupied"] == False:
        actions.append("east")
    if agent_pos[0] - 1 >= 0 and state_map["{},{}".format(agent_pos[0] + 1, agent_pos[1])]["occupied"] == False:
        actions.append("west")
    if agent_pos[1] + 1 <= 4 and state_map["{},{}".format(agent_pos[0], agent_pos[1] + 1)]["occupied"] == False:
        actions.append("south")
    if agent_pos[1] - 1 >= 0 and state_map["{},{}".format(agent_pos[0], agent_pos[1] - 1)]["occupied"] == False:
        actions.append("north")
        
    max_val = -1
    prev_max_val = max_val
    action_index_holder = ["north", "south", "west", "east"]
    action_to_perform = ""

    for action in actions:
        max_val = max(max_val, q_table[agent_pos[0]][agent_pos[1]][action])
        if max_val != prev_max_val:
            prev_max_val = max_val
            action_to_perform = action

    print("Best chosen position is", action_to_perform)

    temporal_difference = state_map["{},{}".format(agent_pos[0], agent_pos[1])]["reward"] + discount_factor * max_val - q_table[agent_pos[0]][agent_pos[1]][action_to_perform]
    new_q_value = q_table[agent_pos[0]][agent_pos[1]][action_to_perform] + learning_rate * temporal_difference

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