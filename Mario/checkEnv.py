from stable_baselines3.common.env_checker import check_env
from MarioEnv import MarioEnv
from Core import Core


env = MarioEnv()
episodes = 50
reward = 0
for episode in range(episodes):
	done = False
	obs = env.reset()
	while not done:
		random_action = env.action_space.sample()
		#print("action",random_action)
		obs, reward, done, info = env.step(random_action)
		env.render()
	print('check reward', reward)
	print(episode)

# It will check your custom environment and output additional warnings if needed
#check_env(env)