import sys
import pygame
from pygame.math import Vector2
import torch

class Cube(object):
    def __init__(self, SQM):
        self.SQM = SQM
        self.x = SQM*1
        self.y = SQM*6

        self.pos = Vector2(self.x,self.y)
        self.vel = Vector2(0,0)
        self.acc = Vector2(0,0)

        self.Trigger_once_gates = True
        self.Trigger_once_lines = True

    def add_force(self, force):
        self.acc += force

    def move_by_Human(self, enable_HM):
        if enable_HM:
            key_bind = pygame.key.get_pressed()
            if key_bind[pygame.K_w]:
                self.add_force(Vector2(0,-6))
            if key_bind[pygame.K_s]:
                self.add_force(Vector2(0,6))         
            self.vel *= 0
            self.vel += self.acc
            self.pos += self.vel
            self.acc *= 0

    def move_by_AI(self, enable_AI, action):
        if enable_AI:
            if action == 0:
                self.add_force(Vector2(0,-6))
            if action == 1:
                self.add_force(Vector2(0,6))
            if action == 2:
                #Bezczynność
                pass         
            self.vel *= 0.1
            self.vel += self.acc
            self.pos += self.vel
            self.acc *= 0

    def wall_collisions(self, res):
        if self.pos.y < 0:
            self.pos.y = 0
            return True
        elif self.pos.y > res[1]-self.SQM:
            self.pos.y = res[1]-self.SQM
            return True
        return False

    def gate_collisions(self, CR, GRU, GRL):
        self.GR = GRU + GRL
        for n in self.GR:
            if CR.colliderect(n):
                return True
        return False

    def line_collisions(self, CR, CRLN):
        for n in CRLN:
            if CR.colliderect(n):
                return True
        return False

    def focus_on_gate(self, CR, GRU, GRL, GRLN):
        cube_right = CR.right
        cube_left = CR.left
        gru_focus = grl_focus = grln_focus = 0

        for x in GRU:
            if cube_left < x.right:
                gru_focus = x
                break

        for x in GRL:
            if cube_left < x.right:
                grl_focus = x
                break

        for x in GRLN:
            if cube_left < x.right:
                grln_focus = x
                break
        return gru_focus, grl_focus, grln_focus 

    def collisions(self, res, CR, GRU, GRL, GRLN):
        wall_collision_state = self.wall_collisions(res)
        gate_collision_state = self.gate_collisions(CR, GRU, GRL)
        line_collision_state = self.line_collisions(CR, GRLN)
        return [wall_collision_state, gate_collision_state, line_collision_state]

    def play_step(self, enable_AI, action, trigger_gate, trigger_line, collisions, SCORE, logic_colison, punishments):
        self.move_by_AI(enable_AI, action)
        PUNISHMENTS = punishments
        REWARD = 0
        GAME_OVER = False
        if collisions[0]:
            REWARD = -2
            print("KARA -2")
        if logic_colison[0] is False or logic_colison[1] is False:
            REWARD = -1
        if trigger_gate:
            REWARD = -10
            GAME_OVER = True
            PUNISHMENTS += 1
            print("KARA -10")
        if trigger_line:
            REWARD = 100
            print("NAGRODA +100")
        
        return REWARD, GAME_OVER, PUNISHMENTS
        
    def cube_gate_trigger_once(self, coli):
        self.coli = coli[1]
        if self.coli and self.Trigger_once_gates:
            self.Trigger_once_gates = False
            return True
        elif self.coli is False:
            self.Trigger_once_gates = True
            return False
     
    def cube_line_trigger_once(self, coli):
        self.coli = coli[2]
        if self.coli and self.Trigger_once_lines:
            self.Trigger_once_lines = False
            return True
        elif self.coli is False:
            self.Trigger_once_lines = True
            return False


    def draw(self, win):
        self.cube_rect = pygame.Rect(self.pos.x, self.pos.y, self.SQM, self.SQM)
        pygame.draw.rect(win, (255, 0, 0), self.cube_rect)
        return self.cube_rect
        

class Score(object):
    def __init__(self, res):
        self.res = res
        self.font_1 = pygame.font.SysFont('Comic Sans MS', 28)
        self.Trigger_once = True

    def draw(self, win, score):
        self.text_score = 'Score = {}'
        self.text_score_full = self.text_score.format(score)
        textsurface = self.font_1.render(self.text_score_full, True, (255, 255, 255))
        win.blit(textsurface,(0,0))

    def calculate_score(self, score, state):
        if state and self.Trigger_once:
            self.Trigger_once = False
            score += 1
        elif state is False:
            self.Trigger_once = True
        return score

