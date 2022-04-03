import agent

class Male(agent.Agent):
    def __init__(self):
        self.symbol = agent.font.render("X", 1, (0, 0, 255))

    def get_symbol(self):
        return self.symbol
    
