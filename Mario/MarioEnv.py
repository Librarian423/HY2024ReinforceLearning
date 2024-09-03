from typing import Optional, Union, List

import numpy as np
import cv2
import random
import time
import pygame as pg

from gym.core import RenderFrame

from Player import Player
import gym
from gym import spaces
from collections import deque
from pygame.locals import *
from Core import Core


Mario_LEN_GOAL = 30

done = False

class MarioEnv(gym.Env, object):
    reward = 0
    def __init__(self):
        #print("init")
        super(MarioEnv, self).__init__()

        self.core = Core()
        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        self.action_space = spaces.Discrete(4)
        # Example for using image as input (channel-first; channel-last also works):
        self.observation_space = spaces.Box(low=-500, high=500,
                                            shape=(5 + Mario_LEN_GOAL,), dtype=np.uint8)

    def step(self, action):
        self.handle_action(action)

        # 게임 상태 업데이트
        self.core.update()

        # 상태 관찰
        state = self.get_state()

        # 보상 계산 (단순한 예시)
        reward = self.calculate_reward()

        # 게임 종료 여부
        done = self.is_done()
        if self.core.get_time() <= 0:
            done = True

        # 추가 정보
        info = {}

        return state, reward, done, info

    def calculate_reward(self):
        reward = 0
        if self.core.get_mm().currentGameState == 'Game':
            reward += 1  # 생존 보상
        return reward

    def is_done(self):
        return self.core.get_mm().currentGameState != 'Game'


    def handle_action(self, action):
        # 액션에 따라 키 입력을 설정
        if action == 0:  # 정지
            self.core.keyR = False
            self.core.keyL = False
            self.core.keyU = False
        elif action == 1:  # 왼쪽 이동
            self.core.move_left()
        elif action == 2:  # 오른쪽 이동
            self.core.move_right()
        elif action == 3:  # 점프
            self.core.jump()

    def reset(self):
        print("reset")
        self.core.restart_game()
        return self.get_state()

    def get_state(self):
        state = pg.surfarray.array3d(self.core.screen)
        return np.transpose(state, (1, 0, 2))  # 상태 형식을 (높이, 너비, 채널)로 변환

    def render(self, mode='human'):
        # Pygame 화면을 렌더링
        self.core.render()