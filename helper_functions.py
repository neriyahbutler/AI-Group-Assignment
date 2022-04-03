def set_points_pickup(points_map, points_to_change_arr):
    for point in points_to_change_arr:
        points_map[point]["pickup"] = True

    return points_map

def set_points_dropoff(points_map, points_to_change_arr):
    for point in points_to_change_arr:
        points_map[point]["dropoff"] = True

    return points_map

def q_learning(agent, q_table, state_map, learning_rate, discount_factor):
    agent_pos = agent.get_pos()
    actions = []
    pos_to_check = []
    
    if agent_pos[0] + 1 <= 4 and state_map["{},{}".format(agent_pos[0] + 1, agent_pos[1])]["occupied"] == False:
        actions.append("east")
        pos_to_check.append(agent_pos[0] + 1, agent_pos[1])
    if agent_pos[0] - 1 >= 0 and state_map["{},{}".format(agent_pos[0] + 1, agent_pos[1])]["occupied"] == False:
        actions.append("west")
        pos_to_check.append(agent_pos[0] - 1, agent_pos[1])
    if agent_pos[1] + 1 <= 4 and state_map["{},{}".format(agent_pos[0], agent_pos[1] + 1)]["occupied"] == False:
        actions.append("south")
        pos_to_check.append(agent_pos[0], agent_pos[1] + 1)
    if agent_pos[1] - 1 >= 0 and state_map["{},{}".format(agent_pos[0], agent_pos[1] - 1)]["occupied"] == False:
        actions.append("north")
        pos_to_check.append(agent_pos[0], agent_pos[1] - 1)
    
    # max_val = -1
    # curr_pos = ""
    # prev_max_val = max_val

    # for state in pos_to_check:
        # max_val = max(max_val, q_table[])