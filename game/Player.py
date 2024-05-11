import pygame
from debug.logger import logger
import globalVars.SettingsConstants as globalVars
import gamedata.Save.SavedData as SAVED_DATA


def loadWalkAnimSprites() -> list[pygame.surface]:
    pass


class PlayerPart(pygame.sprite.Sprite):
    WalkAnimSprites = loadWalkAnimSprites()
    currentPartAnimationIndex = 0

    def __init__(self,image: pygame.Surface, group: pygame.sprite.Group, name: str):
        super().__init__(group)
        self.name = name
        self.image = image


    def outputInfo(self):
        logger.debug(f"Player part info: \n \t {self.name=} \n \t {self.image=} ")




class PossiblePlayerStates:
    RUNNING = "RUNNING"
    WALKING = "WALKING"
    NOT_MOVING = "NOT_MOVING"

class PlayerRectCollisionIDs:
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class PlayerRectCollisionTypes:
    DOOR = "Door"
    WALL = "Wall"
    NONE = "None"

class Player:


    def __init__(self, pos: tuple[int, int], plrPartsDict: dict[str, pygame.Surface]):
        self.playerGroup = pygame.sprite.Group()
        self.playerGroup = Player.generatePlayerGroup(parts=plrPartsDict, group=self.playerGroup)
        for _part in self.playerGroup:
            _part.outputInfo()
        self.velocity = [1, 1]
        self.movementDirection = [0, 0]
        self.onCollision = [False, False, False, False]
        self.onCollisionWith = [None, None, None, None]
        self.rect = Player.generateRect(player_group = self.playerGroup, pos=pos)
        self.rectColor = (255,255,255)
        self.movementState = PossiblePlayerStates.NOT_MOVING
        self.movable = False
        logger.info(f"class {Player=} initialized.")

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
            # logger.debug(f"blitting _part {_part.name=} to position: \n "
            screen.blit(_part.image, (self.rect.x - camera_offset[0],
                                      self.rect.y - camera_offset[1]))

    @staticmethod
    def generateRect(player_group : pygame.sprite.Group, pos : tuple[int, int]) -> pygame.rect.Rect:
        rectWidth = rectHeight = 0
        for _part in player_group:
            rectWidth = _part.image.get_width()
            rectHeight = _part.image.get_height()
            break
        rect = pygame.Rect(pos[0], pos[1], rectWidth, rectHeight)

        return rect

    @staticmethod
    def generatePlayerGroup(parts: dict[str, pygame.Surface], group: pygame.sprite.Group) -> pygame.sprite.Group:
        for name in parts:
            PlayerPart(image=parts[name], group=group, name=name)

        return group

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

    def handleInput(self):
        keys = pygame.key.get_pressed()
        self.handleWalkingInput(keys)

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
        if not self.movable: return None
        diagonalStep = 2
        nonDiagonalStep = 3
        if abs(direction[0]) == abs(direction[1]) == 1:
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
        logger.debug(f"setting player rect pos to: {self.rect.x}, {self.rect.y}")
        self.rect.x = pos_x
        self.rect.y = pos_y

    def setPlayerCollisionInfo(self, COLLISION_UP: bool, COLLISION_DOWN: bool, COLLISION_LEFT: bool, COLLISION_RIGHT: bool):
        self.onCollision[PlayerRectCollisionIDs.UP] = COLLISION_UP
        self.onCollision[PlayerRectCollisionIDs.DOWN] = COLLISION_DOWN
        self.onCollision[PlayerRectCollisionIDs.RIGHT] = COLLISION_RIGHT
        self.onCollision[PlayerRectCollisionIDs.LEFT] = COLLISION_LEFT

    def getPlayerCollisionInfo(self):
        return self.onCollision

    def setPlayerMovability(self, value: bool):
        self.movable = value

    def getPlayerPos(self) -> tuple[float, float]:
        return self.rect.x, self.rect.y

    def update(self, screen, camera : tuple[float, float]):
        self.render(player_group=self.playerGroup, screen=screen, camera_offset=camera)
        try:
            self.handleInput()
            self.movePlayer(direction=self.movementDirection, velocity = self.velocity);
        except Exception as e:
            logger.error(f"Could not handle player input. Error: {e}")
