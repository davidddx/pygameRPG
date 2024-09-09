import pygame
import os
from debug.logger import logger
from game.Scenes.BaseScene import Scene, SceneTypes, SceneStates, SceneAnimations
from game.utils.SceneAnimation import SceneAnimation, AnimationStates
from globalVars.SettingsConstants import DEBUG_MODE, TILE_SIZE, NUM_TILES 
from game.Enemy import EnemyNames, loadEnemyImage, DirectionNames
from collections import deque
from game.utils.Button import TextButton
import gamedata.Moves as MOVES
import game.utils.SettingsFunctions as SETTINGS_FUNCTIONS
import game.utils.Misc as Misc 
import gamedata.Save.SavedData as SAVED_DATA

class BackgroundTile(pygame.sprite.Sprite):
    def __init__(self, sprite_group: pygame.sprite.Group, image_dir: str, pos: tuple):
        super().__init__(sprite_group)
        assert len(pos) == 2
        self.image = pygame.image.load(image_dir)
        assert(type(self.image) == pygame.Surface)
        self.pos = pos
        logger.debug(f"{self.image=}, {self.pos=}")
    def render(self, screen):
        assert type(screen) == pygame.Surface
        screen.blit(self.image, self.pos)


class BattleSceneEntity:
    #prototype class for now will use later
    class states:
        INITIALIZING = "INITIALIZING"
        IDLE = "IDLE"
        DOING_MOVE = "DOING_MOVE"
        DEFENDING = "DEFENDING"
        COMPLETING_TURN = "COMPLETING_TURN" 


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
        self.baseSprite = base_sprite 
        position = Misc.bottomToTopleftPos(position, self.baseSprite)
        self.rect = self.baseSprite.get_rect(topleft=position)
        self.moves = self.loadMoves(name, enemy)
        self.moveAnimations = self.loadMoveAnimations(self.moves)
        self.currentAnimationIdx = 0    
        self.currentSprite = self.baseSprite # points to current sprite 
        logger.debug(f"Initialized BattleSceneEntity {name=}.")
        self.state = self.states.IDLE

    def loadMoveAnimations(self, moves: list[str]):
        pass

    def loadPlayerMoves(self) -> list[dict]:
        return [MOVES.PUNCH, MOVES.KICK, MOVES.HEADBUTT]

    def loadMoves(self, entity_name: str, is_enemy: bool) -> list[dict]:
        # Each move is a dict with different attributes, dicts stored in gamedata.Moves
        if not is_enemy:
            return self.loadPlayerMoves()
        match entity_name:
            case EnemyNames.GROUNDER:
                return [MOVES.HEADBUTT]
            case _:
                return [MOVES.PUNCH]

    def checkState(self, state):
        match state:
            case self.states.INITIALIZING:
                return None
            case self.states.DEFENDING:
                pass
            case self.states.DOING_MOVE:
                pass
            case self.states.COMPLETING_TURN:
                pass
            case self.states.IDLE:
                self.currentAnimationIdx = 0
                return None

    def render(self, screen: pygame.Surface):
        screen.blit(self.currentSprite, (self.rect.x, self.rect.y))

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

# loading button positions for player battle scene using a model ellipses and the number of buttons 
# goal: run this operation only once and store it in this file so that less float/double operations are done

def loadButtonPositions():
    buttonPositions = []
    
    modelEllipse = 90, 30 #formatted as such: top radius, side radius
    numButtons = Battle.NUM_BUTTONS
    #approach: use polar coordinates and then convert them back to cartesian to generate x and y positions
    import math
    for i in range(-90, 270, int(360/numButtons)):
        print(f"{i}")
        if i == 0 or i == 180:
            buttonPositions.append((0, modelEllipse[0]))
            continue
        if i == -90 or i == 90:
            buttonPositions.append((0, modelEllipse[1]))
            continue
        angle = math.radians(i) 
        polar = Misc.getPolarCoordinates(angle, modelEllipse[0], modelEllipse[1])
        cartesian = Misc.getCartesianFromPolar(polar, angle)
        buttonPositions.append(cartesian)

    logger.debug(f"{buttonPositions=}")

    return buttonPositions


