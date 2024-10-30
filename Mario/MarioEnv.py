import pygame as pg
import gym
from gym.envs.registration import register
from Core import Core

class MarioEnv(gym.Env, object):
    render_on = True
    def __init__(self):
        super(MarioEnv, self).__init__()

        self.core = Core()

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
        self.core.reset_key()

    def step(self, action):
        #1. user input
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

        # 2. move
        self.handle_action(action)

        #game update
        self.core.update()
        #agent input
        self.input_player()
        if (self.core.get_map().get_player().on_ground and
                self.core.get_map().get_player().already_jumped):
            self.core.keyU = False

        #3. check is game over
        done = False
        self.reward = 0
        self.score = self.core.get_score()

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
            self.reward += 200 + self.core.get_time()
            self.score = (100 + self.core.get_score() + self.core.get_time())
            return self.reward, done, self.score

        #7. return
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
            #print("player dead")
            return True
        return False

    def player_clear(self):
        if self.has_reached_flag():
            return True
        return False

    def handle_action(self, action):
        if action == 0:  # right jump
            self.press_key(pg.K_RIGHT)
            self.release_key(pg.K_LEFT)
            self.press_key(pg.K_UP)
        elif action == 1:  # left
            self.press_key(pg.K_LEFT)
            self.release_key(pg.K_RIGHT)
            self.release_key(pg.K_UP)
        elif action == 2:  # right
            self.press_key(pg.K_RIGHT)
            self.release_key(pg.K_LEFT)
            self.release_key(pg.K_UP)
        elif action == 3:  # jumo
            self.press_key(pg.K_UP)

        # stop
        if action in [1, 2]:  # on left or right
            self.release_key(pg.K_LEFT)
            self.release_key(pg.K_RIGHT)


    def press_key(self, key):
        #event on press key
        event = pg.event.Event(pg.KEYDOWN, key=key)
        pg.event.post(event)

    def release_key(self, key):
        #event on release key
        event = pg.event.Event(pg.KEYUP, key=key)
        pg.event.post(event)

    def input_player(self):
        #core input
        for e in pg.event.get():
            if e.type == pg.KEYDOWN:
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


    def render(self, mode='human'): # mode='human' 시 렌더링
        # if self.render_on:
        self.core.render()
        pg.display.flip()

    def has_reached_flag(self):
        # check player has reach flag
        return self.core.reached_flag()

# MarioEnv 등록
register(
    id='Mario-v0',                # Env ID
    entry_point='MarioEnv:MarioEnv', 
)