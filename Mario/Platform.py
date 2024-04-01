import pygame as pg


class Platform(object):
    def __init__(self, x, y, image, type_id):
        self.image = image
        self.rect = pg.Rect(x, y, 32, 32)

        # 22 - question block
        #3 --- question block
        # 23 - brick block
        self.typeID = type_id

        self.type = 'Platform'
        self.isActivated = True
        self.shaking = False
        self.shakingUp = True
        self.shakeOffset = 0

        if self.typeID == 22:
            self.currentImage = 0
            self.imageTick = 0
            self.isActivated = False
            self.bonus = 'coin'

    def update(self):
        if self.typeID == 22:
            self.imageTick += 1
            if self.imageTick == 50:
                self.currentImage = 1
            elif self.imageTick == 60:
                self.currentImage = 2
            elif self.imageTick == 70:
                self.currentImage = 1
            elif self.imageTick == 80:
                self.currentImage = 0
                self.imageTick = 0

    def shake(self):
        if self.shakingUp:
            self.shakeOffset -= 2
            self.rect.y -= 2
        else:
            self.shakeOffset += 2
            self.rect.y += 2
        if self.shakeOffset == -20:
            self.shakingUp = False
        if self.shakeOffset == 0:
            self.shaking = False
            self.shakingUp = True


    def render(self, core):
        # Question block
        if self.typeID == 22:
            if not self.isActivated:
                self.update()
            elif self.shaking:
                self.shake()
            core.screen.blit(self.image[self.currentImage], core.get_map().get_Camera().apply(self))

        # Brick block
        elif self.typeID == 23 and self.shaking:
            self.shake()
            core.screen.blit(self.image, core.get_map().get_Camera().apply(self))

        else:
            core.screen.blit(self.image, core.get_map().get_Camera().apply(self))
