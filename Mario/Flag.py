import pygame as pg
import ResourcePath

class Flag(pg.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()

        self.image = pg.image.load(ResourcePath.resource_path('Assets/images/flag_pillar.png'))
        length = (12 - y_pos) * 32
        #self.image = self.image.subsurface(0, 0, 16, length)

        self.rect = pg.Rect(x_pos*32, y_pos*32, 5, length)


    def render(self, core):
        core.screen.blit(self.image, core.get_map().get_Camera().apply(self))
