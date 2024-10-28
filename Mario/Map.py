import pygame as pg
from pytmx.util_pygame import load_pygame
from GameUI import GameUI
from Event import Event
from Const import *
from Platform import Platform
from Camera import Camera
from Player import Player
from Mob import Mob
from Item import *
from MenuManager import MenuManager
from Tube import Tube
from Flag import Flag
from BGObject import BGObject

class Map(object):
    """

    This class will contain every map object: tiles, mobs and player. Also,
    there are camera, event and UI.

    """

    def __init__(self, world_num):
        self.obj = [] #Foreground objects
        self.obj_bg = [] #Background objects

        self.flags = []
        self.tubes = []

        self.debris = []
        self.mobs = []
        self.items = []
        self.projectiles = []
        self.text_objects = []
        self.map = 0
        #self.flag = None

        self.mapSize = (0, 0) #width, height
        self.sky = 0          #surface

        self.textures = {}
        self.worldNum = world_num
        self.loadWorld()

        # self.is_mob_spawned = [False, False]
        self.score_for_killing_mob = 100
        self.score_time = 0

        self.in_event = False
        self.tick = 0
        self.time = 400

        self.oEvent = Event()
        self.oGameUI = GameUI()
        self.oCamera = Camera(self.mapSize[0] * 32, 14)

        self.oPlayer = Player(x_pos=128, y_pos=351)
        self.oGameUI = GameUI()

    def get_time(self):
        return (self.time)

    def loadWorld(self):
        tmx_data = load_pygame("Assets/worlds/tmx/W11.tmx")
        self.mapSize = (tmx_data.width, tmx_data.height)

        self.sky = pg.Surface((WINDOW_W, WINDOW_H))
        self.sky.fill((pg.Color('#5c94fc'))) #Background color

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

                            # 22 ID is a question block, so in that case we should load all it's images
                            if tileID == 22:
                                image = (
                                    image,  # 1
                                    tmx_data.get_tile_image(0, 15, layer_num),  # 2
                                    tmx_data.get_tile_image(1, 15, layer_num),  # 3
                                    tmx_data.get_tile_image(2, 15, layer_num)  # activated
                                )

                            self.map[x][y] = Platform(x * tmx_data.tileheight, y * tmx_data.tilewidth, image, tileID)
                            self.obj.append(self.map[x][y])
                            if tileID == 22:
                                self.items.append(self.map[x][y].item)

                        if layer.name == 'Background':
                            self.map[x][y] = BGObject(x * tmx_data.tileheight, y * tmx_data.tilewidth, image)
                            self.obj_bg.append(self.map[x][y])
            layer_num += 1

        # tubes collection
        #self.spawn_flag(1, 1.5)
        self.spawn_flag(198.25,1.5)
        self.spawn_tube(28, 10)
        self.spawn_tube(37, 9)#9
        self.spawn_tube(46, 9)#8
        self.spawn_tube(55, 9)#8
        self.spawn_tube(163, 10)
        self.spawn_tube(179, 10)
        self.spawn_mob(900, 351, 'goombas')
        self.spawn_mob(700, 351, 'goombas')
        self.spawn_mob(230, 351, 'koopa')

    def get_player(self):
        return self.oPlayer

    def get_is_player_dead(self):
        return self.oPlayer.get_isdead()

    def get_mobs(self):
        return self.mobs

    def get_mobs_xPos(self):
        mobs_pos = []
        for mob in self.mobs:
            if not mob.dead:
                mobs_pos.append(mob.pos_x)
        if len(mobs_pos) <= 0:
            return None
        return mobs_pos

    def get_items(self):
        return self.items

    def get_Camera(self):
        return self.oCamera

    def get_name(self):
        if self.worldNum == '1-1':
            return '1-1'

    def get_ui(self):
        return self.oGameUI

    def spawn_flag(self, x_coord, y_coord):
        self.flags.append(Flag(x_coord, y_coord))

    def get_event(self):
        return self.oEvent

    def set_event(self):
        self.in_event = True

    def spawn_tube(self, x_coord, y_coord):
        self.tubes.append(Tube(x_coord, y_coord))

        for y in range(y_coord, 12):  # 12 is because it ground level
            for x in range(x_coord, x_coord + 2):
                self.map[x][y] = Platform(x * 32, y * 32, image=None, type_id=100)

    def spawn_mob(self, x_pos, y_pos, name):
        index = len(self.mobs)
        self.mobs.append(Mob(x_pos, y_pos, name, index))

    def spawn_item(self, x_pos, y_pos, itemID):
        if itemID == 0: # coin
            self.items.append(Coin(x_pos, y_pos, 'coin'))
        elif itemID == 1: # mushroom
            self.items.append(Mushroom(x_pos, y_pos, 'mushroom'))
        elif itemID == 2: # flower
            self.items.append(Flower(x_pos, y_pos, 'flower'))


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

    def get_block_id(self, x, y):
        if self.map[x][y] != 0 and self.map[x][y].type != 'BGObject':
            return ((self.map[x][y]).get_id())

    def set_block_shake(self, x, y):
        if self.map[x][y] != 0 and self.map[x][y].type != 'BGObject':
            if (self.map[x][y]).get_id() == 22 or 23:
                self.map[x][y].set_shake_true()

    def get_blocks_below(self, x, y):
        # return two blocks where player is standing
        return (
            self.map[x][y + 1],
            self.map[x + 1][y + 1]
        )

    def get_rect_block(self, x, y):
        if self.map[x][y] != 0 and self.map[x][y].type != 'BGObject':
            return (self.map[x][y]).get_id()
        return 0

    def get_near_blocks(self):
        player_x_cord = self.get_player().rect.x // 32
        player_y_cord = self.get_player().rect.y // 32

        # check player 4-dir blocks
        # right block
        right_block = self.get_rect_block(player_x_cord + 2, player_y_cord)
        #left block
        left_block = self.get_rect_block(player_x_cord - 1, player_y_cord)
        #upper block
        upper_block = self.get_rect_block(player_x_cord, player_y_cord - 1)
        #upper right block
        upper_r_block = self.get_rect_block(player_x_cord + 2, player_y_cord - 1)
        # #down block
        # down_block = self.get_rect_block(player_x_cord, player_y_cord + 1)
        if right_block > 0:
            right_block = 1
        else:
            right_block = 0

        if left_block > 0:
            left_block = 1
        else:
            left_block = 0

        if upper_block > 0:
            upper_block = 1
        else:
            upper_block = 0

        if upper_r_block > 0:
            upper_r_block = 1
        else: upper_r_block = 0

        blocks = [right_block, left_block, upper_block, upper_r_block]
        return blocks

    def get_block_height(self):
        return 0

    def update_player(self, core):
        self.get_player().update(core)

    def update_mobs(self, core):
        for mob in self.mobs:
            mob.update(core)

    def update_items(self, core):
        for item in self.items:
            item.update(core)

    def update(self, core):
        if not self.in_event:
            self.update_player(core)
            self.update_mobs(core)
            self.update_items(core)
            # this is code to make move for the camera
            self.get_Camera().update(core.get_map().get_player().rect)
        else:
            print("map in event")
            self.get_event().update(core)
        #update time ui
        self.update_time(core)


    def update_time(self, core):
        """
        Updating a map time.
        """
        # Time updates only if map not in event
        if not self.in_event:
            self.tick += 1
            if self.tick % 40 == 0:
                self.time -= 1
                self.tick = 0
            # if self.time == 100 and self.tick == 1:
            #     core.get_sound().start_fast_music(core)

    def render_map(self, core):

        core.screen.blit(self.sky, (0, 0))

        for obj_group in (self.obj_bg, self.obj):
            for obj in obj_group:
                obj.render(core)

        for tube in self.tubes:
            tube.render(core)

        for flag in self.flags:
            flag.render(core)

    def render(self, core):

        core.screen.blit(self.sky, (0, 0))

        for obj in self.obj_bg:
            obj.render(core)  # clouds and so on

        for tube in self.tubes:
            tube.render(core)

        for flag in self.flags:
            flag.render(core)

        for obj in self.obj:
            obj.render(core)  # bricks

        for mob in self.mobs:
            mob.render(core)

        for item in self.items:
            item.render(core)

        self.get_player().render(core)  # player

        self.get_ui().render(core) #UI
