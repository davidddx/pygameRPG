import pygame
from debug.logger import logger
import globalVars.SettingsConstants as globalVars
import gamedata.Save.SavedData as SAVED_DATA

class PlayerPart(pygame.sprite.Sprite):
    # WalkAnimSprites = PlayerPart.loadWalkAnimSprites()
    currentAnimationIndex = 0
    eyes = "eyes"
    eyebrows = "eyebrows"
    head = "head"
    pants = "pants"
    shirt = "shirt"
    shoes = "shoes"
    arms = "arms"
    hair = "hair"
    def __init__(self,image: pygame.Surface, group: pygame.sprite.Group, name: str):
        super().__init__(group)
        self.name = name
        self.image = image
    
    def writeOutput(self):
        logger.debug(f"Player part info: \n \t {self.name=} \n \t {self.image=} ")
    def writeOutputPrint(self):
        print(f"Player part info: \n \t {self.name=} \n \t {self.image=} ")


    @staticmethod 
    def loadWalkAnimSprites(animation_path):
        pass 

class PossiblePlayerMovementStates:
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
    FACING_FRONT_ID = 0
    FACING_FRONT_RIGHT_ID = 1
    FACING_SIDE_RIGHT_ID = 2
    FACING_BACK_RIGHT_ID = 3
    FACING_BACK_ID = 4
    FACING_BACK_LEFT_ID = 5
    FACING_SIDE_LEFT_ID = 6
    FACING_FRONT_LEFT_ID = 7

    def __init__(self, pos: tuple[int, int], plr_parts_path: dict[str, str],
                 plr_anim_path: str,  
                 plr_sprite_path: str):
        self.playerGroups = Player.loadPlayerTestGroups(sprite_path= plr_sprite_path)
        self.currentPlayerGroupId = 0
        self.writeOutputOfPlayerGroups()
        self.velocity = [1, 1]
        self.movementDirection = [0, 0]
        self.facingDirection = [0, 0]
        self.onCollision = [False, False, False, False]
        self.onCollisionWith = [None, None, None, None]
        self.rect = Player.generateRect(player_groups = self.playerGroups, pos=pos)
        self.rectColor = (255,255,255)
        self.movementState = PossiblePlayerMovementStates.NOT_MOVING
        self.movable = False
        logger.info(f"class {Player=} initialized.")

    def writeOutputOfPlayerGroups(self):
        for group in self.playerGroups:
            for part in group:
                part.writeOutputPrint()
    @staticmethod
    def loadPlayerTestGroups(sprite_path: str) -> list[pygame.sprite.Group]:
        playerParts = [
            sprite_path + "/PlrSpriteReferenceFront.png", 
            sprite_path + "/PlrSpriteReferenceFrontRight.png",
            sprite_path + "/PlrSpriteReferenceRightSide.png",
            sprite_path + "/PlrSpriteReferenceBackRight.png", 
            sprite_path + "/PlrSpriteReferenceBack.png", 
            sprite_path + "/PlrSpriteReferenceBackLeft.png", 
            sprite_path + "/PlrSpriteReferenceLeftSide.png", 
            sprite_path + "/PlrSpriteReferenceFrontLeft.png", 
        ]
        playerGroups = []
        for i in range(len(playerParts)):
            playerGroups.append(pygame.sprite.Group())
        for i in range(len(playerParts)):
            name = playerParts[i]
            playerParts[i] = PlayerPart(name = name, image= pygame.image.load(name), group= playerGroups[i])  
        return playerGroups

    def render(self, player_group, screen, camera_offset):
        ##########################################################################
        # ELIMINATE THIS LINE LATER #
        rectToDraw = pygame.Rect(self.rect.x - camera_offset[0],
                                 self.rect.y - camera_offset[1],
                                 self.rect.width,
                                 self.rect.height)
        # pygame.draw.rect(surface=screen, color=self.rectColor, rect=rectToDraw)
        ##########################################################################

        for _part in player_group:
            # logger.debug(f"blitting _part {_part.name=} to position: \n "
            screen.blit(_part.image, (self.rect.x - camera_offset[0],
                                      self.rect.y - camera_offset[1]))

    @staticmethod
    def generateRect(player_groups : pygame.sprite.Group, pos : tuple[int, int]) -> pygame.rect.Rect:
        rectWidth = rectHeight = 0
        for player_group in player_groups:
            for _part in player_group:
                rectWidth = _part.image.get_width()
                rectHeight = _part.image.get_height()
                break
            break;
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
            if movement_state != PossiblePlayerMovementStates.RUNNING:
                movement_state = PossiblePlayerMovementStates.RUNNING
        elif keys[SAVED_DATA.PLAYER_WALK_UP_KEY_ID] or keys[SAVED_DATA.PLAYER_WALK_LEFT_KEY_ID] \
                or keys[SAVED_DATA.PLAYER_WALK_DOWN_KEY_ID] or keys[SAVED_DATA.PLAYER_WALK_RIGHT_KEY_ID]:
            movement_state = PossiblePlayerMovementStates.WALKING
        else:
            movement_state = PossiblePlayerMovementStates.NOT_MOVING

        return movement_state

    def handleInput(self):
        keys = pygame.key.get_pressed()
        self.handleWalkingInput(keys)

    def handleWalkingInput(self, keys):

        self.movementState = Player.checkPlayerMovementState(keys=keys, movement_state= self.movementState)
        # logger.debug(f"{self.movementState=}")

        if keys[SAVED_DATA.PLAYER_WALK_UP_KEY_ID]:
            self.facingDirection[1] = -1 
            self.movementDirection[1] = -1
        elif keys[SAVED_DATA.PLAYER_WALK_DOWN_KEY_ID]:
            self.facingDirection[1] = 1
            self.movementDirection[1] = 1
        else:
            self.movementDirection[1] = 0
            if not self.movementState == PossiblePlayerMovementStates.NOT_MOVING:
                self.facingDirection[1] = 0
        if keys[SAVED_DATA.PLAYER_WALK_RIGHT_KEY_ID]:
            self.facingDirection[0] = 1
            self.movementDirection[0] = 1
        elif keys[SAVED_DATA.PLAYER_WALK_LEFT_KEY_ID]:
            self.facingDirection[0] = -1
            self.movementDirection[0] = -1
        else:
            self.movementDirection[0] = 0
            if not self.movementState == PossiblePlayerMovementStates.NOT_MOVING:
                self.facingDirection[0] = 0
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
        if self.movementState == PossiblePlayerMovementStates.RUNNING:
            step_x *= 2
            step_y *= 2
        self.setPlayerPos(self.rect.x + (step_x * velocity[0]), self.rect.y + (step_y * velocity[1]))

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

    @staticmethod 
    def determinePlayerGroupIdTest(directionFacing: list[int]) -> int:
        match directionFacing:
            case [0,0]:
                return Player.FACING_FRONT_ID
            case [0,1]:
                return Player.FACING_FRONT_ID 
            case [0,-1]:
                return Player.FACING_BACK_ID 
            case [1,0]:
                return Player.FACING_SIDE_RIGHT_ID
            case [1,-1]:
                return Player.FACING_BACK_RIGHT_ID
            case [1,1]:
                return Player.FACING_FRONT_RIGHT_ID 
            case [-1,0]:
                return Player.FACING_SIDE_LEFT_ID
            case [-1,-1]:
                return Player.FACING_BACK_LEFT_ID
            case [-1,1]:
                return Player.FACING_FRONT_LEFT_ID 
            case _:
                return 0

        

    def update(self, screen, camera : tuple[float, float]):
        self.render(player_group=self.playerGroups[self.currentPlayerGroupId], screen=screen, camera_offset=camera)
        try:
            self.handleInput()
            self.movePlayer(direction=self.movementDirection, velocity = self.velocity);
            self.currentPlayerGroupId = Player.determinePlayerGroupIdTest(self.facingDirection)
        except Exception as e:
            logger.error(f"Could not handle player input. Error: {e}")
