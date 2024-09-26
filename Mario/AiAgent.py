import torch
import random
import numpy as np
from collections import deque
from MarioEnv import MarioEnv
import Const
from Model import Linear_QNet, QTrainer
from Helper import plot


MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001      #learning rate

class Agent:

    def __init__(self):
        self.num_games = 0
        self.epsilon = 0 #randomness
        self.gamma = 0.9 #discount rate #must be smaller than 1
        self.memory = deque(maxlen=MAX_MEMORY) #popleft
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
        #TODO: model, trainer

    def get_state(self, game):
        # players pos
        player_x = game.core.get_map().get_player().pos_x  # 플레이어의 X 좌표
        player_y = game.core.get_map().get_player().pos_y  # 플레이어의 Y 좌표

        # goal x pos
        goal_x = 6341.25

        # distance of goal and player
        distance_to_goal = goal_x - player_x

        # enemies and obstacles pos
        enemies = game.core.get_map().get_mobs_xPos()  # 적들의 좌표 리스트 [(x1, y1), (x2, y2), ...]
        #obstacles = game.core.get_obstacles()  # 장애물 좌표 리스트 [(x1, y1), (x2, y2), ...]

        # distance between enemies
        closest_enemy_distance = float('inf')

        #only if the enemies exists
        if enemies != None:
            for enemy in enemies:
                enemy_x = enemy
                distance = enemy_x - player_x
                if distance > 0:  # 오른쪽에 있는 적만 계산
                    closest_enemy_distance = min(closest_enemy_distance, distance)

        #TODO:

        # distance between obstacles
        # closest_obstacle_distance = float('inf')
        # for obstacle in obstacles:
        #     obstacle_x, obstacle_y = obstacle
        #     distance = obstacle_x - player_x
        #     if distance > 0:  # 오른쪽에 있는 장애물만 계산
        #         closest_obstacle_distance = min(closest_obstacle_distance, distance)

        #TODO
        # hazard zones
        #is_near_cliff = self.core.is_near_cliff(player_x, player_y)  # 플레이어가 낭떠러지 근처에 있는지 확인

        # 상태 벡터로 만들어 반환
        state = np.array([
            player_x,  # 플레이어 X 좌표
            player_y,  # 플레이어 Y 좌표
            distance_to_goal,  # 골대까지의 거리
            closest_enemy_distance,  # 가장 가까운 적과의 거리
            #closest_obstacle_distance,  # 가장 가까운 장애물과의 거리
            #int(is_near_cliff)  # 낭떠러지 근처인지 여부 (1이면 낭떠러지 근처, 0이면 아님)
        ])

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
        #TODO
        self.trainer.train_step( state, action, reward, next_state, done)

    def get_action(self, state):
        #random moves
        self.epsilon = 80 - self.num_games
        #init value
        final_move = 0
        if random.randint(0, 200) < self.epsilon:
            final_move = random.randint(0, 4)
        else:
            #tensor
            first_state = torch.tensor(state, dtype=torch.float)
            prediction = self.model(first_state)
            final_move = torch.argmax(prediction).item()

        return final_move
    # def get_action(self, state):
    #     # random moves: tradeoff exploration / exploitation
    #     self.epsilon = 80 - self.num_games
    #     final_move = [0, 0, 0, 0, 0]  # 5 actions
    #     if random.randint(0, 200) < self.epsilon:
    #         move = random.randint(0, 4)  # Now chooses from 0 to 4
    #         final_move[move] = 1
    #     else:
    #         state0 = torch.tensor(state, dtype=torch.float)
    #         prediction = self.model(state0)
    #         move = torch.argmax(prediction).item()
    #         final_move[move] = 1
    #
    #     return final_move

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
        game.render()
        if done:
            # train long memory, plot result
            game.reset()
            agent.num_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                #agent.model.save()
            print('Game', agent.num_games, 'Score', score, 'Record: ', record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.num_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)


if __name__ == '__main__':
    train()

