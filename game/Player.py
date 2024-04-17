import pygame
from debug.logger import logger
import globalVars.SettingsConstants as globalVars
import gamedata.Save.SavedData as SAVED_DATA
import numpy as np
class PlayerPart(pygame.sprite.Sprite):
    def __init__(self,image: pygame.Surface, group: pygame.sprite.Group):
        super().__init__(group)
        self.offset = []
        self.image = image

    def setPartOffset(self, x_offset, y_offset):
        self.offset = [x_offset, y_offset]

    def outputInfo(self):
        logger.debug(f"Player part info: \n \t {self.offset=} \n \t {self.image=}")




class PossiblePlayerStates:
    RUNNING = "RUNNING"
    WALKING = "WALKING"
    NOT_MOVING = "NOT_MOVING"

class Player:
    PLAYER_HEAD_OFFSET = 0
    PLAYER_BODY_OFFSET = 0

    def __init__(self, pos: tuple[int, int], head_img: pygame.Surface, body_img: pygame.Surface):
        self.playerGroup = pygame.sprite.Group()
        self.movementState = ""
        self.rect = None
        try:
            logger.info(f"class {Player=} initializing....")

            self.playerGroup = Player.generatePlayerGroup(head=head_img, body=body_img, group=self.playerGroup)

            for _part in self.playerGroup:
                _part.outputInfo()

            self.rect = Player.generateRect(player_group = self.playerGroup, pos=pos)
            self.movementState = PossiblePlayerStates.NOT_MOVING
            logger.info(f"class {Player=} initialized.")
        except Exception as e:
            logger.info(f"Failed to initialize class {Player=}.\n Error: {e}")

    def render(self, player_group, screen):
        ##########################################################################
        # ELIMINATE THIS LINE LATER #
        pygame.draw.rect(surface=screen, color=(255, 255, 255), rect=self.rect)
        ##########################################################################

        for _part in player_group:
            screen.blit(_part.image, (self.rect.x + _part.offset[0], self.rect.y + _part.offset[1]))

    @staticmethod
    def generateRect(player_group : pygame.sprite.Group, pos : tuple[int, int]) -> pygame.rect.Rect:
        sumWidths = 0
        sumHeights = 0
        for _part in player_group:
            sumWidths = _part.image.get_width()
            sumHeights += _part.image.get_height()
        rect = pygame.Rect(pos[0], pos[1], sumWidths, sumHeights)

        return rect

    @staticmethod
    def generatePlayerGroup(head: pygame.Surface, body: pygame.Surface,
                            group: pygame.sprite.Group) -> pygame.sprite.Group:
        partList = []

        partHead = PlayerPart(image=head, group=group)
        partHead.setPartOffset(x_offset= - int(body.get_width() - head.get_width()), y_offset = 0)
        partBody = PlayerPart(image=body, group=group)
        partBody.setPartOffset(x_offset= 0, y_offset= head.get_width())
        return group

    def handleInput(self):
        keys = pygame.key.get_pressed()
        self.handleWalkingInput(keys)

    def handleWalkingInput(self, keys):
        diagonalStep = 2
        nonDiagonalStep = 3
        noStep = 0

        if keys[SAVED_DATA.PLAYER_RUN_KEY_ID]:
            self.movementState = PossiblePlayerStates.RUNNING
            diagonalStep *= 2
            nonDiagonalStep *= 2

        if keys[SAVED_DATA.PLAYER_WALK_RIGHT_KEY_ID]:
            if keys[SAVED_DATA.PLAYER_WALK_DOWN_KEY_ID]:
                self.movePlayer(diagonalStep, diagonalStep)
            elif keys[SAVED_DATA.PLAYER_WALK_UP_KEY_ID]:
                self.movePlayer(diagonalStep, -diagonalStep)
            else:
                self.movePlayer(nonDiagonalStep, noStep)
        elif keys[SAVED_DATA.PLAYER_WALK_LEFT_KEY_ID]:
            if keys[SAVED_DATA.PLAYER_WALK_DOWN_KEY_ID]:
                self.movePlayer(-diagonalStep, diagonalStep)
            elif keys[SAVED_DATA.PLAYER_WALK_UP_KEY_ID]:
                self.movePlayer(-diagonalStep, -diagonalStep)
            else:
                self.movePlayer(-nonDiagonalStep, noStep)
        elif keys[SAVED_DATA.PLAYER_WALK_UP_KEY_ID]:
            self.movePlayer(noStep, -nonDiagonalStep)
        elif keys[SAVED_DATA.PLAYER_WALK_DOWN_KEY_ID]:
            self.movePlayer(noStep, nonDiagonalStep)
        else:
            self.movementState = PossiblePlayerStates.NOT_MOVING

    def movePlayer(self, step_x: int, step_y:int):
        logger.debug(f"Moving Player group. Walkspeed: ({step_x=}, {step_y=}")
        self.setPlayerPos(self.rect.x + step_x, self.rect.y + step_y)

    def setPlayerPos(self, pos_x : float, pos_y : float):
        self.rect.x = pos_x
        self.rect.y = pos_y

    def update(self, screen):
        self.render(player_group=self.playerGroup, screen=screen)
        try:
            self.handleInput()
        except Exception as e:
            logger.errorg(f"Could not handle player input. Error: {e}")
