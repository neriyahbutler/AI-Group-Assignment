import agent

class Male(agent.Agent):
    def __init__(self):
        self.symbol = agent.font.render("X", 1, (0, 0, 255))
        self.total_steps = 0
        self.steps = 0
        self.dropoffs = 0
        self.total_dropoffs = 0
        self.steps_to_pick_up = []
        self.steps_to_dropoff = []
        self.terminal_state_steps = []
        self.times_blocked = 0
        self.step_blocked_at = []
        self.total_times_blocked = 0
        self.times_blocked_terminate = []

    def get_symbol(self):
        return self.symbol
