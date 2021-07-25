import pygame
import random
import numpy as np
from collections import deque
from AI_model import Dqn
import torch
class Agent:
    def __init__(self):
        self.gamma = 0.9
        self.dqn = Dqn(3,3,self.gamma)
        
        
    def get_action(self, last_reward, states, score):
        if score >= 3:
            self.result = self.dqn.update(last_reward, states)
        else: 
            if states[1] <= 0:
                self.result = 0
            elif states[0] <= 0:
                self.result = 1
            else:
                self.result = 2
        return self.result

    def get_score(self):
        return self.dqn.score()

    def get_state_1st_model(self, GRUf, GRLf, COLI, CR):
        #BOOLEAN STATES
        self.GRUf = GRUf
        self.GRLf = GRLf
        self.COLI = COLI
        self.CR = CR

        self.states = [False, False, False]

        if self.GRUf != 0 and self.GRLf != 0:
            self.states = [self.CR.top>self.GRUf.bottom, self.CR.bottom<self.GRLf.top, self.COLI[0]]
        return np.array(self.states, dtype=int)


    def get_state_2nd_model(self, GRUf, GRLf, COLI, CR):
        #BOOLEAN STATES
        self.GRUf = GRUf
        self.GRLf = GRLf
        self.COLI = COLI
        self.CR = CR

        self.states = [0,0,0]

        if self.GRUf != 0 and self.GRLf != 0:
            self.gate_frame_upper = self.CR.top - self.GRUf.bottom 
            self.gate_frame_lower = self.GRLf.top - self.CR.bottom
            self.length_between_cube_gate = self.GRUf.left - self.CR.right

            self.states = [self.gate_frame_upper, self.gate_frame_lower, self.length_between_cube_gate]
        return np.array(self.states, dtype=int)


    def remember(self, state_old, state_new, action, reward, done, points):
        self.memory.append((state_old, state_new, action, reward, done, points))

    def train_short_memory(self, state_old, satte_new, action, reward, done):
        self.trainer.train_step(state_old, satte_new, action, reward, done)

