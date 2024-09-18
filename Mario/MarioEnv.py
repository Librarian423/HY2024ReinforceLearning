from typing import Optional, Union, List
from gymnasium import Env, spaces
from gymnasium.core import RenderFrame
import numpy as np
import cv2
import random
import time
import pygame as pg
from Const import *
from gym.core import RenderFrame

from Player import Player
import gym
from gym import spaces
from gym.envs.registration import register
from collections import deque
from pygame.locals import *
from Core import Core


Mario_LEN_GOAL = 30

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
        self.observation_space = spaces.Box(low=0, high=255,
                                            shape=(WINDOW_H, WINDOW_W, 3),
                                            dtype=np.uint8)
        self.currentTime = 0
        self.input_cooldown = 200
        self.score = 0
        self.reward = 0

    def step(self, action):
        if self.currentTime <= 0:
            self.handle_action(action)
            self.currentTime = self.input_cooldown

        # 게임 상태 업데이트
        self.core.update()

        # 상태 관찰
        state = self.get_state()

        # 보상 계산 (단순한 예시)
        #reward = self.calculate_reward()

        # 게임 종료 여부
        done = self.is_done()

        if done:
            self.reward = self.get_reward()

        # 게임이 종료되었지만 더는 상태가 없음
        #truncated = False

        if self.core.get_time() <= 0:
            done = True
            self.reward -= 10
            #truncated = True
            print("time up")

        # 추가 정보
        info = {}
        self.currentTime = self.currentTime - 1

        return state, self.reward, done, info

    def calculate_reward(self):
        reward = 0
        if self.core.get_mm().currentGameState == 'Game':
            reward += 1  # 생존 보상
        return reward

    def set_reward(self, score):
        self.score = score

    def get_reward(self):
        return self.score

    def is_done(self):
        if self.core.get_map().get_event().game_over:
            print("player dead")
            self.set_reward(-10)
            return True
        if self.has_reached_flag():
            self.set_reward(50)
            return True
        return self.core.get_mm().currentGameState != 'Game'


    def handle_action(self, action):
        #print("action", action)
        # 액션에 따라 키 입력을 설정
        if action == 0:  # 정지
            pass
            # self.core.keyR = False
            # self.core.keyL = False
            # self.core.keyU = False
        elif action == 1:  # 왼쪽 이동
            self.core.move_left()
        elif action == 2:  # 오른쪽 이동
            self.core.move_right()
        elif action == 3:  # 점프
            self.core.jump()

    def reset(self):
        print("reset")
        self.last_input_time = 0
        self.input_cooldown = 200
        self.core.restart_game()
        return self.get_state()

    def get_state(self):
        state = pg.surfarray.array3d(self.core.screen)
        return np.transpose(state, (1, 0, 2))  # 상태 형식을 (높이, 너비, 채널)로 변환

    def render(self, mode='human'):
        # Pygame 화면을 렌더링
        self.core.render()
        pg.display.flip()  # 화면 업데이트

    def has_reached_flag(self):
        # 깃대에 도달했는지 확인하는 로직을 구현
        return self.core.reached_flag()

# MarioEnv 등록
register(
    id='Mario-v0',                # 환경 ID
    entry_point='MarioEnv:MarioEnv',  # '파일명:클래스명' 형식
)


