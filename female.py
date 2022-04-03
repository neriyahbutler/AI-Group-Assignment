import agent

class Female(agent.Agent):
    def __init__(self):
        self.symbol = agent.font.render("O", 1, (255, 105, 180))

    def get_symbol(self):
        return self.symbol