class Battle(Scene):
    class States:
        PREPARING_TURN = "PREPARING_TURN"
        PLAYER_CHOOSING_MOVE = "PLAYER_CHOOSING_MOVE"
        ANIMATING = "ANIMATING"
        ENEMY_CHOOSING_MOVE = "ENEMY_CHOOSING_MOVE"
        ANIMATING_MOVE = "ANIMATING_MOVE"

    class Backgrounds:
        GRASS = "GRASS"

    class ZoomStates:
        ZOOMING_TO_RECT = "ZOOMING_TO_RECT"
        RESETTING_ZOOM = "RESETTING_ZOOM"
        FINISHED = "FINISHED"
        NOT_MOVING = "NOT_MOVING"

    NUM_BUTTONS = 6

    ButtonPositions = loadButtonPositions()

    def __init__(self, last_area_frame: pygame.Surface, screen_size: tuple[int, int], enemy_name: str, player_base_surf: pygame.Surface):
        self.setState(SceneStates.INITIALIZING)
        self.setBattleState(self.States.PREPARING_TURN)
        self.prevState = self.battleState
        logger.debug("Initializing Battle Scene...")
        self.animations = [SceneAnimation(SceneAnimations.DRAG_IN_WITH_BLACK_HORIZONTAL_LINES, screen_size), SceneAnimation(SceneAnimations.FADE_IN, screen_size)]
        logger.debug(f"{screen_size=}")
        self.animationHandler = BattleSceneTransitionAnimations(self.animations)
        super().__init__(SceneTypes.BATTLE) 
        self.lastAreaFrame = last_area_frame
        self.opacity = 0
        self.backgroundFull = pygame.Surface((screen_size[0] + 6*TILE_SIZE, screen_size[1]))
        self.background = self.loadBattleSurface(Battle.Backgrounds.GRASS)
        self.currentAnimation = SceneAnimations.NONE
        self.setState(SceneStates.ON_ANIMATION)
        playerBottomPos = 350, 420
        enemyBottomPos = screen_size[0] - playerBottomPos[0], playerBottomPos[1] 
        self.enemy = self.loadEnemy(enemy_name, enemyBottomPos)
        self.player = self.loadPlayer(player_base_surf, playerBottomPos)
        self.currentEntity = self.player # describes entity turn
        self.zoomScale = 1
        self.zoomState = "NONE"
        self.playerTurnButtons = self.generatePlayerTurnButtons(playerBottomPos, player_base_surf)
        self.playerTurnButtonIdx = 0
        self.currentButtons = self.playerTurnButtons
        self.currentButtonIdx = self.playerTurnButtonIdx
        self.timeLastInput = 0
        logger.debug("Battle Scene Initialized")

    def generatePlayerTurnButtons(self, player_bottom_pos, player_base_surf) -> list[TextButton]:
        extraSpacing = 20
        bottomPos = player_bottom_pos[0], player_bottom_pos[1] - player_base_surf.get_height() - extraSpacing
        buttonList = []
        button1 = TextButton("ATTACK", "ATTACK", 0, 0, 0, 0, fit_to_text=True, color=(140, 8, 10), font_path=SAVED_DATA.FONT_PATH)
        button1.animateTextWithOutline((255, 0,0))
        buttonList.append(button1)
        button2 = TextButton("WAIT", "WAIT", 0, 0, 0, 0, fit_to_text=True, color=(200, 110, 140), font_path=SAVED_DATA.FONT_PATH)
        button2.animateTextWithOutline((244, 194, 194))
        buttonList.append(button2)
        button3 = TextButton("FLEE", "FLEE", 0, 0, 0, 0, fit_to_text=True, color=(100, 149, 247), font_path=SAVED_DATA.FONT_PATH)
        button3.animateTextWithOutline((173, 216, 230))
        buttonList.append(button3)
        button4 = TextButton("ANALYZE", "ANALYZE", 0, 0, 0, 0, fit_to_text = True, color = (155, 135, 12), font_path = SAVED_DATA.FONT_PATH)
        button4.animateTextWithOutline((255, 234, 20))
        buttonList.append(button4)
        button5 = TextButton("USE ITEM", "USE ITEM", 0, 0, 0, 0, fit_to_text=True, color=(0, 153, 0), font_path=SAVED_DATA.FONT_PATH)
        button5.animateTextWithOutline((102, 255, 0))
        buttonList.append(button5)
        for button in buttonList:
            pos = Misc.bottomToTopleftPos(bottomPos, button.textSurface)
            button.setX(pos[0])
            button.setY(pos[1])
        return buttonList

    def checkInput(self, state: str, battle_state: str):
        if state != SceneStates.RUNNING:
            return None
        if battle_state == Battle.States.PREPARING_TURN or battle_state == Battle.States.ENEMY_CHOOSING_MOVE:
            return None
        keys = pygame.key.get_pressed()
        timenow = pygame.time.get_ticks()
        cooldown = 300
        match battle_state:
            case Battle.States.PLAYER_CHOOSING_MOVE:
                if timenow - self.timeLastInput < cooldown:
                    return None

                for key in SAVED_DATA.UI_MOVE_RIGHT:
                    if not keys[key]:
                        continue
                    # do something
                    self.currentButtonIdx += 1
                    if self.currentButtonIdx >= len(self.currentButtons):
                        self.currentButtonIdx = 0
                    self.timeLastInput = timenow
                for key in SAVED_DATA.UI_MOVE_LEFT:
                    if not keys[key]:
                        continue 
                    self.currentButtonIdx -= 1
                    if self.currentButtonIdx < 0:
                        self.currentButtonIdx = len(self.currentButtons) - 1
                    self.timeLastInput = timenow

    def setBattleState(self, state: str):
        assert SETTINGS_FUNCTIONS.checkVariableInClass(state, Battle.States)
        self.battleState = state

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
    # using this function because for some reason pygame.image.load gives me performance issues
    def loadBattleSurface(self, name: str) -> pygame.sprite.Group:
        spriteGroup = pygame.sprite.Group()
        cwd = os.getcwd()
        battleSurfBackgroundPath = os.path.join(cwd, 'images', 'BattleBackgrounds')
        tiledSurfPath = os.path.join(battleSurfBackgroundPath, 'Tiled')
        tiledSurfDir = os.path.join(tiledSurfPath, name)
        if not os.path.isdir(tiledSurfDir):
            baseSurfPath = os.path.join(battleSurfBackgroundPath, 'Base')
            surfPath = os.path.join(baseSurfPath, f"{name}.png")
            assert os.path.exists(surfPath)
            Misc.tileImage(TILE_SIZE, surfPath, tiledSurfDir)
        directories = os.listdir(tiledSurfDir)  
        directories.sort()
        for dirName in directories:
            if dirName.startswith("__") or dirName.endswith("__"):
                continue
            dirNameInt = int(dirName)
            dirPath = os.path.join(tiledSurfDir, dirName)
            logger.debug(f"{dirName=}, {dirNameInt=}")
            for image in os.listdir(dirPath):
                logger.debug(f"{image[-4:]=}")
                if not image[-4:] == ".png":
                    continue 
                imageNameInt = int(image[:-4])
                logger.debug(f"{(dirNameInt, imageNameInt)=}")
                tile = BackgroundTile(spriteGroup, os.path.join(dirPath, image), (dirNameInt * TILE_SIZE, imageNameInt * TILE_SIZE))
                tile.render(self.backgroundFull)
        logger.debug(f"{spriteGroup=}")
        return spriteGroup
        

    def renderBattleBackgroundTest(self, screen):
        screen.blit(self.backgroundFull, (0,0))

    def renderTiledBattleBackground(self, screen: pygame.Surface, group: pygame.sprite.Group):
        for tile in group:
            tile.render(screen)

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
        newScreen.blit(self.backgroundFull, (0,0))
        newScreen.blit(self.player.baseSprite, (self.player.rect.x, self.player.rect.y))
        newScreen.blit(self.enemy.baseSprite, (self.enemy.rect.x, self.enemy.rect.y))
        if self.animationHandler.getCurrentAnimationName() == SceneAnimations.FADE_IN:
            self.animationHandler.update(screen, newScreen)
        else:
            self.animationHandler.update(screen, self.lastAreaFrame)

    def updateZoomScale(self, step: float, max_zoom_scale=3, min_zoom_scale=-1):
        self.zoomScale+= step
        if step > 0:
            if self.zoomScale >= max_zoom_scale:
                self.zoomScale = max_zoom_scale 
        if step < 0:
            if self.zoomScale <= min_zoom_scale:
                self.zoomScale = min_zoom_scale

    def updateZoomState(self, zoom_state: str):
        logger.debug(f"{zoom_state=}, {self.zoomScale=}")
        if zoom_state == Battle.ZoomStates.ZOOMING_TO_RECT:
            MAX_ZOOM_SCALE = 2
            step = 0.1
            self.updateZoomScale(step, MAX_ZOOM_SCALE)
            if self.zoomScale == MAX_ZOOM_SCALE:

                self.zoomState = Battle.ZoomStates.NOT_MOVING
        elif zoom_state == Battle.ZoomStates.RESETTING_ZOOM:
            MIN_ZOOM_SCALE = 1
            step = -0.1
            self.updateZoomScale(step, 0, MIN_ZOOM_SCALE)
            if self.zoomScale == MIN_ZOOM_SCALE:
                self.zoomState = Battle.ZoomStates.NOT_MOVING

    def checkBattleState(self, screen: pygame.Surface, battle_state: str):
        logger.debug(f"{battle_state=}, {self.prevState=}, {self.state=}")
        match battle_state:
            case self.States.PLAYER_CHOOSING_MOVE:
                if self.prevState == Battle.States.PREPARING_TURN:
                    self.zoomState = Battle.ZoomStates.ZOOMING_TO_RECT
                    self.prevState = self.state
                self.updateZoomState(self.zoomState)
                blittedSurface = pygame.Surface(screen.get_size())
                blittedSurface.blit(self.backgroundFull, (0,0))
                self.player.update(blittedSurface)
                self.updateButtons(battle_state, self.currentButtons, self.currentButtonIdx, blittedSurface)
                self.enemy.update(blittedSurface)
                #SETTINGS_FUNCTIONS.zoomToSurface(screen, blittedSurface, self.player.rect, self.zoomScale, self.zoomScale - 1)
                position2 = (blittedSurface.get_width()/2 - self.player.rect.center[0], blittedSurface.get_height()/2 - self.player.rect.center[1])
                SETTINGS_FUNCTIONS.zoomToPosition(screen, blittedSurface, (0,0), position2, self.zoomScale, self.zoomScale-1)
    def updateButtons(self, battle_state, current_buttons, current_button_idx, screen):
        assert battle_state == self.States.PLAYER_CHOOSING_MOVE
        logger.debug(f"{current_buttons=}")
        logger.debug(f"{current_button_idx=}")
        current_buttons[current_button_idx].update(screen)


    def checkState(self, state: str, screen: pygame.Surface):
        match state:
            case SceneStates.RUNNING:
                self.checkBattleState(screen, self.battleState)
            case SceneStates.ON_ANIMATION:
                self.transitionToBattleSurface(screen)
                if self.animationHandler.state == AnimationStates.FINISHED:
                    self.setState(SceneStates.RUNNING)
                    self.setBattleState(Battle.States.PLAYER_CHOOSING_MOVE)
            case SceneStates.FINISHING:
                self.background.empty()
                self.exitScene(SceneTypes.AREA)

    def update(self, screen):
        self.checkState(state= self.state, screen= screen)
        self.checkInput(self.state, self.battleState)

        if DEBUG_MODE:
            self.debugExit(state= self.state)

    def clear(self):
        pass

