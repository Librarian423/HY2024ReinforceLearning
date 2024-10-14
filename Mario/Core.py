from os import environ

import pygame as pg
from pygame.locals import *
from enum import Enum
from Const import *
from Map import Map
from MenuManager import MenuManager

class Core(object):
    """

    Main class.

    """

    def __init__(self):
        environ['SDL_VIDEO_CENTERED'] = '1'

        pg.init()
        pg.display.set_caption('Reinforcement Learning')
        pg.display.set_mode((WINDOW_W, WINDOW_H))

        self.screen = pg.display.set_mode((WINDOW_W, WINDOW_H))
        self.clock = pg.time.Clock()

        self.oWorld = Map('1-1')
        self.oMM = MenuManager(self)

        self.run = True
        self.keyR = False
        self.keyL = False
        self.keyU = False
        self.keyD = False
        self.keyShift = False

        self.is_flag = False

    def main_loop(self):
        while self.run:
            self.input()
            self.update()
            self.render()
            self.clock.tick(FPS)

    def input(self):
        # if press 0 reset
        # k = pg.key.get_pressed()

        if self.get_mm().currentGameState == 'Game':
            # test reset input key_0
            # if k[K_0]:
            #     self.__init__()
            # if k[K_d]:
            #     print('r')
            #     self.move_right()
            # elif k[K_a]:
            #     self.move_left()
            # elif k[K_w]:
            #     self.jump()
            #reset up key when player on groun
            if (self.get_map().get_player().on_ground and
                    self.get_map().get_player().already_jumped):
                self.keyU = False

            self.input_player()

    def input_player(self):
        for e in pg.event.get():
            print(e)
            if e.type == pg.KEYDOWN:
                print('down')
                if e.key == pg.K_RIGHT:
                    self.keyR = True
                elif e.key == pg.K_LEFT:
                    self.keyL = True
                elif e.key == pg.K_DOWN:
                    self.keyD = True
                elif e.key == pg.K_UP:
                    self.keyU = True
                elif e.key == pg.K_LSHIFT:
                    self.keyShift = True

            elif e.type == pg.KEYUP:
                if e.key == pg.K_RIGHT:
                    self.keyR = False
                elif e.key == pg.K_LEFT:
                    self.keyL = False
                elif e.key == pg.K_DOWN:
                    self.keyD = False
                elif e.key == pg.K_UP:
                    self.keyU = False
                elif e.key == pg.K_LSHIFT:
                    self.keyShift = False

    def update(self):
        self.get_mm().update(self)

    def render(self):
        self.get_mm().render(self)

    def get_map(self):
        return self.oWorld

    def get_mm(self):
        return self.oMM

    def get_is_player_dead(self):
        return self.oWorld.get_is_player_dead()

    def get_score(self):
        if not self.oWorld.get_player().isdead and self.get_map().time > 0:
            return self.oWorld.get_player().get_score() + self.get_map().time
        return self.oWorld.get_player().get_score()

    def restart_game(self):
        self.__init__()

    def stop(self):
        self.keyR = False
        self.keyL = False
        self.keyU = False
        self.keyD = False
        self.keyShift = False

    def move_left(self):
        # run left
        self.keyShift = True
        self.keyL = True
        self.keyR = False
        self.keyU = False
        self.keyD = False


    def move_right(self):
        # run right
        self.keyShift = True
        self.keyL = False
        self.keyR = True
        self.keyD = False

    def move_down(self):
        # down
        self.keyD = True

    def jump(self):
        # jump
        self.keyShift = True
        self.keyL = False
        self.keyR = False
        self.keyD = False
        self.keyU = True


    def jump_left(self):
        # jump left
        self.keyShift = True
        self.keyL = True
        self.keyR = False
        self.keyD = False
        self.keyU = True


    def jump_right(self):
        # jump right
        # self.keyShift = True
        self.keyL = False
        self.keyR = True
        self.keyD = False
        self.keyU = True

    def reached_flag(self):
        return self.is_flag

    def set_flag_true(self):
        self.is_flag = True

    def get_time(self):
        return (self.oWorld.get_time())
