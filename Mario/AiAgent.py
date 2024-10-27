import torch
import random
import pygame as pg
from pygame.locals import *
import numpy as np
from collections import deque
from MarioEnv import MarioEnv
import Const
from Model import Linear_QNet, QTrainer
from Helper import plot


MAX_MEMORY = 100_000
BATCH_SIZE = 500
LR = 0.001      #learning rate

class Agent:

    def __init__(self):
        self.num_games = 0
        self.epsilon = 0 #randomness
        self.gamma = 0.9 #discount rate #must be smaller than 1
        self.memory = deque(maxlen=MAX_MEMORY) #popleft
        self.model = Linear_QNet(9, 256, 4)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        # players pos
        player_x = game.core.get_map().get_player().pos_x  # 플레이어의 X 좌표
        player_y = game.core.get_map().get_player().rect.y  # 플레이어의 Y 좌표

        # goal x pos
        goal_x = 6341.25

        # distance of goal and player
        distance_to_goal = goal_x - player_x

        #hazard y cord
        hazard_y = 448


        #enemies pos
        enemies = game.core.get_map().get_mobs_xPos()

        # distance between enemies
        #only if the enemies exists
        if enemies != None:
            closest_x = enemies[0]
            for enemy in enemies:
                distance = enemy
                if distance < closest_x:
                    closest_x = distance
        else:
            closest_x = -1

        #blocks pos
        ob_blocks = game.core.get_map().get_near_blocks()
        cha_right = ob_blocks[0]
        cha_left = ob_blocks[1]
        cha_upper = ob_blocks[2]
        cha_upper_r = ob_blocks[3]
        # down = ob_blocks[3]

        # state vector
        state = np.array([
            player_x,  # player x pos
            player_y,  # player y pos
            distance_to_goal,  # left distance x to goal
            hazard_y,           #out from map y cord
            player_x < closest_x,  # 가장 가까운 적과의 거리
            #player surronding blocks
            cha_right,
            cha_left,
            cha_upper,
            cha_upper_r,
        ])
        # print('x: ',state[0],' y: ',state[1],' enemy: ',state[4],
        #        'r: ', state[5],' l: ',state[6],
        #       ' u: ', state[7], ' ur: ', state[8])
        return state

    def remember(self, state, action, reward, next_state, done):
        # popleft if MAX_MEMORY
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            #list of tuples
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)


    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves
        self.epsilon = max(0.01, 80 - self.num_games)
        final_move = [0, 1, 2, 3]#, 4]
        action_num = 0

        # init value
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 3)
            action_num = final_move[move]
        else:
            # tensor
            first_state = torch.tensor(state, dtype=torch.float)
            prediction = self.model(first_state)
            move = torch.argmax(prediction).item()
            action_num = final_move[move]

        #print(action_num)
        return action_num

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = MarioEnv()


    while True:
        #get old state
        state_old = agent.get_state(game)

        #get move
        final_move = agent.get_action(state_old)

        #perform move and get new state
        reward, done, score = game.step(final_move)
        state_new = agent.get_state(game)

        #train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, score)

        #remember
        agent.remember(state_old, final_move, reward, state_new, done)

        #render
        game.render()

        if done:
            # train long memory, plot result
            game.reset()
            agent.num_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()
            print('Game', agent.num_games, 'Score', score, 'Record: ', record, 'Reward: ', reward)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.num_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)


if __name__ == '__main__':
    train()

