import gym
from stable_baselines3 import PPO
from MarioEnv import MarioEnv

env = MarioEnv()
env.reset()

models_dir = "models/PPO_Mario"
model_path = f"{models_dir}/210.zip"

model = PPO.load(model_path, env=env)

episodes = 10

for ep in range(episodes):
    obs = env.reset()
    done = False
    while not done:
        action, _ = model.predict(obs)
        obs, rewards, done, info = env.step(action)
        env.render()

env.close()