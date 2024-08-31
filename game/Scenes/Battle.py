import pygame
import os
from debug.logger import logger
from game.Scenes.BaseScene import Scene, SceneTypes, SceneStates, SceneAnimations
from game.utils.SceneAnimation import SceneAnimation, AnimationStates
from globalVars.SettingsConstants import DEBUG_MODE 
from game.Enemy import EnemyNames, loadEnemyImage, DirectionNames
from collections import deque
import gamedata.Moves as MOVES

class BattleSceneEntity:
    #prototype class for now will use later
    class states:
        INITIALIZING = "INITIALIZING"
        CHOOSING_MOVE = "CHOOSING_MOVE"
        DOING_MOVE = "DOING_MOVE"
        COMPLETING_TURN = "COMPLETING_TURN" 
        WAITING = "WAITING" #Waiting for other entity to do move


    #position param refer to bottom position of sprite
    #enemy: bool to decifer if unit is enemy or not
    #name: unit name
    #base_sprite: base sprite of entity, sprite when entity is not moving
    def __init__(self, name: str, base_sprite: pygame.Surface, enemy: bool, position: tuple):
        logger.debug(f"Initializing BattleSceneEntity {name=}. ")
        self.state = SceneStates.INITIALIZING
        self.isEnemy = enemy
        self.offense = False if enemy else True
        self.name = name
        self.baseSprite = pygame.transform.scale_by(base_sprite, 1.5)
        self.position = self.bottomToTopleftPos(position, self.baseSprite)
        self.moves = self.loadMoves(name, enemy)
        self.moveAnimations = self.loadMoveAnimations(self.moves)
        self.currentAnimationIdx = 0    
        self.currentSprite = self.baseSprite # points to current sprite 
        logger.debug(f"Initialized BattleSceneEntity {name=}.")


    @staticmethod
    def bottomToTopleftPos(bottom_pos: tuple, base_sprite: pygame.Surface):
        topleftPos = bottom_pos[0] - base_sprite.get_width()/2, bottom_pos[1] - base_sprite.get_height()
        return topleftPos

    def loadMoveAnimations(self, moves: list[str]):
        pass

    def loadPlayerMoves(self) -> list[dict]:
        return [MOVES.PUNCH, MOVES.KICK, MOVES.HEADBUTT]

    def loadMoves(self, entity_name: str, is_enemy: bool) -> list[dict]:
        if not is_enemy:
            return self.loadPlayerMoves()
        match entity_name:
            case EnemyNames.GROUNDER:
                return [MOVES.HEADBUTT]
            case _:
                return [MOVES.PUNCH]


    def checkState(self, state):
        match state:
            case self.states.WAITING:
                pass
            case self.states.CHOOSING_MOVE:
                pass
            case self.states.DOING_MOVE:
                pass
            case self.states.COMPLETING_TURN:
                pass
            case self.states.WAITING:
                self.currentAnimationIdx = 0
                return None

    def render(self, screen: pygame.Surface):
        screen.blit(self.currentSprite, self.position)

    def logInfo(self):
        logger.debug(f"LOGGING ENTITY {self.name=} info")
        logger.debug(f"{self.state=}")
        logger.debug(f"{self.offense=}")
        logger.debug(f"{self.isEnemy=}")
        logger.debug(f"{self.moves=}")

    def update(self, screen):
        self.logInfo()
        self.checkState(self.state) 
        self.render(screen)

class BattleSceneTransitionAnimations:
    def __init__(self, animations: list[SceneAnimation]):

        # using queue to determine current animation
        for animation in animations:

            assert hasattr(SceneAnimations, animation.name) 
        self.currentAnimationIdx = 0
        self.animations = deque(animations)
        self.state = AnimationStates.RUNNING

    def setState(self, state: str):
        assert hasattr(AnimationStates, state)
        self.state = state

    def getCurrentAnimationName(self):
        return self.animations[0].name

    def checkAnimationFinished(self, animation):
        if animation.state != AnimationStates.FINISHED:
            return None
        if len(self.animations)==1:
            self.setState(AnimationStates.FINISHED)
        
        self.animations.popleft()

    def update(self, screen: pygame.Surface, background: pygame.Surface, background2=None):
        logger.debug("UPDATING BATTLE SCREEN TRANSITION ANIMATION")
        logger.debug(f"{self.state=}")
        logger.debug(f"{self.animations=}")
        logger.debug(f"{self.currentAnimationIdx=}")
        self.animations[self.currentAnimationIdx].update(screen, background, background2)
        self.checkAnimationFinished(self.animations[self.currentAnimationIdx])

