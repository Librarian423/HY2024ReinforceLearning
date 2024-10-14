from typing import Optional, Union, List
from gymnasium import Env, spaces
from gymnasium.core import RenderFrame
import numpy as np
import cv2
import random
import time
import pygame as pg

import Const
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


class MarioEnv(gym.Env, object):
    render_on = True
    def __init__(self):
        #print("init")
        super(MarioEnv, self).__init__()

        self.core = Core()
        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        #self.action_space = spaces.Discrete(5)
        # Example for using image as input (channel-first; channel-last also works):
        # self.observation_space = spaces.Box(low=0, high=255,
        #                                     shape=(WINDOW_H, WINDOW_W, 3),
        #                                     dtype=np.uint8)

        self.reward = 0
        self.score = 0
        self.flag_x_position = 6341.25
        self.init_distance = self.flag_x_position - self.core.get_map().get_player().pos_x
        self.previous_distance_to_goal = self.init_distance

    def reset(self):
        self.reward = 0
        self.score = 0
        #init game
        self.core.restart_game()
        self.core.stop()

    def step(self, action):
        #1. user input
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

        # 2. move
        #no delay
        self.handle_action(action)

        #game update
        self.core.update()
        self.input_player()
        if (self.core.get_map().get_player().on_ground and
                self.core.get_map().get_player().already_jumped):
            self.core.keyU = False

        #3. check is game over
        done = False
        self.reward = 0

        #4. player dead
        if self.player_fails():
            done = True
            self.reward -= 50
            self.score = self.get_player_dist_score()
            return self.reward, done, self.score

        #5. time up
        if self.core.get_time() <= 0:
            done = True
            self.reward -= 30
            self.score = self.get_player_dist_score()
            return self.reward, done, self.score

        #6. game clear
        if self.player_clear():
            done = True
            self.reward += 200
            self.score = (100 + self.get_player_dist_score() +
                          self.core.get_score())
            return self.reward, done, self.score

        # # 7. intermediate rewards
        # distance_to_goal = self.get_distance_to_goal()
        # time_remaining = self.core.get_time()
        #
        # previous_distance = self.previous_distance_to_goal
        # self.previous_distance_to_goal = distance_to_goal
        #
        # if distance_to_goal < previous_distance:
        #     self.reward += 0.1  # 목표에 가까워질 때마다 소량의 보상
        #
        # # 시간이 흐를수록 작은 페널티 부여 (빠른 목표 달성을 유도)
        # self.reward -= 0.01 * (100 - time_remaining)
        #
        # print(self.reward)

        #4. return
        return self.reward, done, self.score

    def get_player_dist_score(self):
        distance = self.get_distance_to_goal()
        score = (self.init_distance - distance) / self.init_distance
        return round(score, 2) * 10

    def get_distance_to_goal(self):
        player_x = self.core.get_map().get_player().pos_x
        distance = self.flag_x_position - player_x
        return round(distance, 2)

    def player_fails(self):
        if self.core.get_map().get_event().game_over:
            print("player dead")
            return True
        return False

    def player_clear(self):
        if self.has_reached_flag():
            return True
        return False

    def handle_action(self, action):
        #[right, left, jump, jump_right, jump_left]
        # directions = [Direction.RIGHT, Direction.LEFT,
        #               Direction.JUMP, Direction.JUMP_RIGHT]
        # idx = directions.index(self.direction)
        # k = pg.key.get_pressed()
        # #player moves
        # if np.array_equal(action, [1, 0, 0]): #right
        #     #self.core.move_right()
        #     k[K_d] = True
        #     #new_dir = directions[idx]
        # elif np.array_equal(action, [0, 1, 0]): #left
        #     k[K_a] = True
        #     # next_idx = (idx + 1) % 4
        #     # new_dir = directions[next_idx]
        # else:                       #jump
        #     k[K_w] = True
        #     #self.core.jump()
        #     # next_idx = (idx - 1) % 4
        #     # new_dir = directions[next_idx]
        # k[K_d] = False
        # k[K_a] = False
        # k[K_w] = False

        # self.direction = new_dir

        # if self.direction == Direction.RIGHT:
        #     self.core.move_right()
        # elif self.direction == Direction.LEFT:
        #     self.core.jump_right()
        # elif self.direction == Direction.JUMP:
        #     self.core.jump()
        # elif self.direction == Direction.JUMP_RIGHT:
        #     self.core.jump_right()
        #action = 3
        # 2. action 값에 따라 마리오의 행동을 제어
        if action == 0:  # 아무 동작도 하지 않음
            # 아무런 키 입력도 발생시키지 않음
            #print('right')
            self.press_key(pg.K_RIGHT)  # 오른쪽 방향키 누르기
            self.release_key(pg.K_LEFT)
            self.press_key(pg.K_UP)
        elif action == 1:  # 왼쪽 이동
            #print('left')
            self.press_key(pg.K_LEFT)  # 왼쪽 방향키 누르기
            self.release_key(pg.K_RIGHT)
            self.release_key(pg.K_UP)
        elif action == 2:  # 오른쪽 이동
            #print('right')
            self.press_key(pg.K_RIGHT)  # 오른쪽 방향키 누르기
            self.release_key(pg.K_LEFT)
            self.release_key(pg.K_UP)
        elif action == 3:  # 점프
            self.press_key(pg.K_UP)  # 스페이스바 (점프) 누르기
        elif action == 4:  # 오른쪽 이동 + 점프
            self.press_key(pg.K_RIGHT)  # 오른쪽 방향키 누르기
            self.release_key(pg.K_LEFT)
            self.press_key(pg.K_UP)  # 스페이스바 (점프) 누르기

        # 행동을 멈추기 위해 키를 떼는 부분 (optional)
        if action in [1, 2]:  # 왼쪽이나 오른쪽으로 이동한 경우
            self.release_key(pg.K_LEFT)
            self.release_key(pg.K_RIGHT)
        # elif action in [3, 4]:  # 점프를 한 경우
        #     self.release_key(pg.K_UP)

    def press_key(self, key):
        # 키를 누르는 이벤트 생성
        event = pg.event.Event(pg.KEYDOWN, key=key)
        pg.event.post(event)

    def release_key(self, key):
        # 키를 떼는 이벤트 생성
        event = pg.event.Event(pg.KEYUP, key=key)
        pg.event.post(event)

    def input_player(self):
        for e in pg.event.get():
            #print(e)
            if e.type == pg.KEYDOWN:
                #print('down')
                if e.key == pg.K_RIGHT:
                    self.core.keyR = True
                elif e.key == pg.K_LEFT:
                    self.core.keyL = True
                elif e.key == pg.K_DOWN:
                    self.core.keyD = True
                elif e.key == pg.K_UP:
                    self.core.keyU = True
                elif e.key == pg.K_LSHIFT:
                    self.core.keyShift = True

            elif e.type == pg.KEYUP:
                if e.key == pg.K_RIGHT:
                    self.core.keyR = False
                elif e.key == pg.K_LEFT:
                    self.core.keyL = False
                elif e.key == pg.K_DOWN:
                    self.core.keyD = False
                elif e.key == pg.K_UP:
                    self.core.keyU = False
                elif e.key == pg.K_LSHIFT:
                    self.core.keyShift = False

    def render(self, mode='human'):
        #if self.render_on:
        self.core.render()
        pg.display.flip()

    def has_reached_flag(self):
        # check player has reach flag
        return self.core.reached_flag()

# MarioEnv 등록
register(
    id='Mario-v0',                # 환경 ID
    entry_point='MarioEnv:MarioEnv',  # '파일명:클래스명' 형식
)


