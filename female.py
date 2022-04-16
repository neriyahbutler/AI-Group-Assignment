import agent

class Female(agent.Agent):
    def __init__(self):
        self.symbol = agent.font.render("O", 1, (255, 105, 180))
        self.steps = 0

    def get_symbol(self):
        return self.symbol
    
    def increment_step(self):
        self.steps += 1
    
    def get_Step(self):
        return self.steps    