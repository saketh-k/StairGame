import gymnasium as gym
from gymnasium import spaces
import pygame
import numpy as np

class StairTrain(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"],"render_fps": 4}

    def __init__(self, render_mode=None, size=5, n_agents=1): # please only use size 5 for now
        self.size = size # Not yet implemented
        self.window_size = 512
        self.n_agents = n_agents # not yet implemented

        self.observation_space = spaces.Dict(
                {
                    "agent": spaces.Box(0, size - 1, shape=(2,), dtype=int),
                    "helper": spaces.Box(0, size - 1, shape=(2,), dtype=int),
                    "obstacle": spaces.Box(0, size - 1, shape=(2,), dtype=int),
                    "goal": spaces.Box(0, size - 1, shape=(2,), dtype=int)
                }
            )
        self.action_space = spaces.Discrete(5)


        self._action_to_direction = {
            0: np.array([1, 0]),
            1: np.array([0, 1]),
            2: np.array([-1, 0]),
            3: np.array([0, -1]),
            4: np.array([0, 0]), # allow for someone to not move at all
        }

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        self.window=None
        self.clock=None

    def _get_obs(self):
        return {
            "agent": self._agent_location,
            "helper": self._helper_location,
            "obstacle": self._obstacle_location,
            "goal": self._goal_location
        }
        pass #return agent locations, agent goals, obstacle location, etc.

    def _get_info(self):
        return dict()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self._agent_location = self.np_random.integers(0, self.size, size=2, dtype=int) # create starting locations for everyone, overlap is okay
        self._obstacle_location = self._agent_location
        while np.array_equal(self._obstacle_location, self._agent_location):
            self._obstacle_location = self.np_random.integers( 0, self.size, size=2, dtype=int)

        self._goal_location = self._obstacle_location
        # self._goal_location = self._agent_location
        # while np.array_equal(self._goal_location, self._agent_location):
        #     self._goal_location = self.np_random.integers( 0, self.size, size=2, dtype=int)

        #set the helper ramp location for the single agent case
        random_dir = self._action_to_direction[self.np_random.integers(0,4)] # generate a random int between 0 and 3 (helper must be on different square)
        self._helper_location = self._obstacle_location + random_dir
        while (self._helper_location + random_dir < 0).any() or (self._helper_location + random_dir > self.size-1).any():
            #unsure if boolean is correct
            random_dir = self._action_to_direction[self.np_random.integers(0,4)] # generate a random int between 0 and 3 (helper must be on different square)
            self._helper_location = self._obstacle_location + random_dir
            


        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, info
        





    def step(self, action):
        # make the things move, making sure they don't go out of bounds or go into an obstacle illegally
        direction = self._action_to_direction[int(action)]

        #handle bounds and obstacles

        # self._agent_location = np.clip(
        #     self._agent_location + direction, 0, self.size - 1
        # )


        if not np.array_equal(self._agent_location + direction, self._obstacle_location):
            self._agent_location = np.clip(
                self._agent_location + direction, 0, self.size - 1
            )

        elif np.array_equal(self._agent_location, self._helper_location):
#        if self._agent_location == self._helper_location: 
            #it can go wherever it wants if it's on a step
            self._agent_location = np.clip(
                self._agent_location + direction, 0, self.size - 1
            )

        terminated = np.array_equal(self._agent_location, self._goal_location)
        reward = 100 if terminated else 0 #binary sparse rewards
        
        reward += -np.linalg.norm(self._agent_location-self._goal_location)
        if int(action) == 4:
            reward -= 5
        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, reward, terminated, False, info

    def render(self):
        if self.render_mode == "rgb_array":
            return self._render_frame()

    def _render_frame(self):            
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode((self.window_size, self.window_size))

        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()

        canvas = pygame.Surface((self.window_size, self.window_size))
        canvas.fill((255,255,255)) # make black background

        #must draw objects in descending order

        #helper function for draw robot 2
        self._draw_robot(1, canvas, (127,0,0), self._helper_location)
        #helper function for draw robot 1
        self._draw_robot(0, canvas, (255,0,0), self._agent_location)
        #helper function for draw obstacle
        self._draw_robot(-1, canvas, (0,0,0), self._obstacle_location)
        #helper function for draw goal point (as start)
        self._draw_robot(-2, canvas, (0,255,0), self._goal_location)


        if self.render_mode == "human":
            # The following line copies our drawings from `canvas` to the visible window
            self.window.blit(canvas, canvas.get_rect())
            pygame.event.pump()
            pygame.display.update()

            # We need to ensure that human-rendering occurs at the predefined framerate.
            # The following line will automatically add a delay to keep the framerate stable.
            self.clock.tick(self.metadata["render_fps"])
        else:  # rgb_array
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2)
            )

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()

    def _draw_robot(self, idx, canvas, col, location):
        block_size = self.window_size / self.size
        n_obj = self.n_agents + 3 + 1 # n agents, obstacle, start and goal  locations
        obj_num = idx + 3 #leave first three open
        pygame.draw.rect(
            canvas,
            col,
            pygame.Rect(
                block_size * location,
                (block_size, obj_num * block_size//n_obj)
            )
        )
