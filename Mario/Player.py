import pygame as pg
from Const import *
from pygame.locals import QUIT,Rect



class Player(object):
    def __init__(self, x_pos, y_pos):
        # life
        self.numOfLives = 3
        self.score = 0
        self.coins = 0

        self.visible = True
        self.spriteTick = 0
        self.powerLVL = 0

        self.unkillable = False
        self.unkillableTime = 0

        self.inLevelUpAnimation = False
        self.inLevelUpAnimationTime = 0
        self.inLevelDownAnimation = False
        self.inLevelDownAnimationTime = 0

        self.already_jumped = False
        self.next_jump_time = 0
        self.next_fireball_time = 0
        self.x_vel = 0
        self.y_vel = 0
        self.direction = True
        self.on_ground = False
        self.fast_moving = False

        self.pos_x = x_pos
        self.pos_y = y_pos

        self.sprites = []
        self.load_sprites()

        self.rect = pg.Rect(x_pos, y_pos, 32, 32)
        self.groundRect = pg.Rect(x_pos+8, y_pos+28, 16, 4)
        self.hitBlockRect = pg.Rect(x_pos, y_pos, 25, 5)
    def get_score(self):
        return self.score

    def updateRectPos(self):
        self.hitBlockRect.x = self.rect.x
        self.hitBlockRect.y = self.rect.y
        self.hitBlockRect.x += 5
        self.hitBlockRect.y -= 1
        # print("x hit " + str(self.hitBlockRect.x))
        # print("y hit " + str(self.hitBlockRect.y))
        # print("\n---------------------------\n")
    def load_sprites(self):
        self.sprites = [
            # 0 Small, stay
            # 0 Small, stay
            pg.image.load('Assets/images/Mario/mario.png'),

            # 1 Small, move 0
            pg.image.load('Assets/images/Mario/mario_move0.png'),

            # 2 Small, move 1
            pg.image.load('Assets/images/Mario/mario_move1.png'),

            # 3 Small, move 2
            pg.image.load('Assets/images/Mario/mario_move2.png'),

            # 4 Small, jump
            pg.image.load('Assets/images/Mario/mario_jump.png'),

            # 5 Small, end 0
            pg.image.load('Assets/images/Mario/mario_end.png'),

            # 6 Small, end 1
            pg.image.load('Assets/images/Mario/mario_end1.png'),

            # 7 Small, stop
            pg.image.load('Assets/images/Mario/mario_st.png')]

        # Left side
        for i in range(len(self.sprites)):
            self.sprites.append(pg.transform.flip(self.sprites[i], 180, 0))

        # Dead(should always be at last)
        self.sprites.append(pg.image.load('Assets/images/Mario/mario_death.png'))


    def update(self, core):
        if self.player_physics(core):
            self.update_image(core)
            self.updateRectPos()
            self.has_reached_flag(core)

    def die(self, core):
        self.numOfLives -= 1
        core.get_map().get_event().start_kill(core, not self.numOfLives)

    def player_physics(self, core):
        if core.keyR:
            self.x_vel += SPEED_INCREASE_RATE
            self.direction = True
        if core.keyL:
            self.x_vel -= SPEED_INCREASE_RATE
            self.direction = False
        if not core.keyU:
            self.already_jumped = False  # why?
        elif core.keyU:
            if self.on_ground and not self.already_jumped:
                self.y_vel = -JUMP_POWER
                self.already_jumped = True
                self.next_jump_time = pg.time.get_ticks() + 750

        # if player is not playing game, decrease the speed of the Mario
        if not (core.keyR or core.keyL):
            if self.x_vel > 0:
                self.x_vel -= SPEED_DECREASE_RATE

            elif self.x_vel < 0:
                self.x_vel += SPEED_DECREASE_RATE


        else:
            # restrain like threshold which player MArio cannot pass
            if self.x_vel > 0:
                if self.fast_moving:
                    if self.x_vel > MAX_FASTMOVE_SPEED:
                        self.x_vel = MAX_FASTMOVE_SPEED

                    else:
                        if self.x_vel > MAX_MOVE_SPEED:
                            self.x_vel = MAX_MOVE_SPEED

            # move in left direction
            if self.x_vel < 0:
                if self.fast_moving:
                    if (-self.x_vel) > MAX_FASTMOVE_SPEED:
                        self.x_vel = -MAX_FASTMOVE_SPEED

                    else:
                        if (-self.x_vel) > MAX_MOVE_SPEED:
                            self.x_vel = -MAX_MOVE_SPEED

        # write a code for solving computational error
        if 0 < self.x_vel < SPEED_DECREASE_RATE:
            self.x_vel = 0
            self.groundRect.x = self.pos_x+6

        if 0 > self.x_vel > -SPEED_DECREASE_RATE:
            self.x_vel = 0
            self.groundRect.x = self.pos_x+6

        # introduce a proper movement of leg of mario
        # moving Up i/e. JUMP action for MARIO
        if not self.on_ground:
            # button up is pressed
            if (self.y_vel < 0 and core.keyU):
                self.y_vel += GRAVITY

            elif (self.y_vel < 0 and not core.keyU):
                self.y_vel += GRAVITY * LOW_JUMP_MULTIPLIER

            # moving down
            else:
                self.y_vel += GRAVITY * FALL_MULTIPLIER

            if self.y_vel > MAX_FALL_SPEED:
                self.y_vel = MAX_FALL_SPEED

        blocks = core.get_map().get_blocks_for_collision(self.rect.x // 32, self.rect.y // 32)
        mobs = core.get_map().get_mobs()

        self.pos_x += self.x_vel
        self.rect.x = self.pos_x
        self.groundRect.x = self.pos_x+6

        # this function allows to stop when player collides with bricks
        self.update_x_pos(core, blocks, mobs)

        self.rect.y += self.y_vel
        self.update_y_pos(blocks, mobs, core)
        if core.get_map().get_event().killed:
            return False

        # on_ground() parameter won't be stable without the following code:
        # pygame x and y represents top left corner of pygame window
        coord_y = self.rect.y // 32
        if self.powerLVL > 0:
            coord_y += 1
        # main code
        for block in core.get_map().get_blocks_below(self.rect.x // 32, coord_y):
            if block != 0 and block.type != 'BGObject':

                if pg.Rect(self.rect.x, self.rect.y + 1, self.rect.w, self.rect.h).colliderect(block.rect):
                    self.on_ground = True

        return True



    def update_x_pos(self, core, blocks, mobs):

        if self.rect.left < 0:
            self.die(core)
            # self.rect.left = 0
            # self.pos_x = self.rect.left
            # self.x_vel = 0

        elif self.rect.right > WINDOW_W:
            pass

        for block in blocks:
            if block != 0 and block.type != 'BGObject':
                block.debugLight = True
                if pg.Rect.colliderect(self.rect, block.rect):
                    if self.x_vel > 0:
                        self.rect.right = block.rect.left
                        self.pos_x = self.rect.left
                        self.x_vel = 0  # idle stop moving
                    elif self.x_vel < 0:
                        self.rect.left = block.rect.right
                        self.pos_x = self.rect.left
                        self.x_vel = 0

        for mob in mobs:
            if mob.dead and mob.name != "koopa":
                continue
            if pg.Rect.colliderect(self.rect, mob.rect):
                mob.collided = True
                # if self.x_vel > 0:
                #     self.rect.right = mob.rect.left
                #     self.pos_x = self.rect.left
                #     self.x_vel = 0
                # elif self.x_vel < 0:
                #     self.rect.left = mob.rect.right
                #     self.pos_x = self.rect.left
                #     self.x_vel = 0



    def update_y_pos(self, blocks, mobs, core):

        # WINDOW_H???
        if self.rect.bottom > WINDOW_H:
            self.die(core)
            return

        self.on_ground = False
        for block in blocks:
            if block != 0 and block.type != 'BGObject':
                # Reset hitblockRect position
                # self.hitBlockRect.x = self.rect.x
                # self.hitBlockRect.y = self.rect.y
                if pg.Rect.colliderect(self.hitBlockRect, block.rect):
                    blockX = block.rect.left // 32
                    blockY = block.rect.top // 32
                    self.check_upper_block(blockX, blockY,self.hitBlockRect, core)
                if pg.Rect.colliderect(self.rect, block.rect):
                    #self.check_upper_block(self.rect, core)
                    if self.y_vel > 0:
                        self.on_ground = True
                        self.rect.bottom = block.rect.top
                        self.y_vel = 0

                    elif self.y_vel < 0:
                        self.rect.top = block.rect.bottom
                        self.y_vel = -self.y_vel / 3

        for mob in mobs:
            if not mob.collided:
                continue
            mob.collided = False
            if mob.weaponized:
                self.die(core)
                return
            if self.y_vel > 0:
                self.rect.bottom = mob.rect.top
                self.y_vel = -self.y_vel
                if not mob.dead:
                    self.score += SCORES[mob.name]
                    mob.get_killed(0)
                else:  # koopa
                    mob.get_weaponized(self.x_vel)
            else:
                if not mob.dead:
                    self.die(core)
                else:
                    mob.get_weaponized(self.x_vel)

        #self.hitBlockRect.y = self.rect.y

        #print("y rect " + str(self.rect.y))

    def check_upper_block(self, xCord, yCord,  character, core):

        # x_temp = character.x // 32
        # #x_temp = int(tc.clamp(x_temp, min=x_temp-0.5, max=x_temp+0.5))
        # y_temp = character.y // 32
        # print(x_temp, y_temp)
        # print("block id",core.get_map().get_block_id(x_temp, y_temp))
        if core.get_map().get_block_id(xCord, yCord) == 22:
            core.get_map().set_block_shake(xCord, yCord)
            #print("hit")
        # elif core.get_map().get_block_id(x_temp+1, y_temp) == 22:
        #     core.get_map().set_block_shake(x_temp+1, y_temp)
        #     print("hit")
        # elif core.get_map().get_block_id(x_temp-1, y_temp) == 22:
        #     core.get_map().set_block_shake(x_temp-1, y_temp)
        #     print("hit")

        if core.get_map().get_block_id(xCord, yCord) == 23:
            #print("shake")
            core.get_map().set_block_shake(xCord, yCord)
            #print("hit")
        # elif core.get_map().get_block_id(x_temp+1, y_temp) == 23:
        #     core.get_map().set_block_shake(x_temp+1, y_temp)
        #     print("hit")
        # elif core.get_map().get_block_id(x_temp-1, y_temp) == 23:
        #     core.get_map().set_block_shake(x_temp-1, y_temp)
        #     print("hit")



    def activate_block_action(self, core, block):
        pass

    def set_image(self, image_id):
        if image_id == -1: # player dead
            self.image = self.sprites[len(self.sprites) - 1]
            return

        if self.direction:
            self.image = self.sprites[image_id % 8]
        else:
            self.image = self.sprites[(image_id % 8) + 8]

    def update_image(self, core):

        self.spriteTick += 1
        if (core.keyShift):
            self.spriteTick += 1

        if self.powerLVL in (0, 1, 2):

            if self.x_vel == 0:
                self.set_image(0)
                self.spriteTick = 0

            # Player is running
            elif (
                    ((self.x_vel > 0 and core.keyR and not core.keyL) or
                     (self.x_vel < 0 and core.keyL and not core.keyR)) or
                    (self.x_vel > 0 and not (core.keyL or core.keyR)) or
                    (self.x_vel < 0 and not (core.keyL or core.keyR))
            ):

                if (self.spriteTick > 30):
                    self.spriteTick = 0

                if self.spriteTick <= 10:
                    self.set_image(1)
                elif 11 <= self.spriteTick <= 20:
                    self.set_image(2)
                elif 21 <= self.spriteTick <= 30:
                    self.set_image(3)
                elif self.spriteTick == 31:
                    self.spriteTick = 0
                    self.set_image(1)

            # Player decided to move in the another direction, but hasn't stopped yet
            elif (self.x_vel > 0 and core.keyL and not core.keyR) or (self.x_vel < 0 and core.keyR and not core.keyL):
                self.set_image(8)
                self.spriteTick = 0

            if not self.on_ground:
                self.spriteTick = 0
                self.set_image(4)

    def render(self, core):
        #pg.draw.rect(core.screen, (255, 255, 255), self.hitBlockRect)
        if self.visible:
            core.screen.blit(self.image, core.get_map().get_Camera().apply(self))

    def has_reached_flag(self, core):
        # 깃대에 도달했는지 확인하는 로직을 구현
        flag_x_position = 6341.25  # 깃대의 x 좌표 예시
        if flag_x_position <= self.pos_x:
            core.reached_flag()