import pygame as pg
from Const import *
import ResourcePath


class Item(object):
  def __init__(self, x_pos, y_pos, name):
    self.pos_x = x_pos
    self.name = name
    self.x_vel = 0
    self.y_vel = 0
    self.on_ground = False
    self.activated = False
    self.eaten = False
    self.image = None

  def render(self, core):
    if not self.activated:
      return
    core.screen.blit(self.image, core.get_map().get_Camera().apply(self))

  def get_activated(self, core):
    self.activated = True

class Coin(Item):
  def __init__(self, x_pos, y_pos, name):
    super().__init__(x_pos, y_pos, name)
    image_path = ResourcePath.resource_path('Assets/images/' + self.name + '_an0.png')
    self.image = pg.image.load(image_path)
    width = self.image.get_width()
    height = self.image.get_height()
    self.rect = pg.Rect(x_pos, y_pos - (height - 32), width, height)
    self.start_pos = self.rect.bottom
    self.y_vel = -MAX_FALL_SPEED
    self.sprites = []
    self.spriteTick = 0
    self.load_sprites()

  def load_sprites(self):
    for i in range(0, 4):
      image_path = ResourcePath.resource_path('Assets/images/' + self.name + '_an' + str(i) + '.png')
      self.sprites.append(pg.image.load(image_path))

  def update(self, core): # no concern with block
    if not self.activated:
      return
    self.item_physics()
    self.update_image()

  def item_physics(self):
    if not self.on_ground:
      self.y_vel += GRAVITY * FALL_MULTIPLIER
    if self.y_vel > MAX_FALL_SPEED:
      self.y_vel = MAX_FALL_SPEED

    # just update y pos
    self.rect.y += self.y_vel
    self.update_y_pos()

  def update_y_pos(self):
    if self.rect.bottom >= self.start_pos:
      self.activated = False

  def update_image(self):

    self.spriteTick += 1
    if self.spriteTick >= 8:
      self.spriteTick = 0
    if self.spriteTick < 1:
      self.image = self.sprites[0]
    elif 2 <= self.spriteTick < 4:
      self.image = self.sprites[1]
    elif 4 <= self.spriteTick < 6:
      self.image = self.sprites[2]
    elif 6 <= self.spriteTick < 8:
      self.image = self.sprites[3]
    elif self.spriteTick == 8:
      self.spriteTick = 0
      self.image = self.sprites[0]

  def get_activated(self, core):
    if not self.eaten:
      self.eaten = True
      core.get_map().get_player().incr_coin()
    self.activated = True

  def get_eaten(self): # player gets point
    pass


class Mushroom(Item):
  def __init__(self, x_pos, y_pos, name):
    super().__init__(x_pos, y_pos, name)
    self.image = pg.image.load('Assets/images/' + self.name + '.png')
    width = self.image.get_width()
    height = self.image.get_height()
    self.rect = pg.Rect(x_pos, y_pos - (height - 32), width, height)
    self.start_pos = self.rect.top
    self.y_vel = -MOB_SLOW_SPEED / 2
    self.rising = True

  def update(self, core):
    if not self.activated:
      return
    self.item_physics(core)

  def item_physics(self, core):

    if self.rising and self.rect.bottom == self.start_pos: # stop going up
      self.rising = False
      self.x_vel = MOB_SLOW_SPEED
      self.y_vel = 0

    blocks = core.get_map().get_blocks_for_collision(self.rect.x // 32, self.rect.y // 32)

    if not self.on_ground:
      self.y_vel += GRAVITY * FALL_MULTIPLIER
    if self.y_vel > MAX_FALL_SPEED:
      self.y_vel = MAX_FALL_SPEED

    self.rect.y += self.y_vel
    if not self.rising:
      self.update_y_pos(blocks)

    self.pos_x += self.x_vel
    self.rect.x = self.pos_x
    if not self.rising:
      self.update_x_pos(blocks)

  def update_x_pos(self, blocks):

    if self.rect.right < 0:
      self.activated = False
      return

    for block in blocks:
      if block != 0 and block.type != 'BGObject':
        block.debugLight = True
        if pg.Rect.colliderect(self.rect, block.rect):
          if self.x_vel > 0:
            self.rect.right = block.rect.left
            self.pos_x = self.rect.left
            self.x_vel *= -1
          elif self.x_vel < 0:
            self.rect.left = block.rect.right
            self.pos_x = self.rect.left
            self.x_vel *= -1

  def update_y_pos(self, blocks):
    self.on_ground = False

    if self.rect.top > WINDOW_H:
      self.activated = False
      return

    for block in blocks:
      if block != 0 and block.type != 'BGObject':
        if pg.Rect.colliderect(self.rect, block.rect):
          if self.y_vel > 0:
            self.on_ground = True
            self.rect.bottom = block.rect.top
            self.y_vel = 0
          # mushroom cannot jump
          # elif self.y_vel < 0:
          #   self.rect.top = block.rect.bottom
          #   self.y_vel = -self.y_vel / 3

  def get_eaten(self):  # player gets bigger
    pass






class Flower(Item):
  def __init__(self, x_pos, y_pos, name):
    super().__init__(x_pos, y_pos, name)
    self.image = pg.image.load('Assets/images/' + self.name + '0.png')
    width = self.image.get_width()
    height = self.image.get_height()
    self.rect = pg.Rect(x_pos, y_pos - (height - 32), width, height)
    self.sprites = []
    self.spriteTick = 0
    self.load_sprites()

  def load_sprites(self):
    for i in range(0, 4):
      self.sprites.append(pg.image.load('Assets/images/' + self.name + '_an' + str(i) + '.png'))

  def update(self, core):  # no concern with block
    if not self.activated:
      return
    self.update_image()

  def update_image(self):
    self.spriteTick += 1
    if self.spriteTick > 20:
      self.spriteTick = 0
    if self.spriteTick <= 5:
      self.image = self.sprites[0]
    elif 5 < self.spriteTick <= 10:
      self.image = self.sprites[1]
    elif 11 < self.spriteTick <= 15:
      self.image = self.sprites[2]
    elif 15 < self.spriteTick <= 20:
      self.image = self.sprites[3]
    elif self.spriteTick == 21:
      self.spriteTick = 0
      self.image = self.sprites[0]

  def get_eaten(self):  # player can throw fire
    pass
