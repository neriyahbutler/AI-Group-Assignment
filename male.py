import agent
import numpy as np

class Male(agent.Agent):
    def __init__(self):
        self.symbol = agent.font.render("X", 1, (0, 0, 255))
        self.total_steps = 0
        self.steps = 0
        self.dropoffs = 0
        self.dropoffs_list = []
        self.total_dropoffs = 0
        self.steps_to_pick_up = []
        self.steps_to_dropoff = []
        self.terminal_state_steps = []
        self.times_blocked = 0
        self.step_blocked_at = []
        self.total_times_blocked = 0
        self.times_blocked_terminate = []
        self.visits = np.zeros((4, 1), dtype=int)
        self.total_visits = np.zeros((4, 1), dtype=int)

    def get_symbol(self):
        return self.symbol
