import pygame
from pygame.locals import *
import numpy as np


"""EFFICIENCY SECOND SAKETH"""

NXNSIZE = 4

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class GameInstance:
    def __init__(self) -> None:
        self.size = NXNSIZE
        self.obs_list = []  # List of randomly generated obstacles
        self.player_list = []  # List of player objects
        self.player_pos_list = []  # List of player positions

    def step(self):
        for player in self.player_list:
            player.move(self.player_list, self.player_list)

        check_victory(self.player_list)


class Player:
    def __init__(self, key_left, key_right, key_up, key_down) -> None:
        self.goal_pos = np.random.randint(0, 4, (2, 1))  # I think coordinates are 2x1??
        self.start_pos = np.random.randint(
            0, 4, (2, 1)
        )  # yes things can start at their goals get over it
        self.pos = self.start_pos
        # self.movementKeys = [key_left, key_right, key_up, key_down]
        self.key_left = key_left
        self.key_right = key_right
        self.key_up = key_up
        self.key_down = key_down

    def move(self, obs_list, player_list):
        # for now they can just only move in one direction???
        pressed_keys = pygame.key.getpressed()
        if pressed_keys[self.key_left]:
            if checkMove(obs_list, player_list, self.pos, LEFT):
                self.pos = self.pos + np.array(LEFT)
        if pressed_keys[self.key_right]:
            if checkMove(obs_list, player_list, self.pos, RIGHT):
                self.pos = self.pos + np.array(RIGHT)
        if pressed_keys[self.key_up]:
            if checkMove(obs_list, player_list, self.pos, UP):
                self.pos = self.pos + np.array(UP)
        if pressed_keys[self.key_down]:
            if checkMove(obs_list, player_list, self.pos, DOWN):
                self.pos = self.pos + np.array(DOWN)


def checkMove(obs_list, player_list, pos, direction):
    if direction == LEFT and pos[0] == 0:
        return False
    if direction == RIGHT and pos[0] == NXNSIZE - 1:
        return False
    if direction == UP and pos[1] == 0:
        return False
    if direction == DOWN and pos[1] == NXNSIZE - 1:
        return False

    pos_after_move = pos + np.array(direction)

    n_players_on_spot = 0
    for obs in obs_list:
        if obs == pos_after_move:
            for player in player_list:
                if player.pos == pos:
                    n_players_on_spot += 1
                    if n_players_on_spot > 1:  # one player is the player
                        return True
            return False
    return True


def check_victory(player_list):
    for player in player_list:
        if player.pos != player.goal_pos:
            return False
    return True
