from os import environ

import pygame as pg
from pygame.locals import *

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
        pg.display.set_caption('Mario by S&D')
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

    def main_loop(self):

        while self.run:
            self.input()

            self.update()
            self.render()
            self.clock.tick(FPS)

    def input(self):
        #if press 0 reset
        k = pg.key.get_pressed()
        if self.get_mm().currentGameState == 'Game':
            #reset
            if k[K_0]:
                print("reset")
                self.__init__()

            self.input_player()

       

    def input_player(self):
        for e in pg.event.get():

            if e.type == pg.QUIT:
                self.run = False

            elif e.type == KEYDOWN:
                if e.key == K_RIGHT:
                    self.keyR = True
                elif e.key == K_LEFT:
                    self.keyL = True
                elif e.key == K_DOWN:
                    self.keyD = True
                elif e.key == K_UP:
                    self.keyU = True
                elif e.key == K_LSHIFT:
                    self.keyShift = True

            elif e.type == KEYUP:
                if e.key == K_RIGHT:
                    self.keyR = False
                elif e.key == K_LEFT:
                    self.keyL = False
                elif e.key == K_DOWN:
                    self.keyD = False
                elif e.key == K_UP:
                    self.keyU = False
                elif e.key == K_LSHIFT:
                    self.keyShift = False


    def update(self):
        self.get_mm().update(self)

    def render(self):
        self.get_mm().render(self)

    def get_map(self):
        return self.oWorld

    def get_mm(self):
        return self.oMM

    def restart_game(self):
        self.__init__()

    def move_left(self):
        #left
        self.keyL = True
        self.keyD = False
    def move_right(self):
        #left
        self.keyR = True

    def move_down(self):
        #down
        self.keyD = True
    def jump(self):
        #jump
        self.keyU = True

    def get_time(self):
        return (self.oWorld.get_time())
  
















































































#removed:



# from Sound import Sound

#init:

# pg.mixer.pre_init(44100, -16, 2, 1024)
# self.oSound = Sound()


#input:
 #else:
            #self.input_menu()



#input menu:

    # def input_menu(self):
    #     for e in pg.event.get():
    #         if e.type == pg.QUIT:
    #             self.run = False

    #         elif e.type == KEYDOWN:
    #             if e.key == K_RETURN:
    #                 self.get_mm().start_loading()



#get_sound()

#  # def get_sound(self):
    #     return self.oSound
