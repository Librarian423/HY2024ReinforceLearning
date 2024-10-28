import os
from stable_baselines3 import PPO
import gym
from stable_baselines3.common.env_checker import check_env
from MarioEnv import MarioEnv
from stable_baselines3 import PPO
from Core import Core
import tensorboard

class Manager:

  def __init__(self):
    self.modelDir = "models/PPO_Mario"
    if not os.path.exists(self.modelDir):
      os.makedirs(self.modelDir)
    self.env = gym.make('Mario-v0')
    self.env.reset()

  def closeEnv(self):
    self.env.close()

  def saveModel(self, cnt, timeSteps):
    logDir = "logs"
    if not os.path.exists(logDir):
      os.makedirs(logDir)
  
    # PPO 모델 생성 (MlpPolicy 사용)
    model = PPO('MlpPolicy', self.env, verbose=1, tensorboard_log=logDir)
  
    # 모델 학습 및 저장
    for i in range(cnt):
      model.learn(total_timesteps=timeSteps, reset_num_timesteps=False, tb_log_name="PPO")
      print(i)
      model.save(f"{self.modelDir}/{timeSteps * i}")
      print('save')
  
    self.closeEnv()

  def contSaveModel(self, start, end, timeSteps):
    logDir = "logs"
    if not os.path.exists(logDir):
      os.makedirs(logDir)

    modelPath = f"{self.modelDir}/{(start - 1) * timeSteps}.zip"
    model = PPO.load(modelPath, env=self.env)

    for i in range(start, end):
      model.learn(total_timesteps=timeSteps, reset_num_timesteps=False, tb_log_name="PPO")
      print(i)
      model.save(f"{self.modelDir}/{timeSteps * i}")
      print('save')

    self.closeEnv()

  
  def loadModel(self, num, episodes):
    modelPath = f"{self.modelDir}/{num}.zip"
    model = PPO.load(modelPath, env=self.env)

    for ep in range(episodes):
      obs = self.env.reset()
      done = False
      while not done:
        action, _ = model.predict(obs)
        print(action)
        obs, rewards, done, info = self.env.step(action)
        self.env.render()

    self.closeEnv()
  
  
manager = Manager()
# manager.saveModel(10, 100000)
# manager.contSaveModel(100, 120, 100000)
manager.loadModel(11000000, 10)
