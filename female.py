import agent

class Female(agent.Agent):
    def __init__(self):
        self.symbol = agent.font.render("O", 1, (255, 105, 180))
        self.total_steps = 0;
        self.steps = 0
        self.dropoffs = 0
        self.terminal_state_steps = []

    def get_symbol(self):
        return self.symbol
    
    