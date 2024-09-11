import os
from stable_baselines3 import PPO
import gym
from stable_baselines3.common.env_checker import check_env
from MarioEnv import MarioEnv
from stable_baselines3 import PPO
from Core import Core
import tensorboard

# 모델 및 로그 디렉토리 설정
models_dir = "models/PPO_Mario"
logdir = "logs"

if not os.path.exists(models_dir):
    os.makedirs(models_dir)

if not os.path.exists(logdir):
    os.makedirs(logdir)

# Gym 환경 생성
env = gym.make('Mario-v0')  # 등록된 환경 사용
env.reset()

# PPO 모델 생성 (MlpPolicy 사용)
model = PPO('MlpPolicy', env, verbose=1, tensorboard_log=logdir)

# 모델 학습 및 저장
TIMESTEPS = 10000
for i in range(1, 30):
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name="PPO")
    print(i)
    model.save(f"{models_dir}/{TIMESTEPS * i}")
    print('save')

env.close()
