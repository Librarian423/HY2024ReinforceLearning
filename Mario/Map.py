import pygame as pg
from pytmx.util_pygame import load_pygame

from GameUI import GameUI

from Event import Event

from Const import *
from Platform import Platform

from Camera import Camera
from Player import Player

from Tube import Tube

from BGObject import BGObject
class Map(object):
    """

    This class will contain every map object: tiles, mobs and player. Also,
    there are camera, event and UI.

    """

    def __init__(self, world_num):
        self.obj = []
        self.obj_bg = []
        
        self.tubes = []

        self.debris = []
        self.mobs = []
        self.projectiles = []
        self.text_objects = []
        self.map = 0
        self.flag = None

        self.mapSize = (0, 0)
        self.sky = 0

        self.textures = {}
        self.worldNum = world_num
        self.loadWorld_11()

        self.is_mob_spawned = [False, False]
        self.score_for_killing_mob = 100
        self.score_time = 0

        self.in_event = False
        self.tick = 0
        self.time = 400

        self.oEvent = Event()
        self.oGameUI = GameUI()
        self.oCamera = Camera(self.mapSize[0] * 32, 14)


        self.oPlayer = Player(x_pos=128, y_pos=351)

    def loadWorld_11(self):
        tmx_data = load_pygame("Next/worlds/tmx/W11.tmx")
        self.mapSize = (tmx_data.width, tmx_data.height)

        self.sky = pg.Surface((WINDOW_W, WINDOW_H))
        self.sky.fill((pg.Color('#5c94fc')))

        # 2D List
        self.map = [[0] * tmx_data.height for i in range(tmx_data.width)]

        

        layer_num = 0
        for layer in tmx_data.visible_layers:
            for y in range(tmx_data.height):
                for x in range(tmx_data.width):

                    # Getting pygame surface
                    image = tmx_data.get_tile_image(x, y, layer_num)

                    # It's none if there are no tile in that place
                    if image is not None:
                        tileID = tmx_data.get_tile_gid(x, y, layer_num)

                        if layer.name == 'Foreground':

                            # 22 ID is a question block, so in taht case we shoud load all it's images
                            if tileID == 22:
                                image = (
                                    image,                                      # 1
                                    tmx_data.get_tile_image(0, 15, layer_num),   # 2
                                    tmx_data.get_tile_image(1, 15, layer_num),   # 3
                                    tmx_data.get_tile_image(2, 15, layer_num)    # activated
                                )

                            self.map[x][y] = Platform(x * tmx_data.tileheight, y * tmx_data.tilewidth, image, tileID)
                            self.obj.append(self.map[x][y])

                        if layer.name == 'Background':
                            self.map[x][y] = BGObject(x * tmx_data.tileheight, y * tmx_data.tilewidth, image)
                            self.obj_bg.append(self.map[x][y])
            layer_num += 1

      
        #tubes collection
        self.spawn_tube(28, 10)
        self.spawn_tube(37, 9)
        self.spawn_tube(46, 8)
        self.spawn_tube(55, 8)
        self.spawn_tube(163, 10)
        self.spawn_tube(179, 10)


    def get_player(self):
        return self.oPlayer

    def get_Camera(self):
        return self.oCamera


    def spawn_tube(self, x_coord, y_coord):
        self.tubes.append(Tube(x_coord, y_coord))

        for y in range(y_coord, 12): #12 is because it ground level
            for x in range(x_coord, x_coord + 2):
                self.map[x][y] = Platform(x*32, y*32, image = None, type_id= 0)
            


    # Returns tiles around the entity
    def get_blocks_for_collision(self, x, y):
        
        return (
            self.map[x][y - 1],
            self.map[x][y + 1],
            self.map[x][y],
            self.map[x - 1][y],
            self.map[x + 1][y],
            self.map[x + 2][y],
            self.map[x + 1][y - 1],
            self.map[x + 1][y + 1],
            self.map[x][y + 2],
            self.map[x + 1][y + 2],
            self.map[x - 1][y + 1],
            self.map[x + 2][y + 1],
            self.map[x][y + 3],
            self.map[x + 1][y + 3]
        )

 

#code to get position where player is currently standing on the gound
    
    def get_blocks_below(self, x, y):
        #return two blocks where player is standing
        return (
            self.map[x][y + 1],
            self.map[x+ 1][y + 1]
        )




    def update_player(self, core):
        self.get_player().update(core)

   


    def update(self, core):

        
        if not core.get_map().in_event:
            self.update_player(core)

        else:
            self.get_event().update(core)

        #this is code to make move for the camera
        if not self.in_event:
            self.get_Camera().update(core.get_map().get_player().rect)
      
        
    
    def render_map(self, core):
        """

        Rendering only tiles. It's used in main menu.

        """
        core.screen.blit(self.sky, (0, 0))

        for obj_group in (self.obj_bg, self.obj):
            for obj in obj_group:
                obj.render(core)

        for tube in self.tubes:
            tube.render(core)

    def render(self, core):
        """

        Renders every object.

        """
        core.screen.blit(self.sky, (0, 0))

        for obj in self.obj_bg:
            obj.render(core) #clouds and so on


        for tube in self.tubes:
            tube.render(core)

        for obj in self.obj:
            obj.render(core) #bricks

        self.get_player().render(core) #player

     
























