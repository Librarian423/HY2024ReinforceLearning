from stable_baselines3.common.env_checker import check_env
from MarioEnv import MarioEnv
from Core import Core


env = MarioEnv()
episodes = 50

for episode in range(episodes):
	done = False
	obs = env.reset()
	while not done:
		random_action = env.action_space.sample()
		print("action",random_action)
		obs, reward, done, info = env.step(random_action)
		print('reward',reward)
		env.render()

# It will check your custom environment and output additional warnings if needed
#check_env(env)