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
    
    def increment_step(self):
        self.steps += 1
    
    def get_steps(self):
        return self.steps
    
    def increment_dropoff_count(self):
        self.dropoffs += 1
    
    def get_dropoffs(self):
        return self.dropoffs
    
    def add_steps_to_list(self):
        self.terminal_state_steps.append(self.steps)
        self.total_steps += self.steps
        self.steps = 0
    
    def get_total_steps(self):
        return self.total_steps
    
    def get_steps_list(self):
        return self.terminal_state_steps
    
    def get_avg_steps_per_terminal_state(self):
        total = 0
        for i in range(len(self.terminal_state_steps)):
            total += self.terminal_state_steps[i]
        
        return total/len(self.terminal_state_steps)