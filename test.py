import stair_world.stair_world
import gymnasium
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3 import DQN

env = gymnasium.make("StairWorld-v0")

model = DQN('MultiInputPolicy', env).learn(total_timesteps=1e6)
mean_reward, std_reward = evaluate_policy(model, model.get_env(), n_eval_episodes=10)
print(f'The mean reward was {mean_reward} and the standard deviation was {std_reward}.')
#check_env(env, skip_render_check=False)

obs = env.reset()
for i in range(1000):
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    env.render()