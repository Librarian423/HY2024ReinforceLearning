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
from enum import Enum

from Player import Player
import gym
from gym import spaces
from gym.envs.registration import register
from collections import deque
from pygame.locals import *
from Core import Core


#Mario_LEN_GOAL = 30

class MOVES(Enum):
    RIGHT = 0
    LEFT = 1
    JUMP = 2
    JUMP_LEFT = 3
    JUMP_RIGHT = 4

class MarioEnv(gym.Env, object):
    reward = 0
    def __init__(self):
        #print("init")
        super(MarioEnv, self).__init__()

        self.core = Core()
        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        self.action_space = spaces.Discrete(5)
        # Example for using image as input (channel-first; channel-last also works):
        self.observation_space = spaces.Box(low=0, high=255,
                                            shape=(WINDOW_H, WINDOW_W, 3),
                                            dtype=np.uint8)
        self.currentTime = 0
        self.input_cooldown = 200
        self.score = 0
        self.direction = MOVES.RIGHT

    def reset(self):
        print("reset")
        self.direction = MOVES.RIGHT
        self.last_input_time = 0
        self.currentTime = 0
        self.input_cooldown = 200
        self.reward = 0
        self.score = 0
        self.core.restart_game()

    def step(self, action):
        #1. user input
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

        # 2. move
        #input delay
        if self.currentTime <= 0:
            self.handle_action(action)
            self.currentTime = self.input_cooldown
        #input delay cooldown
        self.currentTime = self.currentTime - 1

        #game update
        self.core.update()


        #3. check is game over
        done = False

        reward = 0

        #player dead or time up
        if self.player_fails() or self.core.get_time() <= 0:
            reward -= 10
            done = True
            self.score = self.core.get_score()
            return reward, done, self.score
        #game clear
        if self.player_clear():
            done = True
            reward += 10
            self.score = self.core.get_score()
            return reward, done, self.score

        #4. return
        return reward, done, self.score

    # def calculate_reward(self):
    #     reward = 0
    #     if self.core.get_mm().currentGameState == 'Game':
    #         reward += 1  # 생존 보상
    #     return reward

    # def set_reward(self, score):
    #     self.score = score

    def player_fails(self):
        if self.core.get_map().get_event().game_over:
            print("player dead")
            #self.set_reward(-100)
            return True
        return False

    def player_clear(self):
        if self.has_reached_flag():
            return True
        return False

    def handle_action(self, action):
        if action == 0:
            self.core.move_right()
        elif action == 1:
            self.core.move_left()
        elif action == 2:  # 점프
            self.core.jump()
        elif action == 3:
            self.core.jump_left()
        elif action == 4:
            self.core.jump_right()


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