class Battle(Scene):
    def __init__(self, last_area_frame: pygame.Surface, screen_size: tuple[int, int], enemy_name: str, player_base_surf: pygame.Surface):
        self.setState(SceneStates.INITIALIZING)
        logger.debug("Initializing Battle Scene...")
        self.animations = [SceneAnimation(SceneAnimations.DRAG_IN_WITH_BLACK_HORIZONTAL_LINES, screen_size), SceneAnimation(SceneAnimations.FADE_IN, screen_size)]
        logger.debug(f"{screen_size=}")
        self.animationHandler = BattleSceneTransitionAnimations(self.animations)
        super().__init__(SceneTypes.BATTLE) 
        self.lastAreaFrame = last_area_frame
        self.opacity = 0
        self.background = self.testLoadBattleSurface()
        logger.debug("Battle Scene Initialized")
        self.currentAnimation = SceneAnimations.NONE
        self.setState(SceneStates.ON_ANIMATION)
        playerBottomPos = 249, 420
        enemyBottomPos = screen_size[0] - 249, 420
        self.enemy = self.loadEnemy(enemy_name, enemyBottomPos)
        self.player = self.loadPlayer(player_base_surf, playerBottomPos)
        self.currentEntity = self.player # describes entity turn

    def loadEnemy(self, name: str, bottom_pos) -> BattleSceneEntity:
        enemyImage = loadEnemyImage(name, DirectionNames.LEFT, 0)
        match name:
            case EnemyNames.GROUNDER:
                return BattleSceneEntity(EnemyNames.GROUNDER, enemyImage, True, bottom_pos)
            case _:
                return BattleSceneEntity(EnemyNames.GROUNDER, enemyImage, True, bottom_pos)

    def loadPlayer(self, base_sprite, bottom_pos) -> BattleSceneEntity:
        return BattleSceneEntity("PLAYER", base_sprite, False, bottom_pos)

    def playBattleMusic(self):
        pass

    def testLoadBattleSurface(self): #function is a test function that will be removed later 
        cwd = os.getcwd() 
        battleSurfDirPath = os.path.join(cwd, 'images', 'test', 'Battle', 'Backgrounds')
        testSurfPath = os.path.join(battleSurfDirPath, 'Grass.png')
        return pygame.image.load(testSurfPath)

    def render(self, screen):
        screen.blit(self.background, (0,0))

    def debugExit(self, state):
        if state != SceneStates.RUNNING:
            return None
        keys = pygame.key.get_pressed()
        if keys[pygame.K_f]:
            self.setState(SceneStates.FINISHING)

    def exitScene(self, ptr_next_scene):
        self.setState(SceneStates.FINISHED)
        self.setPtrNextScene(ptr_next_scene)

    def transitionToBattleSurface(self, screen):
        newScreen = pygame.Surface(screen.get_size())
        newScreen.blit(self.background, (0,0))
        newScreen.blit(self.player.baseSprite, self.player.position)
        newScreen.blit(self.enemy.baseSprite, self.enemy.position)
        if self.animationHandler.getCurrentAnimationName() == SceneAnimations.FADE_IN:
            self.animationHandler.update(screen, newScreen)
        else:
            self.animationHandler.update(screen, self.lastAreaFrame)
        

    def checkState(self, state: str, screen: pygame.Surface):
        match state:
            case SceneStates.RUNNING:
                self.render(screen) 
                self.player.update(screen)
                self.enemy.update(screen)
            case SceneStates.ON_ANIMATION:
                self.transitionToBattleSurface(screen)
                if self.animationHandler.state == AnimationStates.FINISHED:
                    self.setState(SceneStates.RUNNING)
            case SceneStates.FINISHING:
                self.exitScene(SceneTypes.AREA)

    def update(self, screen):
        self.checkState(state= self.state, screen= screen)

        if DEBUG_MODE:
            self.debugExit(state= self.state)

    def clear(self):
        pass

