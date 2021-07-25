import sys
import pygame
import numpy as np
import random

class Gates(object):
    def __init__(self, SQM, res):
        self.SQM = SQM
        self.res = res
        self.crack = 3*self.SQM
        self.rand_crack = random.randrange(self.SQM, res[1]-self.SQM-self.crack)
        #Górna ścianka
        self.x_upper = res[0]-self.SQM
        self.y_upper = 0

        #Dolna ścianka
        self.x_lower = res[0]-self.SQM
        self.y_lower = self.rand_crack + self.crack

    def draw(self, win):
        self.gate_upper_rect = pygame.Rect(self.x_upper, self.y_upper, self.SQM, self.rand_crack)
        self.gate_lower_rect = pygame.Rect(self.x_lower, self.y_lower, self.SQM, self.res[1]-self.crack-self.rand_crack)  
        self.pass_lines = pygame.Rect(self.x_upper+self.SQM, self.rand_crack,1,self.crack)
        pygame.draw.rect(win, (255, 255, 255), self.gate_upper_rect)
        pygame.draw.rect(win, (255, 255, 255), self.gate_lower_rect)
        pygame.draw.rect(win, (51, 51, 255), self.pass_lines)

        return self.gate_upper_rect, self.gate_lower_rect, self.pass_lines

    def move(self):
        self.x_upper -= 4
        self.x_lower -= 4
