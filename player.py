import pygame
from constants import *
from pygame.locals import *
import numpy as np

class Player(pygame.sprite.Sprite):
    def __init__(self, color=(255,255,0)) -> None:
        super().__init__()
        self.surf = pygame.Surface((BOXSIZE))
        self.surf.fill(color)
        self.rect = self.surf.get_rect()

        self.screen_pos = ... # position 
        self.block_pos = ... # position in NxN grid

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT]:
            self.check_move(self.block_pos + [[-1,0]])

        if pressed_keys[K_RIGHT]:
            self.check_move(self.block_pos + [[1,0]])

        if pressed_keys[K_UP]:
            self.check_move(self.block_pos + [[0,-1]])

        if pressed_keys[K_DOWN]:
            self.check_move(self.block_pos + [[0,1]])


    def check_move(self, pos):
        ...