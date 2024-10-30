import pygame as pg
import math
import random
import ResourcePath

from Const import *


class Mob(object):

    def __init__(self, x_pos, y_pos, name, index):

        self.name = name
        self.pos_x = x_pos
        if index % 2 :
            self.x_vel = -MOB_SLOW_SPEED
            self.image = pg.image.load(ResourcePath.resource_path('Assets/images/' + self.name + '_0.png'))
        else :
            self.x_vel = MOB_SLOW_SPEED
            self.image = pg.image.load(ResourcePath.resource_path('Assets/images/' + self.name + '_1.png'))
        self.y_vel = 0
        self.index = index
        self.on_ground = False

        self.state = NORMAL
        self.collided = False

        self.sprites = []
        self.spriteTick = 0
        self.load_sprites()

        width = self.image.get_width()
        height = self.image.get_height()
        self.rect = pg.Rect(x_pos, y_pos - (height - 32), width, height)

    def load_sprites(self):
        self.sprites = [
            # 0
            pg.image.load(ResourcePath.resource_path('Assets/images/' + self.name + '_0.png')),

            # 1
            pg.image.load(ResourcePath.resource_path('Assets/images/' + self.name + '_1.png'))]

        # Left side
        for i in range(len(self.sprites)):
            self.sprites.append(pg.transform.flip(self.sprites[i], 180, 0))
        # Dead
        self.sprites.append(pg.image.load(ResourcePath.resource_path('Assets/images/' + self.name + '_dead.png')))

    def update(self, core):
        if self.state == GONE:
            return
        self.mob_physics(core)
        self.update_image()

    def get_state(self):
        return self.state

    def is_collided(self):
        return self.collided

    def collide(self):
        self.collided = True

    def uncollide(self):
        self.collided = False

    def get_killed(self, weapon_vel):
        self.image = self.sprites[4]

        if self.name == "koopa":
            self.state = UNDEAD
            width = self.image.get_width()
            height = self.image.get_height()
            self.rect = pg.Rect(self.rect.x, self.rect.y + 14, width, height)
        else:
            self.state = DEAD

        if weapon_vel:
            self.spriteTick = -1  # do not update image
            self.image = pg.transform.flip(self.image, 0, 180)
            self.x_vel = MOB_SLOW_SPEED * weapon_vel / abs(weapon_vel)
            self.y_vel = -JUMP_POWER
        else:
            self.spriteTick = 0
            self.x_vel = 0
            self.y_vel = 0

    def get_weaponized(self, player_vel):
        self.state = WEAPON
        if player_vel < 0:
            self.x_vel = -MOB_FAST_SPEED * 3
        else:
            self.x_vel = MOB_FAST_SPEED * 3

    def mob_physics(self, core):
        blocks = core.get_map().get_blocks_for_collision(self.rect.x // 32, self.rect.y // 32)
        mobs = core.get_map().get_mobs()
        player = core.get_map().get_player()

        if not self.on_ground:
            self.y_vel += GRAVITY * FALL_MULTIPLIER
        if self.y_vel > MAX_FALL_SPEED:
            self.y_vel = MAX_FALL_SPEED

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

        if self.rect.right < 0:
            # self.rect.left = 0
            # self.pos_x = self.rect.left
            # self.x_vel = MOB_SLOW_SPEED
            self.state = GONE
            return
        # elif self.rect.left > WINDOW_W:
        #     # self.rect.right = WINDOW_W
        #     # self.pos_x = self.rect.left
        #     # self.x_vel = MOB_SLOW_SPEED
        #     self.state = GONE
        #     return

        if self.state == DEAD:
            return

        for mob in mobs:
            if self.index == mob.index:
                continue
            if mob.state == DEAD or mob.state == GONE:
                continue
            if pg.Rect.colliderect(self.rect, mob.rect):
                if self.state == WEAPON:
                    mob.get_killed(self.x_vel)
                    player.score += SCORES[mob.name]
                    return
                # if self.x_vel > 0:
                    # self.rect.right = mob.rect.left
                    # self.pos_x = self.rect.left
                # elif self.x_vel < 0:
                    # self.rect.left = mob.rect.right
                    # self.pos_x = self.rect.left
                self.x_vel *= -1

        for block in blocks:
            if block != 0 and block.type != 'BGObject':
                block.debugLight = True
                if pg.Rect.colliderect(self.rect, block.rect):
                    if block.shaking:
                        self.get_killed(self.rect.centerx - block.rect.centerx)
                        return
                    if self.x_vel > 0:
                        self.rect.right = block.rect.left
                        self.pos_x = self.rect.left
                    elif self.x_vel < 0:
                        self.rect.left = block.rect.right
                        self.pos_x = self.rect.left
                    self.x_vel *= -1

    def update_y_pos(self, blocks):

        self.on_ground = False

        if self.rect.top > WINDOW_H:
            self.rect.top = WINDOW_H
            self.y_vel = 0
            self.state = GONE

        # DEAD라면 지형지물 무시한 채 떨어진다
        if self.state == DEAD:
            return

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

        if self.state == UNDEAD or self.state == WEAPON:
            return

        if self.state == DEAD:
            if self.spriteTick < 0:  # killed by koopa
                pass
            elif self.spriteTick < 40:  # 플레이어한테 죽었으나 시체가 남음
                self.spriteTick += 1
            else:  # 플레이어한테 죽고 시체도 사라짐
                self.state = GONE
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
        if self.state == GONE:
            return
        core.screen.blit(self.image, core.get_map().get_Camera().apply(self))