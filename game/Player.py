import pygame
from debug.logger import logger
import globalVars.SettingsConstants as globalVars
import gamedata.Save.SavedData as SAVED_DATA

class PlayerPart(pygame.sprite.Sprite):
    walkAnimationIndex = 0
    timeLastAnimated = 0
    walkAnimationCooldown = 100 #in milliseconds
    eyes = "eyes"
    eyebrows = "eyebrows"
    head = "head"
    pants = "pants"
    shirt = "shirt"
    shoes = "shoes"
    arms = "arms"
    hair = "hair"
    def __init__(self,group: pygame.sprite.Group, partName: str, direction_id: int, animation_path: str):
        super().__init__(group)
        self.partName = partName
        self.direction_id = direction_id
        self.walkAnimationImages = PlayerPart.loadWalkAnimSpritesTest(animation_path,
                                                                  PlayerPart.translateDirectionID(direction_id))

    @staticmethod
    def translateDirectionID(direction_id: int) -> str:
        match direction_id:
            case 0:
                return "Front"
            case 1:
                return "FrontRight"
            case 2:
                return "Right"
            case 3:
                return "BackRight"
            case 4:
                return "Back"
            case 5:
                return "BackLeft"
            case 6:
                return "Left"
            case 7:
                return "FrontLeft"
            case _:
                return "Front"


    def writeOutput(self):
        logger.debug(f"Player part info: \n \t {self.name=} \n \t {self.image=} ")
    def writeOutputPrint(self):
        print(f"Player part info: \n \t {self.partName=} \n \t {self.direction_id=} \n \t Facing {self.translateDirectionID(self.direction_id)}. ")


    @staticmethod 
    def loadWalkAnimSpritesTest(animation_path: str, direction: str):
        WalkAnimImages = []
        direction = direction + "/"
        WalkAnimImages.append(pygame.image.load(animation_path + "/FullPlayer/" + direction + '0.png')) 
        WalkAnimImages.append(pygame.image.load(animation_path + "/FullPlayer/" + direction + '1.png'))
        WalkAnimImages.append(pygame.image.load(animation_path + "/FullPlayer/" + direction + '2.png')) 
        WalkAnimImages.append(pygame.image.load(animation_path + "/FullPlayer/" + direction + '3.png'))
        return WalkAnimImages

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
        self.playerSprites = Player.loadPlayerTestGroups(sprite_path= plr_sprite_path, animation_path = plr_anim_path)
        self.writeOutputOfPlayerGroups()
        self.currentDirectionalIdx = 0;
        self.velocity = [1, 1]
        self.movementDirection = [0, 0]
        self.facingDirection = [0, 0]
        self.onCollision = [False, False, False, False]
        self.onCollisionWith = [None, None, None, None]
        self.rect = Player.generateRect(player_groups = self.playerSprites, pos=pos)
        self.rectColor = (255,255,255)
        self.movementState = PossiblePlayerMovementStates.NOT_MOVING
        self.movable = False
        logger.info(f"class {Player=} initialized.")

    def writeOutputOfPlayerGroups(self):
        for group in self.playerSprites:
            for part in group:
                pass
                #part.writeOutputPrint()
    @staticmethod
    def loadPlayerTestGroups(sprite_path: str, animation_path: str) -> list[pygame.sprite.Group]:
        playerDirections = [
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
        for i in range(len(playerDirections)):
            playerGroups.append(pygame.sprite.Group())
        for i in range(len(playerDirections)):
            name = playerDirections[i]
            playerDirections[i] = PlayerPart(partName = "FULL", group= playerGroups[i],
                                             animation_path = animation_path, direction_id=i)  
        return playerGroups

    def render(self, player_sprite, screen, camera_offset):
        ##########################################################################
        # ELIMINATE THIS LINE LATER #
        rectToDraw = pygame.Rect(self.rect.x - camera_offset[0],
                                 self.rect.y - camera_offset[1],
                                 self.rect.width,
                                 self.rect.height)
        pygame.draw.rect(surface=screen, color=self.rectColor, rect=rectToDraw)
        ##########################################################################

        for _part in player_sprite:
            # logger.debug(f"blitting _part {_part.name=} to position: \n "
            screen.blit(_part.walkAnimationImages[PlayerPart.walkAnimationIndex], (self.rect.x - camera_offset[0],
                                      self.rect.y - camera_offset[1] - self.rect.height/2))

    def updateAnimation(self):
        if self.movementState == PossiblePlayerMovementStates.NOT_MOVING:
            PlayerPart.walkAnimationIndex = 0
            return None
        timenow = pygame.time.get_ticks()
        if timenow - PlayerPart.timeLastAnimated < PlayerPart.walkAnimationCooldown:
            return None
        PlayerPart.walkAnimationIndex+=1
        PlayerPart.timeLastAnimated = timenow
        if PlayerPart.walkAnimationIndex > 3:
            PlayerPart.walkAnimationIndex = 0
            return None

        


        

    @staticmethod
    def generateRect(player_groups : pygame.sprite.Group, pos : tuple[int, int]) -> pygame.rect.Rect:
        rectWidth = rectHeight = 0
        for player_group in player_groups:
            for _part in player_group:
                rectWidth = _part.walkAnimationImages[0].get_width()
                rectHeight = _part.walkAnimationImages[0].get_height()/2
                break
            break;
        rect = pygame.Rect(pos[0], pos[1], rectWidth, rectHeight)

        return rect


    def updatePlayerMovementState(self, keys):
        if keys[SAVED_DATA.PLAYER_WALK_UP_KEY_ID] or keys[SAVED_DATA.PLAYER_WALK_LEFT_KEY_ID] \
                or keys[SAVED_DATA.PLAYER_WALK_DOWN_KEY_ID] or keys[SAVED_DATA.PLAYER_WALK_RIGHT_KEY_ID]:
            self.movementState = PossiblePlayerMovementStates.WALKING
            if keys[SAVED_DATA.PLAYER_RUN_KEY_ID]:
                self.movementState = PossiblePlayerMovementStates.RUNNING
        else:
            self.movementState = PossiblePlayerMovementStates.NOT_MOVING
       
    def handleInput(self, keys):
        keys = pygame.key.get_pressed()
        self.handleWalkingInput(keys)


    def handleWalkingInput(self, keys):
        # logger.debug(f"{self.movementState=}")
        tmp = [self.facingDirection[0], self.facingDirection[1]] #create copy of list to deal with other cases
        if keys[SAVED_DATA.PLAYER_WALK_UP_KEY_ID]:
            self.facingDirection[1] = -1 
            self.movementDirection[1] = -1
        elif keys[SAVED_DATA.PLAYER_WALK_DOWN_KEY_ID]:
            self.facingDirection[1] = 1
            self.movementDirection[1] = 1
        else:
            self.movementDirection[1] = 0
            self.facingDirection[1] = 0
        if keys[SAVED_DATA.PLAYER_WALK_RIGHT_KEY_ID]:
            self.facingDirection[0] = 1
            self.movementDirection[0] = 1
        elif keys[SAVED_DATA.PLAYER_WALK_LEFT_KEY_ID]:
            self.facingDirection[0] = -1
            self.movementDirection[0] = -1
        else:
            self.movementDirection[0] = 0
            self.facingDirection[0] = 0

        if self.movementState == PossiblePlayerMovementStates.NOT_MOVING:
            self.facingDirection[0] = tmp[0]
            self.facingDirection[1] = tmp[1]

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

    def getPlayerMovementState(self):
        return self.movementState

    def setPlayerMovability(self, value: bool):
        self.movable = value

    def getPlayerPos(self) -> tuple[float, float]:
        return self.rect.x, self.rect.y

    @staticmethod 
    def determineDirectionalIdx(directionFacing: list[int]) -> int:
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
        # also handles animation in render function
        
        self.render(player_sprite=self.playerSprites[self.currentDirectionalIdx], screen=screen, camera_offset=camera)
        keys = pygame.key.get_pressed()
        self.updatePlayerMovementState(keys)
        self.handleInput(keys)
        self.movePlayer(direction=self.movementDirection, velocity = self.velocity);
        self.currentDirectionalIdx = Player.determineDirectionalIdx(self.facingDirection)
        self.updateAnimation()
