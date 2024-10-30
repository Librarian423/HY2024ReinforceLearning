import pygame as pg

from Const import *

#UPDATE CHECK KILL 
class Event(object):
    def __init__(self):
        self.x_vel = 0
        self.y_vel = 0
        self.win = False
        self.game_over = False
        self.player_in_castle = False


    def reset(self):
        self.x_vel = 0
        self.y_vel = 0
        self.win = False
        self.game_over = False
        self.player_in_castle = False


    def start_kill(self, core, game_over):
        core.get_map().set_event()

        # core.get_map().get_player().add_score(-5000)
        core.get_map().get_player().set_image(-1)
        self.y_vel = -4.0

        self.game_over = True #game_over
        self.win = False



    def start_win(self, core):
        core.set_flag_true()
        core.get_map().set_event()

        # core.get_map().get_player().add_score(5000)
        core.get_map().get_player().set_image(5)
        core.get_map().get_player().x_vel = 1
        core.get_map().get_player().rect.x += 10

        self.win = True
        self.game_over = False

        # Adding score depends on the map's time left.
        if core.get_map().time >= 300:
            core.get_map().get_player().add_score(5000)
        #     core.get_map().spawn_score_text(core.get_map().get_player().rect.x + 16, core.get_map().get_player().rect.y, score=5000)
        elif 200 <= core.get_map().time < 300:
            core.get_map().get_player().add_score(2000)
        #     core.get_map().spawn_score_text(core.get_map().get_player().rect.x + 16, core.get_map().get_player().rect.y, score=2000)
        else:
            core.get_map().get_player().add_score(1000)
        #     core.get_map().spawn_score_text(core.get_map().get_player().rect.x + 16, core.get_map().get_player().rect.y, score=1000)


    def update(self, core):
        player = core.get_map().get_player()
        if self.game_over:
            self.y_vel += GRAVITY * FALL_MULTIPLIER if self.y_vel < 6 else 0
            core.get_map().get_player().rect.y += self.y_vel
        elif self.win:
            if self.player_in_castle:
                pass
            else:
                pass