import pygame
import math
import os
from game.Tile import Tile, TileTypes
from debug.logger import logger
from globalVars.SettingsConstants import TILE_SIZE

class EnemyNames:
    GROUNDER = 'GROUNDER'

def loadEnemyImage(name: str, direction: str, frame: int, battle=False) -> pygame.Surface: #adding battle stuff later
    baseDir = os.path.join(os.getcwd(), 'images', 'test', 'Enemy', name, direction, f"{str(frame)}.png")
    return pygame.image.load(baseDir)


class DirectionNames:
    FRONT = "Front"
    FRONT_RIGHT = "Front Right"
    RIGHT = "Right"
    BACK_RIGHT = "Back Right"
    BACK = "Back"
    BACK_LEFT = "Back Left"
    LEFT = "Left"
    FRONT_LEFT = "Front Left"

class DirectionIndices:
    FRONT = 0
    FRONT_RIGHT = 1
    RIGHT = 2
    BACK_RIGHT = 3
    BACK = 4
    BACK_LEFT = 5
    LEFT = 6
    FRONT_LEFT = 7

class Enemy(Tile):
    '''Format:
    pos is enemy npc position
    surfs is in followed format:
    imageOnCurrentFrame = surfs[direction_index][walk_anim_index]
    collision bool determines if enemy can go thru walls or not
    '''
    
    def __init__(self, name: str, pos: tuple[int, int], surfs: list[list[pygame.Surface]], collision=True):
        super().__init__(pos=pos, collidable= True, image= surfs[0][0], _type = TileTypes.ENEMY)
        self.name = name
        self.speed = Enemy.getSpeed(name)
        self.detectionRadius = Enemy.getDetectionRadius(name)
        self.movementDirection = [0, 0]
        self.facingDirection = [0,0]
        self.lastFacingDirection = [self.facingDirection[0], self.facingDirection[1]]
        self.surfIndex = [0,0]
        self.surfaces = surfs
        self.rect = surfs[0][0].get_rect(topleft=pos)
        self.hasCollision = collision
        self.locked = False
        self.timeLastLocked = 0
        self.lockCooldown = 500

    def lock(self, milliseconds=500):
        self.locked = True
        self.timeLastLocked = pygame.time.get_ticks()
        self.lockCooldown = milliseconds

    def unlock(self):
        self.locked = False

    def updateLock(self, lock_cooldown, time_last_locked):
        if not self.locked:
            return None
        timenow = pygame.time.get_ticks()
        logger.debug(f"{time_last_locked=}")
        if timenow - time_last_locked < lock_cooldown:
            return None
        self.locked = False 

    @staticmethod
    def getSpeed(name):
        match name:
            case EnemyNames.GROUNDER:
                return 5
            case _:
                return 1

    @staticmethod
    def getDetectionRadius(name):
        match name:
            case EnemyNames.GROUNDER: return 6 * TILE_SIZE
            case _: return 5


    @staticmethod
    def convertSurfDictToList(_dict):
        assert len(_dict.keys()) == 8
        myList = [None, None, None, None, None, None, None, None]
        myList[DirectionIndices.FRONT] = _dict[DirectionNames.FRONT]
        myList[DirectionIndices.FRONT_RIGHT] = _dict[DirectionNames.FRONT_RIGHT]
        myList[DirectionIndices.RIGHT] = _dict[DirectionNames.RIGHT]
        myList[DirectionIndices.BACK_RIGHT] = _dict[DirectionNames.BACK_RIGHT]
        myList[DirectionIndices.BACK] = _dict[DirectionNames.BACK]
        myList[DirectionIndices.BACK_LEFT] = _dict[DirectionNames.BACK_LEFT]
        myList[DirectionIndices.LEFT] = _dict[DirectionNames.LEFT]
        myList[DirectionIndices.FRONT_LEFT] = _dict[DirectionNames.FRONT_LEFT]
        return myList 
        
    @staticmethod
    def getValidEnemyNames():
        return [attr for attr in dir(EnemyNames) if not attr.startswith('__')] 

    @staticmethod
    def getSurfsByName(name):
        enemySpriteDir = os.path.join(os.getcwd(), "images", "test", "Enemy", name)
        if not os.path.exists(enemySpriteDir):
            name = EnemyNames.GROUNDER
            enemySpriteDir = os.path.join(os.getcwd(), "images", "test", "Enemy", name)
            logger.error(f"Could not get Surf by Name for enemy {name=}, dir {enemySpriteDir} does not exist.")
        if not os.path.isdir(enemySpriteDir):
            name = EnemyNames.GROUNDER
            enemySpriteDir = os.path.join(os.getcwd(), "images", "test", "Enemy", name)
            logger.error(f"Could not get Surf by Name for enemy {name=}, dir {enemySpriteDir} is not a directory.")
        
        surfDict = {}
        validImageNames = ["0.png", "1.png", "2.png", "3.png"]
        for directory in os.listdir(enemySpriteDir):
            newDir = os.path.join(enemySpriteDir, directory)
            logger.debug(f"{directory=}")
            if not os.path.isdir(newDir):
                continue
            myList = []
            surfDict[directory] = myList
            for walkAnimationFrame in os.listdir(newDir):
                myList.append(walkAnimationFrame)
            myList.sort()
            for index, imagePath in enumerate(myList):
                logger.debug(f"{imagePath=}")
                if imagePath not in validImageNames:
                    continue
                myList[index] = pygame.image.load(os.path.join(newDir, imagePath))

        return surfDict
    def render(self, surf: pygame.Surface, screen: pygame.Surface, camera_offset, player_pos):
        if not self.checkInRange(player_pos, (self.rect.x, self.rect.y), screen.get_size()): return None
        screen.blit(surf, (self.rect.x - camera_offset[0], self.rect.y - camera_offset[1]))

    def checkDetectionRadius(self, pos: tuple[int, int], player_pos: tuple[int, int], player_size):
        playerEnemyDistance = (pos[0] + self.rect.width/2) - (player_pos[0] + player_size[0]/2), (pos[1] + self.rect.height/2) - (player_pos[1] + player_size[1]/2) 
        #playerEnemyDistance = pos[0] - player_pos[0], pos[1] - player_pos[1] 
        pythagDistance = math.sqrt(playerEnemyDistance[0]**2 + playerEnemyDistance[1]**2)

        logger.debug(f"{playerEnemyDistance=}")
        logger.debug(f"{pythagDistance=}")
        logger.debug(f"{self.detectionRadius=}")
        if pythagDistance > self.detectionRadius:
            self.movementDirection = [0,0]
            return None
            
        toleranceFactor = 20

        if playerEnemyDistance[0] > toleranceFactor:
            self.movementDirection[0] = -1
        elif playerEnemyDistance[0] < -toleranceFactor: self.movementDirection[0] = 1
        else: self.movementDirection[0] = 0
            
        if playerEnemyDistance[1] > toleranceFactor: self.movementDirection[1] = -1
        elif playerEnemyDistance[1] < -toleranceFactor: self.movementDirection[1] = 1
        else: self.movementDirection[1] = 0

        self.facingDirection = [self.movementDirection[0], self.movementDirection[1]]

    def move(self, movement_direction: list[int]):
        diagonalFactor = 1
        if 0 not in movement_direction: 
            diagonalFactor = 0.6
        self.rect.x += movement_direction[0] * self.speed * diagonalFactor 
        self.rect.y += movement_direction[1] * self.speed * diagonalFactor 

    def updateSurfIndex(self, facing_direction: list[int]):
        logger.debug(f"{facing_direction=}")
        if facing_direction == [0, 0]: return None
        match facing_direction:
            case [0, 1]:
                self.surfIndex[0] = DirectionIndices.FRONT
            case [0, -1]:
                self.surfIndex[0] = DirectionIndices.BACK
            case [1, 1]: self.surfIndex[0] = DirectionIndices.FRONT_RIGHT
            case [1,0]: self.surfIndex[0] = DirectionIndices.RIGHT
            case [1, -1]: self.surfIndex[0] = DirectionIndices.BACK_RIGHT
            case [-1,1]: self.surfIndex[0] = DirectionIndices.FRONT_LEFT
            case [-1, 0]: self.surfIndex[0] = DirectionIndices.LEFT 
            case [-1, -1]: self.surfIndex[0] = DirectionIndices.BACK_LEFT

    def checkInRange(self, player_pos, pos, screen_size):
        if abs(player_pos[0] - pos[0]) > screen_size[0]/2: return False
        if abs(player_pos[1] - pos[1]) > screen_size[1]/2: return False
        return True

    def update(self, screen, camera, player_pos, player_size):
        #logger.debug(f"{self.surfIndex[0]=}, {self.surfIndex[1]=}")
        self.render(surf=self.surfaces[self.surfIndex[0]][self.surfIndex[1]], screen=screen, camera_offset=camera, player_pos=player_pos)
        logger.debug(f"{self.locked=}")
        if self.locked: 
            self.updateLock(self.timeLastLocked, self.lockCooldown)
            return None
        self.checkDetectionRadius(pos= (self.rect.x, self.rect.y), player_pos=player_pos, player_size = player_size) 
        self.move(self.movementDirection) 
        self.updateSurfIndex(self.facingDirection)
