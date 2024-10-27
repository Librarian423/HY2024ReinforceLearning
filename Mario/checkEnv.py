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
		reward, done, score = env.step(random_action)
		env.render()

	print(episode, 'attempt')
	print('reward: ', reward)
	print('score: ', score)


# It will check your custom environment and output additional warnings if needed
#check_env(env)