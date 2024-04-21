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
        self.onCollision = False
        self.rect = None
        self.rectColor = (255,255,255)
        self.velocity = []  # format: [xVelocity, yVelocity]
        self.movementDirection = [] # format: same as above.
        try:
            logger.info(f"class {Player=} initializing....")

            self.playerGroup = Player.generatePlayerGroup(head=head_img, body=body_img, group=self.playerGroup)

            for _part in self.playerGroup:
                _part.outputInfo()
            self.velocity = [1, 1]
            self.movementDirection = [0, 0]
            self.rect = Player.generateRect(player_group = self.playerGroup, pos=pos)
            self.movementState = PossiblePlayerStates.NOT_MOVING
            logger.info(f"class {Player=} initialized.")
        except Exception as e:
            logger.info(f"Failed to initialize class {Player=}.\n Error: {e}")



    def render(self, player_group, screen, camera_offset):
        ##########################################################################
        # ELIMINATE THIS LINE LATER #
        rectToDraw = pygame.Rect(self.rect.x - camera_offset[0],
                                 self.rect.y - camera_offset[1],
                                 self.rect.width,
                                 self.rect.height)
        pygame.draw.rect(surface=screen, color=self.rectColor, rect=rectToDraw)
        ##########################################################################

        for _part in player_group:
            screen.blit(_part.image, (self.rect.x + _part.offset[0] - camera_offset[0],
                                      self.rect.y + _part.offset[1] - camera_offset[1]))

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

    @staticmethod
    def checkPlayerMovementState(keys, movement_state: str) -> str:
        if keys[SAVED_DATA.PLAYER_RUN_KEY_ID]:
            if movement_state != PossiblePlayerStates.RUNNING:
                movement_state = PossiblePlayerStates.RUNNING
        elif keys[SAVED_DATA.PLAYER_WALK_UP_KEY_ID] or keys[SAVED_DATA.PLAYER_WALK_LEFT_KEY_ID] \
                or keys[SAVED_DATA.PLAYER_WALK_DOWN_KEY_ID] or keys[SAVED_DATA.PLAYER_WALK_RIGHT_KEY_ID]:
            movement_state = PossiblePlayerStates.WALKING
        else:
            movement_state = PossiblePlayerStates.NOT_MOVING

        return movement_state

    def handleWalkingInput(self, keys):

        self.movementState = Player.checkPlayerMovementState(keys=keys, movement_state= self.movementState)
        # logger.debug(f"{self.movementState=}")

        if keys[SAVED_DATA.PLAYER_WALK_UP_KEY_ID]:
            self.movementDirection[1] = -1
        elif keys[SAVED_DATA.PLAYER_WALK_DOWN_KEY_ID]:
            self.movementDirection[1] = 1
        else:
            self.movementDirection[1] = 0
        if keys[SAVED_DATA.PLAYER_WALK_RIGHT_KEY_ID]:
            self.movementDirection[0] = 1
        elif keys[SAVED_DATA.PLAYER_WALK_LEFT_KEY_ID]:
            self.movementDirection[0] = -1
        else:
            self.movementDirection[0] = 0

    def movePlayer(self, direction: list, velocity: list):
        # logger.debug(f"Moving Player group. \n Direction: {self.movementDirection=}, \n Velocity: {self.velocity=}")
        step_x, step_y = 0, 0
        diagonalStep = 2
        nonDiagonalStep = 3
        if abs(direction[0]) == abs(direction[1]):
            step_x = direction[0] * diagonalStep
            step_y = direction[1] * diagonalStep
        else:
            step_x = direction[0] * nonDiagonalStep
            step_y = direction[1] * nonDiagonalStep
        if self.movementState == PossiblePlayerStates.RUNNING:
            step_x *= 2
            step_y *= 2
        self.setPlayerPos(self.rect.x + (step_x * self.velocity[0]), self.rect.y + (step_y * self.velocity[1]))

    def setPlayerPos(self, pos_x : float, pos_y : float):
        self.rect.x = pos_x
        self.rect.y = pos_y

    def getPlayerPos(self) -> tuple[float, float]:
        return self.rect.x, self.rect.y

    def update(self, screen, camera : tuple[float, float]):
        self.render(player_group=self.playerGroup, screen=screen, camera_offset=camera)
        try:
            self.handleInput()
            self.movePlayer(direction=self.movementDirection, velocity = self.velocity);
        except Exception as e:
            logger.error(f"Could not handle player input. Error: {e}")
