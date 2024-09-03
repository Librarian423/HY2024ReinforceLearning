import numpy as np
import cv2
import random
import time
from Core import Core
import Player
import gym
from gym import spaces
from collections import deque

Mario_LEN_GOAL = 30

game = Core()

class MarioEnv(gym.Env, object):
    def __init__(self):
        #print("init")
        super(MarioEnv, self).__init__()
        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        self.action_space = spaces.Discrete(4)
        # Example for using image as input (channel-first; channel-last also works):
        self.observation_space = spaces.Box(low=-500, high=500,
                                            shape=(5 + Mario_LEN_GOAL,), dtype=np.uint8)

    def step(self, action):
        print("step")
        self.prev_actions = []
        self.prev_actions.append(action)

        # Change the head position based on the button direction
        #left
        if action == 0:
            game.move_left()
        #right
        elif action == 1:
            game.move_right()
        #up
        elif action == 2:
            game.jump()

        info = {}
        self.observation = []
        self.reward = 0
        if game
        self.done = False

        return self.observation, self.reward, self.done, info

    def reset(self):
        print("reset")
        game.restart_game()
        self.done = False

