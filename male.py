import agent

class Male(agent.Agent):
    def __init__(self):
        self.symbol = agent.font.render("X", 1, (0, 0, 255))
        self.total_steps = 0;
        self.steps = 0
        self.dropoffs = 0
        self.terminal_state_steps = []

    def get_symbol(self):
        return self.symbol