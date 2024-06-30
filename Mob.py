import pygame as pg
import math
import random

from Const import *


class Mob(object):

    def __init__(self, x_pos, y_pos, name, index):

        self.pos_x = x_pos
        self.x_vel = math.pow(-1, index) * MOB_SLOW_SPEED
        self.y_vel = 0
        self.name = name
        self.index = index
        self.on_ground = False
        self.dead = False
        self.collided = False

        if self.x_vel < 0:
            self.image = pg.image.load('Assets/images/' + self.name + '_0.png')
        else:
            self.image = pg.image.load('Assets/images/' + self.name + '_1.png')
        self.sprites = []
        self.spriteTick = 0
        self.load_sprites()

        width = self.image.get_width()
        height = self.image.get_height()
        self.rect = pg.Rect(x_pos, y_pos - (height - 32), width, height)

    def load_sprites(self):
        self.sprites = [
            # 0
            pg.image.load('Assets/images/' + self.name + '_0.png'),

            # 1
            pg.image.load('Assets/images/' + self.name + '_1.png')]

        # Left side
        for i in range(len(self.sprites)):
            self.sprites.append(pg.transform.flip(self.sprites[i], 180, 0))
        # Dead
        self.sprites.append(pg.image.load('Assets/images/' + self.name + '_dead.png'))

    def update(self, core):
        self.mob_physics(core)
        self.update_image()

    def get_killed(self):
        self.dead = True
        self.x_vel = 0
        self.y_vel = 2.0

    def mob_physics(self, core):
        blocks = core.get_map().get_blocks_for_collision(self.rect.x // 32, self.rect.y // 32)
        mobs = core.get_map().get_mobs()
        player = core.get_map().get_player()

        self.rect.y += self.y_vel
        self.update_y_pos(blocks)

        self.pos_x += self.x_vel
        self.rect.x = self.pos_x
        self.update_x_pos(blocks, mobs, player)

        for block in core.get_map().get_blocks_below(self.rect.x // 32, self.rect.y // 32):
            if block != 0 and block.type != 'BGObject':

                if pg.Rect(self.rect.x, self.rect.y + 1, self.rect.w, self.rect.h).colliderect(block.rect):
                    self.on_ground = True


    def update_x_pos(self, blocks, mobs, player):

        if self.rect.left < 0:
            self.rect.left = 0
            self.pos_x = self.rect.left
            self.x_vel = MOB_SLOW_SPEED
        elif self.rect.right > WINDOW_W:
            pass

        for mob in mobs:
            if self.index == mob.index:
                continue
            if pg.Rect.colliderect(self.rect, mob.rect):
                if self.x_vel > 0:
                    # self.rect.right = mob.rect.left
                    # self.pos_x = self.rect.left
                    self.x_vel = -MOB_SLOW_SPEED
                elif self.x_vel < 0:
                    # self.rect.left = mob.rect.right
                    # self.pos_x = self.rect.left
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

    def update_y_pos(self, blocks):

        self.on_ground = False

        if self.rect.top > WINDOW_H:
            self.rect.top = WINDOW_H
            self.y_vel = 0
            self.on_ground = True

        # If it is dead keep falling ignoring blocks
        if self.dead:
            return
        # If alive
        for block in blocks:
            if block != 0 and block.type != 'BGObject':
                if pg.Rect.colliderect(self.rect, block.rect):
                    if self.y_vel > 0:
                        self.on_ground = True
                        self.rect.bottom = block.rect.top
                        self.y_vel = 0
                    elif self.y_vel < 0:
                        self.rect.top = block.rect.bottom
                        self.y_vel = -self.y_vel / 3


    def set_image(self, image_id):
        if self.x_vel < 0:
            self.image = self.sprites[image_id]
        else:
            self.image = self.sprites[image_id + 2]

    def update_image(self):

        if self.dead:
            self.image = self.sprites[4]
            return

        self.spriteTick += 1
        if self.spriteTick > 20:
            self.spriteTick = 0
        if self.spriteTick <= 10:
            self.set_image(0)
        elif 11 <= self.spriteTick <= 20:
            self.set_image(1)
        elif self.spriteTick == 21:
            self.spriteTick = 0
            self.set_image(0)

    def render(self, core):
        core.screen.blit(self.image, core.get_map().get_Camera().apply(self))

