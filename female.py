import agent

class Female(agent.Agent):
    def __init__(self):
        self.symbol = agent.font.render("O", 1, (255, 105, 180))
        self.total_steps = 0;
        self.steps = 0
        self.dropoffs = 0
        self.terminal_state_steps = []
        self.times_blocked = 0
        self.total_times_blocked = 0
        self.times_blocked_terminate = []

    def get_symbol(self):
        return self.symbol
    
    