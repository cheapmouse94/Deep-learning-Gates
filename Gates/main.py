import numpy as np
import gym
import pygame
import os
import sys
from collections import deque
import random
from prop_player import Cube, Score
from prop_gates import Gates
from AI_agent import Agent
from results import Plot

FPS = 60
SQM = 64
GATES_CLASSES = []
GATES_RECT_UPPER = []
GATES_RECT_LOWER = []
GATES_RECT_LINES = []
CUBE_RECT = []
AI_STATIC_RECT = []

class Engine():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('ML passing through gates')
        self.frame_counter = 0
        self.score_counter = 0
        self.punishments = 0
        self.last_reward = 0
        self.step_between_gates = 150
        self.resolution = (SQM*13,SQM*10)
        self.window = pygame.display.set_mode(self.resolution)
        self.score = Score(self.resolution)
        self.agent = Agent()
        self.plot = Plot()
        self.clock = pygame.time.Clock()
        self.cube = Cube(SQM)
        
        self.control_by_human = False
        self.control_by_AI = True
        self.gates_avaible = False

    def runtime(self):
        self.run = True
        while self.run:
            self.window.fill((0,0,0))
            CUBE_RECT = self.cube.draw(self.window)
            GATES_RECT_UPPER, GATES_RECT_LOWER, GATES_RECT_LINES = self.generating_gates()

            self.cube_collisions_state = self.cube.collisions(self.resolution, CUBE_RECT ,GATES_RECT_UPPER, GATES_RECT_LOWER, GATES_RECT_LINES)

            self.gate_rect_upper_focus, self.gate_rect_lower_focus, self.gate_rect_line_focus = self.cube.focus_on_gate(CUBE_RECT, GATES_RECT_UPPER, GATES_RECT_LOWER, GATES_RECT_LINES) 
            self.score_counter = self.score.calculate_score(self.score_counter, self.cube_collisions_state[2])
            self.score.draw(self.window, self.score_counter)

            self.cube_gate_trigger_once_logic = self.cube.cube_gate_trigger_once(self.cube_collisions_state)
            self.cube_line_trigger_once_logic = self.cube.cube_line_trigger_once(self.cube_collisions_state)

            self.get_state_1st_model_states_old = self.agent.get_state_1st_model(self.gate_rect_upper_focus, self.gate_rect_lower_focus, self.cube_collisions_state, CUBE_RECT)
            self.get_state_2nd_model_states_old = self.agent.get_state_2nd_model(self.gate_rect_upper_focus, self.gate_rect_lower_focus, self.cube_collisions_state, CUBE_RECT)
            self.action_= self.agent.get_action(self.last_reward, self.get_state_2nd_model_states_old, self.score_counter)

            self.cube.move_by_Human(self.control_by_human)
            self.last_reward, done, self.punishments = self.cube.play_step(self.control_by_AI, 
                self.action_,
                self.cube_gate_trigger_once_logic,
                self.cube_line_trigger_once_logic,
                self.cube_collisions_state,
                self.score_counter,
                self.get_state_1st_model_states_old,
                self.punishments)

            
            self.mean_reward = self.agent.get_score()
            self.remove_gate_on_trigger(self.cube_gate_trigger_once_logic)
            self.run = self.plot.generate_results(self.frame_counter, self.score_counter, self.mean_reward, self.punishments)

            pygame.display.update()
            self.clock.tick(FPS)
            self.frame_counter += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

    def generating_gates(self):
        self.gru = []
        self.grl = []
        self.lines = []
        if self.frame_counter % self.step_between_gates == 0: 
            self.gates = Gates(SQM, self.resolution)
            GATES_CLASSES.append(self.gates)
            self.gates_avaible = True

        if self.gates_avaible:
            for i in GATES_CLASSES:
                self.gate_upper_rect, self.gate_lower_rect, self.pass_lines = i.draw(self.window)
                self.gru.append(self.gate_upper_rect)
                self.grl.append(self.gate_lower_rect)
                self.lines.append(self.pass_lines)
                i.move()
                if i.x_upper <= -SQM*3:
                    del GATES_CLASSES[0]
        return self.gru, self.grl, self.lines

    def remove_gate_on_trigger(self, flag):
        if flag:
            del GATES_CLASSES[0]
                    
    
if __name__ == '__main__':
    engine = Engine()
    engine.runtime()