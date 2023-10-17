import gym
from gym import spaces
import pygame
import numpy as np

class StairTrain(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"],"render_fps": 4}

    def __init__(self, render_mode=None, size=5, n_agents=1): # please only use size 5 for now
        self.size = size # Not yet implemented
        self.n_agents = n_agents # not yet implemented
        self.observation_space = ...
        self.action_space = spaces.Discrete(5)


        self._action_to_direction = {
            0: np.array([1, 0]),
            1: np.array([0, 1]),
            2: np.array([-1, 0]),
            3: np.array([0, -1]),
            4: np.array([0,0]) # allow for someone to not move at all
        }

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        self.window=None
        self.clock=None

    def _get_obs(self):
        pass #return agent locations, agent goals, obstacle location, etc.

    def _get_info(self):
        pass # aux info

    def reset(self, seed=None, options=None):
        super.reset(seed=seed)

        self._agent_location = self.np_random.integers(0, self.size, size=2, dtype=int) # create starting locations for everyone, overlap is okay
        self._obstacle_location = self._agent_location
        while np.array_equal(self._obstacle_location, self._agent_location):
            self._target_location = self.np_random.integers( 0, self.size, size=2, dtype=int)

        self._goal_location = self._agent_location
        while np.array_equal(self._goal_location, self._agent_location):
            self._goal_location = self.np_random.integers( 0, self.size, size=2, dtype=int)

        #only one agent: use a step next to obstacle

        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, info
        





    def step():
        # make the things move, making sure they don't go out of bounds or go into an obstacle illegally
