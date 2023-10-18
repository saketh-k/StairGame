from gymnasium.envs.registration import register

register(
    id="StairWorld-v0",
    entry_point="stair_world.envs:StairTrain",
    max_episode_steps=300
)