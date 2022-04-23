import os
import pygame

base_path = os.path.dirname(os.path.abspath(__file__))

font_path = os.path.join(base_path, "./font/Joystix.ttf")
font = pygame.font.Font(font_path, 35)


class Agent(object):
    x_move = 0
    y_move = 0

    block_count = 0

    movement = 40

    def move_left(self):
        if self.x_move != 0:
            self.x_move -= 1

    def move_right(self):
        if self.x_move != 4:
            self.x_move += 1

    def move_down(self):
        if self.y_move != 4:
            self.y_move += 1
            
    def move_up(self):
        if self.y_move != 0:
            self.y_move -= 1

    def get_pos(self):
        return [150 + self.x_move * self.movement, 140 + self.y_move * self.movement]

    def get_coor(self):
        return [self.x_move, self.y_move]

    def set_coor(self, pos):
        self.x_move = pos[0]
        self.y_move = pos[1]

    def set_block_count(self, block_count):
        self.block_count = block_count

    def get_block_count(self):
        return self.block_count

    def increase_block_count(self):
        self.block_count += 1

    def decrease_block_count(self):
        self.block_count -= 1
    
    ####
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

    def get_blocked_counter(self):
        return self.times_blocked

    def get_total_blocked_counter(self):
        return self.total_times_blocked

    def get_blocked_list(self):
        return self.times_blocked_terminate

    def increment_blocked_counter(self):
        self.times_blocked += 1

    def add_blocking_to_list(self):
        self.times_blocked_terminate.append(self.times_blocked)
        self.total_times_blocked += self.times_blocked
        self.times_blocked = 0
