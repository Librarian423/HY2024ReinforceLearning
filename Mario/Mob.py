import pygame as pg
import random

from Const import *


class Mob(object):

    def __init__(self, x_pos, y_pos, name, index):

        self.pos_x = x_pos
        self.x_vel = random.choice([-1, 1]) * MOB_SLOW_SPEED
        self.y_vel = 0
        self.name = name
        self.index = index
        self.on_ground = False

        self.image = pg.image.load('Assets/images/' + self.name + '_0.png')
        self.sprites = []
        self.spriteTick = 0
        self.load_sprites()

        self.rect = pg.Rect(x_pos, y_pos, 32, 32)

    def load_sprites(self):
        self.sprites = [
            # 0
            pg.image.load('Assets/images/' + self.name + '_0.png'),

            # 1
            pg.image.load('Assets/images/' + self.name + '_1.png')]

    def update(self, core):
        self.mob_physics(core)
        self.update_image(core)

    def mob_physics(self, core):
        blocks = core.get_map().get_blocks_for_collision(self.rect.x // 32, self.rect.y // 32)
        self.pos_x += self.x_vel
        self.rect.x = self.pos_x

        # this function allows to stop when player collides with bricks
        self.update_x_pos(blocks, core)

    def update_x_pos(self, blocks, core):

        if self.rect.left < 0:
            self.rect.left = 0
            self.pos_x = self.rect.left
            self.x_vel = MOB_SLOW_SPEED
        elif self.rect.right > WINDOW_H:
            pass

        for mob in core.get_map().mobs:
            if self.index == mob.index:
                continue
            if pg.Rect.colliderect(self.rect, mob.rect):
                if self.x_vel > 0:
                    self.rect.right = mob.rect.left
                    self.pos_x = self.rect.left
                    self.x_vel = -MOB_SLOW_SPEED
                elif self.x_vel < 0:
                    self.rect.left = mob.rect.right
                    self.pos_x = self.rect.left
                    self.x_vel = MOB_SLOW_SPEED

        for block in blocks:
            if block != 0 and block.type != 'BGObject':
                block.debugLight = True
                if pg.Rect.colliderect(self.rect, block.rect):
                    if self.x_vel > 0:
                        self.rect.right = block.rect.left
                        self.pos_x = self.rect.left
                        self.x_vel = -MOB_SLOW_SPEED
                    elif self.x_vel < 0:
                        self.rect.left = block.rect.right
                        self.pos_x = self.rect.left
                        self.x_vel = MOB_SLOW_SPEED

    def update_y_pos(self, blocks, core):
        pass

    def update_image(self, core):

        self.spriteTick += 1
        if self.spriteTick > 20:
            self.spriteTick = 0

        if self.spriteTick <= 10:
            self.image = self.sprites[0]
        elif 11 <= self.spriteTick <= 20:
            self.image = self.sprites[1]
        elif self.spriteTick == 21:
            self.spriteTick = 0
            self.image = self.sprites[0]

    def render(self, core):
        core.screen.blit(self.image, core.get_map().get_Camera().apply(self))

