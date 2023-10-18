import time
import stair_world
import gymnasium
import numpy as np
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3 import DQN, A2C
from gymnasium.wrappers import NormalizeReward
import imageio

env = gymnasium.make("StairWorld-v0", render_mode="rgb_array")
env = NormalizeReward(env)
# print(env.reset(seed=22))
# model = A2C('MultiInputPolicy', env, verbose=1).learn(total_timesteps=1e5)
# mean_reward, std_reward = evaluate_policy(model, model.get_env(), n_eval_episodes=10)
# print(f'The mean reward was {mean_reward} and the standard deviation was {std_reward}.')
#check_env(env, skip_render_check=False)

# model.save("a2c_stair")
# del model

model = A2C.load("a2c_stair")

images = []
obs, _info = env.reset()
img = env.render()
images.append(img)
print(obs)
for i in range(1000):
    action, _states = model.predict(obs)
    obs, reward, terminated, info, done = env.step(action)
    print(obs, action)
    img = env.render()
    images.append(img)
    # env.render()
    time.sleep(1)

    if terminated:
        break
imageio.mimsave("stair_game.gif", [np.array(img) for i, img in enumerate(images)], fps=2)