import pygame
import os
import random
from debug.logger import logger
from game.Scenes.BaseScene import Scene, SceneTypes, SceneStates, SceneAnimations
from game.utils.SceneAnimation import SceneAnimation, AnimationStates
from globalVars.SettingsConstants import DEBUG_MODE, TILE_SIZE, NUM_TILES, SCREEN_WIDTH, SCREEN_HEIGHT
from game.Enemy import EnemyNames, loadEnemyImage, DirectionNames
import game.Enemy as Enemy
from game.Player import DirectionNames, PLAYER
from game.utils.Button import TextButton
import game.utils.SettingsFunctions as SETTINGS_FUNCTIONS
import game.utils.Misc as Misc 
import gamedata.Save.SavedData as SAVED_DATA
import gamedata.Moves as MOVES
import gamedata.MoveAnimationLoader as MOVE_ANIMATION_LOADER
import numpy
from collections import deque

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
    class States:
        INITIALIZING = "INITIALIZING"
        IDLE = "IDLE"
        DOING_MOVE = "DOING_MOVE"
        DEFENDING = "DEFENDING"
        COMPLETING_TURN = "COMPLETING_TURN" 
        NONE = "NONE"

    #class that describes possible values for self.movestate variable
    class MoveStates:
        IDLE = "IDLE"
        INITIALIZING = "INITIALIZING"
        MOVING = "MOVING"
        ATTACKING = "ATTACKING"
        RETURNING = "RETURNING"
        DONE = "DONE"

    #position param refer to bottom position of sprite
    #enemy: bool to decifer if unit is enemy or not
    #name: unit name
    #base_sprite: base sprite of entity, sprite when entity is not moving
    ## GROUPS:
    # each group has a minimal part which holds image and name data
    # idle group is sprite group list of entity being idle
    # walk animation is sprite group list of entity walking
    # move animation is sprite group list of entity doing move
    # current group points to the current group based on state n other logic that i have and/or will implement
    def __init__(self, name: str, enemy: bool, position: tuple):
        logger.debug(f"Initializing BattleSceneEntity {name=}. ")
        self.state = self.States.NONE
        self.prevState = self.States.NONE
        self.setState(self.States.INITIALIZING)
        self.setMoveState(self.MoveStates.IDLE)
        self.isEnemy = enemy
        self.offense = False if enemy else True # player turn is always first, will probably change this to do a comparison off of speed
        self.name = name
        self.moves = self.loadMoves(name, enemy)
        self.currentGroupIdx = 0 # max group index is len(groups) - 1
        # denotes animation frame.
        self.idleGroup = BattleSceneEntity.loadIdleSprites(name = name, enemy = enemy)
        self.walkAnimation = self.loadWalkAnimation(name = self.name)
        self.moveAnimations = self.loadMoveAnimations(moves = self.moves)
        self.walkBackAnimation = self.loadWalkBackAnimation(name = self.name)
        self.currentMoveAnimation = None 
        self.currentGroups = self.idleGroup # points to the current sprite group 
        ##
        baseSprite = self.getBaseSpriteSurface(self.idleGroup)
        position = Misc.bottomToTopleftPos(position, baseSprite) # Turns position to topleft appropriately
        self.originalPosition = position
        self.rect = baseSprite.get_rect(topleft=position)
        self.selectedMove = MOVES.NONE 
        self.selectedTargetPos = (0, 0) # When target selected this gets set
        logger.debug(f"Initialized BattleSceneEntity {name=}.")
        self.setState(self.States.IDLE)
        logger.debug(f"WALK ANIM: \n{self.walkAnimation=}")
        self.timeLastAnimFreeze = 0

    def getMoves(self):
        return self.moves;

    def setSelectedTargetPos(self, x, y):
        assert (type(x) == int or type(x) == float) and (type(y) == int or type(y) == float)
        self.selectedTargetPos = x, y # selected target pos as tuple of format (coordinateX, coordinateY)

    @staticmethod
    def loadIdleSprites(name: str, enemy: bool):
        sprites = []
        frameNumber = 0
        if enemy:
            # logic of loading enemy sprites
            match name:
                case EnemyNames.GROUNDER:

                    group = Enemy.loadEnemyImageAsSpriteGroup(name, DirectionNames.LEFT, frameNumber)
                    sprites.append(group)
                    pass
                case _:
                    raise Exception(f"Error in game/Scenes/Battle.py function BattleSceneEntity.loadSprites: invalid enemy name: {name=}") 
            return sprites 
        if name == PLAYER:
            # logic of loading player sprites
            myGroup = Misc.loadIdleAnimByDirection(direction= DirectionNames.RIGHT)
            # is a list b/c want to add idle anim later.
            logger.debug(f"{myGroup=}")
            sprites.append(myGroup)
            return sprites 
        
        raise Exception(f"Error in game/Scenes/Battle.py function BattleSceneEntity.loadSprites: Invalid entity name: {name=}") 
        # invalid name case.

    def getBaseSpriteSurface(self, groups: list) -> pygame.Surface:
        logger.debug(f"{groups=}")
        for group in groups:
            assert type(group) == pygame.sprite.Group
            for part in group:
                # All images in a entity sprite group should have the same size.
                assert part.image != None
                return part.image

        raise Exception("Error in game/Scenes/Battle.py function getBaseSpriteSurface: could not return a image; no images found") 

    def setState(self, state: str):
        assert hasattr(BattleSceneEntity.States, state)
        self.prevState = self.state
        self.state = state

    def getPrevState(self):
        return self.prevState

    def getState(self):
        return self.state

    def setMoveState(self, state: str):
        assert hasattr(BattleSceneEntity.MoveStates, state)
        self.moveState = state

    def loadMoveAnimations(self, moves: dict) -> dict:
        
        '''
        Move Animations have the followin format
        moveAnimationDict = {
            plrMoveName0 : list with n0 frames of this move composed of spritegroups of parts 
            plrMoveName1 : list with n1 frames of this move composed of spritegroups of parts 
            ...
            ...
        }
    
        '''
        logger.debug(f"{moves=}")
        myDict = {}
        for moveDict in moves.values():
            logger.debug(f"{moveDict=}")
            moveName = moveDict[MOVES.NAME]
            myDict[moveName] = MOVE_ANIMATION_LOADER.loadMoveAnim(moveName, self.isEnemy)
        return myDict

    ##test function, will modify later
    def loadPlayerMoves(self) -> dict:
        moveDict = {
            MOVES.PUNCH[MOVES.NAME]: MOVES.PUNCH,
            MOVES.KICK[MOVES.NAME] : MOVES.KICK,
            MOVES.HEADBUTT[MOVES.NAME] : MOVES.HEADBUTT
        }
        return moveDict

    def loadWalkAnimation(self, name: str):
        if not self.isEnemy:
            return Misc.loadWalkAnimByDirection(DirectionNames.RIGHT)
        return Enemy.loadEnemyWalkAnimAsSpriteGroupList(name, DirectionNames.LEFT)

    # walk anim when u walkin back from a attack to ur original position
    def loadWalkBackAnimation(self, name: str):
        if not self.isEnemy:
            return Misc.loadWalkAnimByDirection(DirectionNames.LEFT)
        return Enemy.loadEnemyWalkAnimAsSpriteGroupList(name, DirectionNames.RIGHT)

    ##will modify later
    def loadMoves(self, entity_name: str, is_enemy: bool) -> dict:
        # Each move is a dict with different attributes, dicts stored in gamedata.Moves
        if not is_enemy:
            return self.loadPlayerMoves()
        match entity_name:
            case EnemyNames.GROUNDER:
                return {MOVES.HEADBUTT[MOVES.NAME] : MOVES.HEADBUTT}
            case _:
                return {MOVES.PUNCH[MOVES.NAME] : MOVES.PUNCH} 

    def setSelectedMove(self, move_name: str):
        selectedMove = None
        for move in self.moves.values():
            if move[MOVES.NAME] != move_name:
                continue
            selectedMove = move
            break
        assert selectedMove is not None
        self.selectedMove = selectedMove

    def checkWindUp(self):
        if self.moveState != self.MoveStates.ATTACKING:
            return None
        move = self.selectedMove
        animData = MOVES.ANIMATION_DATA[move[MOVES.NAME]]
        if self.currentGroupIdx == animData[MOVES.WIND_UP_FRAME_IDX]:
            return True
        return False
    
    def checkPostWindUp(self):
        if self.moveState != self.MoveStates.ATTACKING:
            return None
        move = self.selectedMove
        animData = MOVES.ANIMATION_DATA[move[MOVES.NAME]]
        # The + 1 are for edge cases that occur and make bar flicker because i use floats to control anim speed 
        # sometimes self.currentGroupIdx will be = to targetValue + 0.2 or 0.3 or whatever which messes up this function so i need that strict  bounds because of how i handle all this
        if self.currentGroupIdx >= animData[MOVES.WIND_UP_FRAME_IDX] + 1 and self.currentGroupIdx <= animData[MOVES.FULL_EXTENSION_FRAME_IDX] + 1:
            return True
        return False
    
    def checkMoveState(self, state, move):
        assert self.state == self.States.DOING_MOVE
        if state == self.MoveStates.IDLE:
            self.setMoveState(self.MoveStates.MOVING)
            self.currentGroups = self.walkAnimation
            logger.debug(f"{self.walkAnimation=}");
            logger.debug(f"{self.currentGroups=}");

            return None 
        if state == self.MoveStates.MOVING:
            # might add a goalY later.
            goalX = self.selectedTargetPos[0] - self.rect.width
            if self.isEnemy:
                goalX = self.selectedTargetPos[0];
                # this is for width position fix stuff.
            xOffset = 5
            yOffset = 0
            walkAnimStep = 0.3
            self.moveEntity(xOffset, yOffset)
            self.currentGroupIdx += walkAnimStep
            # version for player.
            if not self.isEnemy:
                if self.currentGroupIdx >= len(self.currentGroups):
                    # making sure the animation is circular and goes from frame 1-2-...n -> 1-2-...n
                    # works b/c int(x) on float x will truncate decimal
                    self.currentGroupIdx -= len(self.currentGroups)
                if self.rect.x > goalX:
                    self.rect.x = goalX 

                if self.rect.x == goalX:
                    if (int(self.currentGroupIdx) != 0) and (int(self.currentGroupIdx) != 2):
                        # making sure the walk anim finishes for smooth transition. 
                        return None
                    self.setMoveState(self.MoveStates.ATTACKING)
                return None
            #enemy case starts here.

            if self.currentGroupIdx >= len(self.currentGroups):
                self.currentGroupIdx -= len(self.currentGroups)
            if self.rect.x < goalX:
                self.rect.x = goalX 

            if self.rect.x == goalX:
                if (int(self.currentGroupIdx) != 0) and (int(self.currentGroupIdx) != 2):
                    # making sure the walk anim finishes for smooth transition. 
                    return None
                self.setMoveState(self.MoveStates.ATTACKING)
            return None

            #enemy case ends.
        if state == self.MoveStates.ATTACKING:
            sGroup = self.moveAnimations[self.selectedMove[MOVES.NAME]]
            if not self.currentGroups == sGroup:
                self.currentGroups = sGroup
                logger.debug(f"{sGroup=}")
                self.currentGroupIdx = 0
                return None
            
            animData = MOVES.ANIMATION_DATA[move[MOVES.NAME]]
            timenow = pygame.time.get_ticks()
            logger.debug(f"{self.timeLastAnimFreeze=}, {timenow=}")
            atkAnimStep = 0.4


            # WIND UP FRAME FIRST REACHED.
            if int(self.currentGroupIdx) == animData[MOVES.WIND_UP_FRAME_IDX] and self.timeLastAnimFreeze == 0: 
                self.currentGroupIdx = animData[MOVES.WIND_UP_FRAME_IDX]
                return None

            # WINDING UP TILL COOLDOWN ENDS
            if self.checkWindUp():
            #if self.currentGroupIdx == animData[MOVES.WIND_UP_FRAME_IDX]:
#                if timenow - self.timeLastAnimFreeze >= windUpFreezeTime:
#                    self.currentGroupIdx = animData[MOVES.WIND_UP_FRAME_IDX] + 1 # move on to next idx 
#                    self.timeLastAnimFreeze = 0
                return None

            # FULL EXTENSION FIRST REACHED.
            fullExtensionFreezeTime = 300
            if int(self.currentGroupIdx) == animData[MOVES.FULL_EXTENSION_FRAME_IDX] and self.timeLastAnimFreeze == 0:
                self.timeLastAnimFreeze = timenow
                self.currentGroupIdx = animData[MOVES.FULL_EXTENSION_FRAME_IDX]
                return None
            if self.currentGroupIdx == animData[MOVES.FULL_EXTENSION_FRAME_IDX]:
                if timenow - self.timeLastAnimFreeze >= fullExtensionFreezeTime:
                    self.currentGroupIdx = animData[MOVES.FULL_EXTENSION_FRAME_IDX] + 1
                    self.timeLastAnimFreeze = 0
                return None
                
            self.currentGroupIdx += atkAnimStep

            # ANIM FINISHED:
            if int(self.currentGroupIdx) == animData[MOVES.FRAME_SIZE_IDX]:
                self.setMoveState(self.MoveStates.RETURNING)
                self.currentGroupIdx = 0
                self.currentGroups = self.walkBackAnimation
                return None 

            return None
        if state == self.MoveStates.RETURNING:
            goalX = self.originalPosition[0]
            xOffset = -5
            yOffset = 0
            walkAnimStep = 0.3
            self.movePlayer(xOffset, yOffset)
            self.currentGroupIdx += walkAnimStep
            if self.currentGroupIdx >= len(self.currentGroups):
                # making sure the animation is circular and goes from frame 1-2-...n -> 1-2-...n
                # works b/c int(x) on float x will truncate decimal
                self.currentGroupIdx -= len(self.currentGroups)
            if self.rect.x < goalX:
                self.rect.x = goalX 

            if self.rect.x == goalX:
                if (int(self.currentGroupIdx) != 0) and (int(self.currentGroupIdx) != 2):
                    return None
                self.setMoveState(self.MoveStates.DONE)
                self.currentGroupIdx = 0
                self.currentGroups = self.idleGroup

            return None

        if state == self.MoveStates.DONE:
            return None

    def checkState(self, state):
        match state:
            case self.States.INITIALIZING:
                return None
            case self.States.DEFENDING:
                pass
            case self.States.DOING_MOVE:
                self.checkMoveState(self.moveState, self.selectedMove)
                pass
            case self.States.COMPLETING_TURN:
                pass
            case self.States.IDLE:
                self.currentGroupIdx = 0

                return None

    def moveEntity(self, x_offset, y_offset):
        if self.isEnemy:
            self.rect.x -= x_offset
            self.rect.y -= y_offset
            return
        self.movePlayer(x_offset, y_offset);

    def movePlayer(self, x_offset, y_offset):
        assert type(x_offset) == float or type(x_offset) == int
        assert type(y_offset) == float or type(y_offset) == int
        self.rect.x += x_offset
        self.rect.y += y_offset

    def render(self, screen: pygame.Surface):
        logger.debug(f"{self.currentGroupIdx=}");
        idx = int(self.currentGroupIdx)
        for minimalPart in self.currentGroups[idx]:
            minimalPart.render(position = (self.rect.x,self.rect.y), screen = screen)
        #screen.blit(self.currentSprite, (self.rect.x, self.rect.y))

    def logInfo(self):
        logger.debug(f"LOGGING ENTITY {self.name=} info")
        logger.debug(f"ENTITY STATE {self.state=}")
        logger.debug(f"ENTITY MOVE STATE {self.moveState=}")
        logger.debug(f"{self.offense=}")
        logger.debug(f"{self.isEnemy=}")
        logger.debug(f"{self.moves=}")
        logger.debug(f"{self.selectedMove=}")
        logger.debug(f"{self.currentGroupIdx=}")
        logger.debug(f"{self.currentGroups=}")
        logger.debug(f"self.currentPos=({self.rect.x}, {self.rect.y})"); 
        logger.debug(f"{self.selectedTargetPos=}")

    def update(self, screen):
        self.logInfo()
        self.checkState(self.state) 
        #self.logInfo()
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
def loadButtonPositions(num_buttons: int, pos=(0,0), model_ellipse = (30, 30)):
    angles = numpy.radians(numpy.array(range(-90, 270, int(360/num_buttons))))
    polarCoordinates = Misc.getPolarCoordinates(angles, model_ellipse[1], model_ellipse[0])
    pos = Misc.getCartesianFromPolar(polarCoordinates, angles) + pos 

    logger.debug(f"button positions: {pos}")
    return pos 

def loadEllipseInterpolatedButtonPositions(num_buttons, ellipse_size, base_angle, num_steps, pos):
    baseArr = numpy.zeros((num_buttons, num_steps + 1, 2)) # 2 at the end because 2d
    '''
    num_buttons: number of buttons, 
    ellipse_size: (ellipse horizontal axis radius, vertical axis radius)
    base_angle: starting angle in degrees
    num_steps: number of interpolation steps taken.
    pos: our offset
    baseArr is a 3d array with the format specified below
    array[0] = 5 positions b/t path from button_positions[0] to button_positions[1]
    array[1] = 5 positions b/t path from button_positions[1] to button_positions[2]
    array[2] = 5 positions b/t path from button_positions[2] to button_positions[3]
    array[3] = 5 positions b/t path from button_positions[3] to button_positions[0]
    
    ##Remember## array[0] pos is for -90 degrees, array[numbuttons - 1] pos is for 270
    '''
    endingAngle = base_angle + 360
    numButtons = num_buttons 
    outerStep = int((endingAngle - base_angle)/numButtons)
    for index1, angleMeasure in enumerate(range(base_angle, endingAngle, outerStep)):
        innerEndingAngle = angleMeasure + outerStep
        innerStep = int(outerStep / num_steps) 
        # range function sets interpolation range from angleMeasure to endingAngle
        theRange = range(angleMeasure, innerEndingAngle + innerStep, innerStep)
        innerArr = numpy.zeros(len(theRange))
        for index2, interpolatedAngle in enumerate(theRange):
            innerArr[index2] = interpolatedAngle
        #logger.debug(f"Loading Ellipse Interpolated Button positions. {innerArr=}")
        innerArr = numpy.radians(innerArr)
        polarCoordinates = Misc.getPolarCoordinates(innerArr, ellipse_size[1], ellipse_size[0])
        baseArr[index1] = Misc.getCartesianFromPolar(polarCoordinates, innerArr) + pos 
    logger.debug(f"{baseArr=}")
    return baseArr

class Battle(Scene):

    class PlayerTurnButtonNames:
        ATTACK = "ATTACK"
        FLEE = "FLEE"
        WAIT = "WAIT"
        USE_ITEM = "USE_ITEM"
        BACK = "BACK"

    class States:
        PREPARING_TURN = "PREPARING_TURN"
        PLAYER_CHOOSING_ACTION = "PLAYER_CHOOSING_ACTION"
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

    class ButtonMenus:
        PLAYER_TURN = "PLAYER_TURN"
        ATK = "ATK"

    NONE = "NONE"
    NUM_BUTTONS = 4 
    PLAYER_BOTTOM_POS = 350, 420
    BUTTON_MODEL_ELLIPSE = (100, 25)
    BUTTON_OFFSET = (PLAYER_BOTTOM_POS[0], PLAYER_BOTTOM_POS[1] - 2*TILE_SIZE - BUTTON_MODEL_ELLIPSE[1])
    ButtonPositions = loadButtonPositions(NUM_BUTTONS, pos=BUTTON_OFFSET, model_ellipse = BUTTON_MODEL_ELLIPSE)
    InterpolatedButtonPositions = loadEllipseInterpolatedButtonPositions(NUM_BUTTONS, BUTTON_MODEL_ELLIPSE, -90, 3, BUTTON_OFFSET)

    def __init__(self, last_area_frame: pygame.Surface, screen_size: tuple[int, int], enemy_name: str, player_base_surf: pygame.Surface):
        # timing rect variables begin
        self.tryNum = 1 
        self.outerRect = pygame.Rect(0, 0, player_base_surf.get_width() + 50, player_base_surf.get_height()/4)
        self.timingRect = pygame.Rect(0, 0, 0, 0)
        self.timingRectColor = (15, 15, 15)
        self.timing = False
        self.timingRectIncreaseRate = 3
        # timing rect variables end
        self.cameraPos = [0, 0]
        self.uiLock = False
        self.uiLockTemp = False
        self.uiLockTimeSet = 0
        self.uiLockCooldown = 0
        self.setState(SceneStates.INITIALIZING)
        self.setBattleState(self.States.PREPARING_TURN)
        self.prevState = self.battleState
        logger.debug("Initializing Battle Scene...")
        self.animations = [SceneAnimation(SceneAnimations.DRAG_IN_WITH_BLACK_HORIZONTAL_LINES, screen_size), SceneAnimation(SceneAnimations.FADE_IN, screen_size)]
        logger.debug(f"{screen_size=}")
        self.animationHandler = BattleSceneTransitionAnimations(self.animations)
        super().__init__(SceneTypes.BATTLE) 
        self.lastAreaFrame = last_area_frame
        self.lastFrame = pygame.Surface(screen_size) 
        self.opacity = 0
        self.backgroundFull = pygame.Surface((screen_size[0] + 6*TILE_SIZE, screen_size[1]))
        self.zoomLerpFactor = 0 # Variable used for zoom lerping
        self.background = self.loadBattleSurface(Battle.Backgrounds.GRASS)
        self.additionalBackgroundSurfs = []
        self.additionalBackgroundSurfsPos = []
        self.cover = [None, None, None, None, None]
        self.coverIdx = 0
        self.coverPos = [(), (), (), (), ()]
        self.currentAnimation = SceneAnimations.NONE
        self.setState(SceneStates.ON_ANIMATION)
        enemyBottomPos = screen_size[0] - Battle.PLAYER_BOTTOM_POS[0], Battle.PLAYER_BOTTOM_POS[1] 
        self.enemy = self.loadEnemy(enemy_name, enemyBottomPos)
        self.player = self.loadPlayer(Battle.PLAYER_BOTTOM_POS)
        self.currentEntity = self.player # describes entity turn
        self.zoomScale = 1
        self.zoomState = Battle.NONE 
        self.buttonPressedName = Battle.NONE 
        self.currentButtons = self.generatePlayerTurnButtons() 
        self.currentButtonIdx = 0 
        self.buttonIndices = self.loadButtonIndices() # Used to save button menu indices
        self.timeLastInput = 0
        self.currentButtonMenu = Battle.ButtonMenus.PLAYER_TURN 
        self.canFlee = self.determinePlayerFlee()
        self.timeAttackFinished = 0;
        logger.debug("Battle Scene Initialized")

    def loadButtonIndices(self) -> dict:
        members = [attr for attr in dir(Battle.ButtonMenus) if not callable(getattr(Battle.ButtonMenus, attr)) and not attr.startswith("__")]
        myDict = {}
        for member in members:
            myDict[member] = 0
        logger.debug(f"BUTTON INDICE DICT: {myDict}")
        return myDict 

    def generatePlayerAttackButtons(self, player_moves: dict, shift_right=0) -> list[TextButton]:
        positions = loadButtonPositions(num_buttons = len(player_moves) + 1, model_ellipse = Battle.BUTTON_MODEL_ELLIPSE, pos= Battle.BUTTON_OFFSET ) # + 1 for back button
        myButtons = []
        mainPos = positions[0]
        buttonColor = (140, 8, 10)
        buttonOutlineColor = (200, 0, 0)
        for move in player_moves.keys():
            logger.debug(f"{player_moves.keys()=}")
            moveName = move
            button = TextButton(moveName, f"{Battle.PlayerTurnButtonNames.ATTACK}.{moveName}", 0, 0, 0, 0, fit_to_text=True, color=buttonColor, font_path=SAVED_DATA.FONT_PATH)
            button.animateTextWithOutline(buttonOutlineColor, size="small")
            button.setTextSurfaceAlpha(0)
            button.setTextSurfaceOutlineAlpha(0)
            myButtons.append(button)
        # adding back button
        backButtonColor = (200, 8, 10)
        backButtonOutlineColor = (255, 0, 0)
        backButton = TextButton("BACK", f"{Battle.PlayerTurnButtonNames.ATTACK}.BACK", 0, 0, 0, 0, fit_to_text=True, color = backButtonColor, font_path=SAVED_DATA.FONT_PATH)
        backButton.animateTextWithOutline(backButtonOutlineColor, size="small")
        backButton.setTextSurfaceAlpha(0)
        backButton.setTextSurfaceOutlineAlpha(0)
        myButtons.append(backButton)
        myButtons = Misc.shiftList(myButtons, shift_right)

        # Button position stuff
        mainPos = Battle.ButtonPositions[0]
        for i in range(len(myButtons)):
            currentButton = myButtons[i]
            adjustedPos = Misc.bottomToTopleftPos(Battle.ButtonPositions[0 - i], myButtons[i].textSurface) 
            currentButton.setX(adjustedPos[0])
            currentButton.setY(adjustedPos[1])
            if i != 0:
                lastSize = currentButton.fontSize
                sizeDiff = int((mainPos[1] - Battle.ButtonPositions[0 - i, 1])/10 + 3)
                currSize = currentButton.originalFontSize - sizeDiff
                currentButton.animateTextToAlpha(100)
                currentButton.animateTextToSize(size= currSize, step= 1, shrink= lastSize > currSize)
                logger.debug(f"{currSize=}")
                logger.debug(f"{sizeDiff=}")
                logger.debug(f"{currentButton.fontSize=}")
            else:
                currentButton.animateTextToAlpha(255)
                currentButton.animateTextToSize(size= currentButton.originalFontSize + 4, step=0.3, shrink= False)
                currentButton.animateTextWithOutline()
                logger.debug(f"{currentButton.fontSize=}")
        myButtons = Misc.shiftList(myButtons, -shift_right)
        self.currentButtonIdx = -shift_right
        return myButtons 

    def generatePlayerTurnButtons(self, shift_right = 0) -> list[TextButton]:
        #extraSpacing = 20
        #bottomPos = player_bottom_pos[0], player_bottom_pos[1] - player_base_surf.get_height() - extraSpacing
        buttonList = []
        button2 = TextButton(Battle.PlayerTurnButtonNames.WAIT, Battle.PlayerTurnButtonNames.WAIT, 0, 0, 0, 0, fit_to_text=True, color=(200, 110, 140), font_path=SAVED_DATA.FONT_PATH)
        button2.animateTextWithOutline((244, 194, 194), size="small")
        buttonList.append(button2)
        button1 = TextButton(Battle.PlayerTurnButtonNames.ATTACK, Battle.PlayerTurnButtonNames.ATTACK, 0, 0, 0, 0, fit_to_text=True, color=(140, 8, 10), font_path=SAVED_DATA.FONT_PATH)
        button1.animateTextWithOutline((255, 0,0), size="small")
        buttonList.append(button1)
        button3 = TextButton(Battle.PlayerTurnButtonNames.FLEE, Battle.PlayerTurnButtonNames.FLEE, 0, 0, 0, 0, fit_to_text=True, color=(100, 149, 247), font_path=SAVED_DATA.FONT_PATH)
        button3.animateTextWithOutline((173, 216, 230), size="small")
        buttonList.append(button3)
        #button4 = TextButton("ANALYZE", "ANALYZE", 0, 0, 0, 0, fit_to_text = True, color = (155, 135, 12), font_path = SAVED_DATA.FONT_PATH)
        #button4.animateTextWithOutline((255, 234, 20))
        #buttonList.append(button4)
        button5 = TextButton(Battle.PlayerTurnButtonNames.USE_ITEM, Battle.PlayerTurnButtonNames.USE_ITEM, 0, 0, 0, 0, fit_to_text=True, color=(0, 153, 0), font_path=SAVED_DATA.FONT_PATH)

        button5.animateTextWithOutline((102, 255, 0), size="small")
        buttonList.append(button5)

        buttonList = Misc.shiftList(buttonList, shift_right)

        mainPos = Battle.ButtonPositions[0]
        for i in range(len(buttonList)):
            currentButton = buttonList[i]
            adjustedPos = Misc.bottomToTopleftPos(Battle.ButtonPositions[0 - i], buttonList[i].textSurface) 
            currentButton.setX(adjustedPos[0])
            currentButton.setY(adjustedPos[1])
            if i != 0:
                lastSize = currentButton.fontSize
                sizeDiff = int((mainPos[1] - Battle.ButtonPositions[0 - i, 1])/10 + 3)
                currSize = currentButton.originalFontSize - sizeDiff
                currentButton.setTextSurfaceAlpha(100)
                currentButton.setTextSurfaceOutlineAlpha(100)
                currentButton.animateTextToSize(size= currSize, step= 1, shrink= lastSize > currSize)
                logger.debug(f"{currSize=}")
                logger.debug(f"{sizeDiff=}")
                logger.debug(f"{currentButton.fontSize=}")
            else:
                currentButton.setTextSurfaceAlpha(255)
                currentButton.setTextSurfaceOutlineAlpha(255)
                currentButton.animateTextToSize(size= currentButton.originalFontSize + 4, step=0.3, shrink= False)
                currentButton.animateTextWithOutline()
                logger.debug(f"{currentButton.fontSize=}")
            logger.debug(f"{buttonList[i].textSurfaceAlpha=}")
            logger.debug(f"{buttonList[i].textSurfaceOutlineAlpha=}")

        buttonList = Misc.shiftList(buttonList, -shift_right)
        self.currentButtonIdx = -shift_right

        return buttonList

    def lockUI(self, cooldown):
        self.uiLockTemp = True
        self.uiLock = True
        self.uiLockTimeSet = pygame.time.get_ticks()
        self.uiLockCooldown = cooldown

    # Function ran once when a button selection is detected.
    def checkButtonSelected(self, selected_button):
        buttonName = selected_button.name
        # Using facts of string.partition to nest button menus with depth of 2 
        partitionedName = buttonName.partition(".")
        category = partitionedName[0]
        separator = partitionedName[1]
        buttonName2 = partitionedName[2]
        self.buttonPressedName = buttonName
        logger.debug(f"{buttonName=}, {partitionedName=}, {category=}, {separator=}")
        match category:
            case Battle.PlayerTurnButtonNames.FLEE: 
                # Has no nested buttons 
                if self.canFlee:
                    self.uiLock = True
                    surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                    surf.set_alpha(0)
                    surf.fill((0,0,0))
                    self.cover[0] = surf
                    self.coverPos[0] = (0,0)
                    self.cover[1] = self.lastAreaFrame
                    self.coverPos[1] = (0,0)
                    for button in self.currentButtons:
                        button.animateTextToAlpha(alpha=0, step=-10)
                    self.lastAreaFrame.set_alpha(0)
                else:
                    self.lockUI(200)
                return None
            case Battle.PlayerTurnButtonNames.ATTACK:
                if separator != ".": 
                    #Case where buttonname is ATTACK & no dots found
                    self.uiLock = True
                    self.player.setSelectedTargetPos(self.enemy.rect.x, self.enemy.rect.y)
                    for button in self.currentButtons:
                        if button.name == Battle.PlayerTurnButtonNames.ATTACK:
                            outlineColor = button.outlineColor
                            textColor = button.textColor
                            desiredOutlineColor = outlineColor[0] - 30, outlineColor[1] - 150, outlineColor[2]
                            desiredTextColor = textColor[0] + 30, textColor[1] + 30, textColor[2] + 30
                            button.animateTextOutlineToColor(color= desiredOutlineColor, lastColor = outlineColor)
                            button.animateTextToColor(color= desiredTextColor)
                            button.animateTextToSize(button.fontSize + 3, 1, shrink=False)
                            button.animateTextToAlpha(alpha=200, step=-20)
                            currentPos = button.rect.centerx, button.rect.centery
                            goalPos = button.rect.centerx, button.rect.centery - Battle.BUTTON_MODEL_ELLIPSE[1]
                            logger.debug(f"{currentPos=}, {goalPos=}") 
                            button.animateTextToPosition(goal_pos = goalPos, current_pos = currentPos, middle= True, num_steps=10)
                            button.animateTextToAlpha(alpha= 150, step = -20)
                            continue
                        button.animateTextToAlpha(alpha=0, step=-30)

                    return None

                ### Button pressed from Attack Button Menu case
                match buttonName2:
                    case "BACK":
                        self.uiLock = True
                        for button in self.currentButtons:
                            button.animateTextToAlpha(alpha = 0, step = -10)

                    case _:
                        logger.debug(f"{buttonName2=}, {MOVES.MOVE_LIST=}")
                        assert buttonName2 in MOVES.MOVE_NAMES
                        self.uiLock = True
                        self.additionalBackgroundSurfs.clear()
                        self.additionalBackgroundSurfsPos.clear()
                        self.player.setSelectedMove(move_name = buttonName2)
                        for button in self.currentButtons:
                            button.animateTextToAlpha(alpha = 0, step = -40)
                        
                        #self.setBattleState(Battle.States.ANIMATING_MOVE)

            #case Battle.PlayerTurnButtonNames.WAIT:
            #    pass
            #    return None
            case _:
                ### If the following code below is reached than button name is invalid or has not been added functionality yet
                raise Exception(f"Selected button with name {selected_button.name} has invalid or unchecked name")

    def updateButtonsOnUIInput(self, current_buttons, current_button_idx, direction=1, button_pressed = False):
        unselectedOpacity = 100
        selectedOpacity = 255
        mainPos = Battle.ButtonPositions[0]
        if button_pressed:
            self.checkButtonSelected(current_buttons[current_button_idx]) 
            return None
        for i in range(len(current_buttons)):
            currentButton = current_buttons[i]
            if direction == 1:
                interpolatedPositions = Battle.InterpolatedButtonPositions[current_button_idx - i - 1]
            else:
                interpolatedPositions = Battle.InterpolatedButtonPositions[current_button_idx - i ]
            adjustedPositions = numpy.zeros(interpolatedPositions.shape)
            for index, position in enumerate(interpolatedPositions):
                adjustedPositions[index] = Misc.bottomToTopleftPos(position, currentButton.textSurface) 
            if direction == -1:
                adjustedPositions = numpy.flip(adjustedPositions, 0)
            logger.debug(f"{interpolatedPositions=}, {adjustedPositions=}")
            currentButton.animateTextToPosition(current_pos = adjustedPositions[0], goal_pos = adjustedPositions[-1], given_positions = True, positions=adjustedPositions, step=1)




            if i == current_button_idx:
                currentButton.animateTextWithOutline()
                currentButton.setTextSurfaceAlpha(selectedOpacity)
                currentButton.setTextSurfaceOutlineAlpha(selectedOpacity)
                currentButton.animateTextToSize(size= currentButton.originalFontSize + 3, step=2, shrink=False)

                continue
            currentButton.animateTextWithOutline(currentButton.originalOutlineColor, size="small")
            currentButton.setTextSurfaceAlpha(unselectedOpacity) 
            currentButton.setTextSurfaceOutlineAlpha(unselectedOpacity)
            sizeDiff = int((mainPos[1] - Battle.ButtonPositions[current_button_idx-i, 1])/10 + 3)
            lastSize = currentButton.fontSize
            currSize = currentButton.originalFontSize - sizeDiff
            logger.debug(f"{mainPos=}")
            logger.debug(f"{lastSize=}") 
            logger.debug(f"{currSize=}") 
            logger.debug(f"{sizeDiff=}")
            logger.debug(f"{lastSize >= currSize=}")
            currentButton.animateTextToSize(size= currSize, step= 2, shrink= lastSize > currSize)

    def checkInput(self, state: str, battle_state: str):
        if state != SceneStates.RUNNING:
            return None
        if battle_state == Battle.States.PREPARING_TURN or battle_state == Battle.States.ENEMY_CHOOSING_MOVE:
            return None
        if self.uiLock: return None
        keys = pygame.key.get_pressed()
        timenow = pygame.time.get_ticks()
        cooldown = 300
        direction = 0
        buttonPressed = False
        lastButtonIdx = self.currentButtonIdx
        currentButtonIdx = lastButtonIdx
        match battle_state:
            case Battle.States.PLAYER_CHOOSING_ACTION:
                if self.uiLock:
                    return None
                if timenow - self.timeLastInput < cooldown:
                    return None

                for key in SAVED_DATA.UI_MOVE_RIGHT:
                    if not keys[key]:
                        continue
                    # do something
                    direction = 1
                    currentButtonIdx+=1
                    if currentButtonIdx >= len(self.currentButtons):
                        currentButtonIdx = 0 
                    self.timeLastInput = timenow
                for key in SAVED_DATA.UI_MOVE_LEFT:
                    if not keys[key]:
                        continue 
                    direction = -1
                    currentButtonIdx -= 1
                    if currentButtonIdx < 0:
                        currentButtonIdx = len(self.currentButtons) - 1
                    self.timeLastInput = timenow
                for key in SAVED_DATA.UI_SELECT:
                    if not keys[key]: continue
                    direction = 0
                    self.timeLastInput = timenow
                    buttonPressed = True
                logger.debug(f"{direction=}, {buttonPressed=}, {lastButtonIdx=}, {currentButtonIdx=}") 
                if lastButtonIdx != currentButtonIdx or buttonPressed:
                    self.buttonIndices[self.currentButtonMenu] = currentButtonIdx
                    self.updateButtonsOnUIInput(self.currentButtons, currentButtonIdx, direction, buttonPressed)
                    self.currentButtonIdx = currentButtonIdx
                    if buttonPressed:
                        pass

    def setBattleState(self, state: str):
        assert SETTINGS_FUNCTIONS.checkVariableInClass(state, Battle.States)
        self.battleState = state

    def loadEnemy(self, name: str, bottom_pos) -> BattleSceneEntity:
        match name:
            case EnemyNames.GROUNDER:
                return BattleSceneEntity(name = EnemyNames.GROUNDER, enemy = True, position = bottom_pos)
            case _:
                return BattleSceneEntity(name = EnemyNames.GROUNDER, enemy = True, position = bottom_pos)

    def loadPlayer(self, bottom_pos) -> BattleSceneEntity:
        return BattleSceneEntity(name=PLAYER, enemy=False, position=bottom_pos)

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
        self.player.render(newScreen)
        self.enemy.render(newScreen)
        #newScreen.blit(self.player.baseSprite, (self.player.rect.x, self.player.rect.y))
        #newScreen.blit(self.enemy.baseSprite, (self.enemy.rect.x, self.enemy.rect.y))
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

    def blitBackground(self, screen: pygame.Surface):
        screen.blit(self.backgroundFull, (0,0))
        self.blitSurfs(screen, self.additionalBackgroundSurfs, self.additionalBackgroundSurfsPos)
        '''
        for i, surf in enumerate(self.additionalBackgroundSurfs):
            screen.blit(surf, self.additionalBackgroundSurfsPos[i])
        '''  

    def blitSurfs(self, screen, lst_surf, lst_pos):
        for i, surf in enumerate(lst_surf):
            screen.blit(surf, lst_pos[i])
    
    def blitCover(self, screen, cover, cover_pos):
        if not cover[0]: return None
        for index, aCover in enumerate(cover):
            if not aCover: continue
            if not cover_pos[index]: continue
            logger.debug(f"COVER OPACITY: {aCover.get_alpha()}")
            screen.blit(aCover, cover_pos[index])

    # Calculate Flee pct and rng to determine flee outcome as fled or not fled
    # Will add feature later, for now it is a number from 0-9 or always true for debugging purposes
    def determinePlayerFlee(self) -> bool:
        '''
        if numpy.random.randint(low=0, high=9, size=1, dtype=numpy.uint8)[0] > 4:
            return False
        return True
        '''
        return True

    def fleePressedUpdater(self, can_flee: bool, cover_idx: int, cover: list, opacity: int):
        if can_flee:
            #if cover_idx == coverLength:
            #    return None
            if opacity == 255:
                cover_idx += 1
                opacity = 0
                
                self.coverIdx = cover_idx
                coverLen = 0
                for i in cover:
                    if not i:
                        continue
                    coverLen+=1
                assert not (cover_idx > coverLen or cover_idx < 0) 
                if cover_idx == coverLen:
                    self.setState(SceneStates.FINISHING)
                    return None


            opacity += 10
            if opacity >= 255:
                opacity = 255
            cover[cover_idx].set_alpha(opacity)
            self.opacity = opacity
        else:
            self.buttonPressedName = Battle.NONE 
            self.lockUI(200)

    def updateTimingRect(self, timing_rect: pygame.Rect, outer_rect: pygame.Rect):
        if self.timingRectIncreaseRate == 0:
            return None
        keys = pygame.key.get_pressed()
        if keys[SAVED_DATA.BATTLE_TIMING_BUTTON]:
            self.timingRectIncreaseRate = 0
            self.player.currentGroupIdx += 1
            return None
        maxTries = 2
        increaseRate = self.timingRectIncreaseRate
        if timing_rect.width < 0:
            if self.tryNum >= maxTries: return None
            self.tryNum+=1
            timing_rect.width = 0
            self.timingRectIncreaseRate = -increaseRate

        if timing_rect.width == outer_rect.width:
            self.timingRectIncreaseRate = -increaseRate
        timing_rect.width += self.timingRectIncreaseRate
        if timing_rect.width >= outer_rect.width:
            timing_rect.width = outer_rect.width

    def drawTimingRect(self, rect: pygame.Rect, screen: pygame.Surface, color: tuple[int, int, int]):
        pygame.draw.rect(screen, color, rect) #draws the inner bar

    # enemies choose move by rng.
    def chooseEnemyMove(self, enemy: BattleSceneEntity):
        moveNames = list(enemy.getMoves().keys());
        numMoves = len(enemy.getMoves().keys());
        moveIdx = random.randint(1, numMoves); 
        #logger.debug(f"NUMBER OF MOVES: {numMoves}. \nMOVE IDX CHOSEN: {moveIdx}");
        self.enemy.setSelectedMove(moveNames[moveIdx - 1]);
        #logger.debug(f"MOVE CHOSEN: {moveNames[moveIdx - 1]}");
        
    def checkBattleState(self, screen: pygame.Surface, battle_state: str):
        logger.debug(f"{battle_state=}, {self.prevState=}, {self.state=}")
        blittedSurface = pygame.Surface(screen.get_size())
        self.blitBackground(blittedSurface)
        #zoomToPos = (0, 0)
        zoomToPos = (blittedSurface.get_width()/2 - self.player.rect.center[0], blittedSurface.get_height()/2 - self.player.rect.center[1])
        xOffset = 0

        match battle_state:
            case self.States.PLAYER_CHOOSING_ACTION:
                if self.prevState == Battle.States.PREPARING_TURN:
                    self.zoomState = Battle.ZoomStates.ZOOMING_TO_RECT
                    self.prevState = self.state
                buttonPressedNamePartition = self.buttonPressedName.partition('.')
                if self.uiLock and self.buttonPressedName != Battle.NONE:
                    logger.debug(f"BUTTON PRESSED NAME: {self.buttonPressedName}")

                    #Flee Button Pressed
                    if self.buttonPressedName == Battle.PlayerTurnButtonNames.FLEE:
                        self.fleePressedUpdater(self.canFlee, self.coverIdx, self.cover, self.opacity)
                        
                    #Attack Button pressed
                    if self.buttonPressedName == Battle.PlayerTurnButtonNames.ATTACK:
                        currButton = self.currentButtons[self.currentButtonIdx]
                        alphaChanging = False
                        for i in range(len(self.currentButtons)):
                            if i == self.currentButtonIdx:
                                continue
                            if self.currentButtons[i].textAnimationInfo.getAlphaChanging():
                                alphaChanging = True
                        if not (currButton.textAnimationInfo.getLerpXY() or alphaChanging):
                            size = currButton.textSurface.get_size()[0] + 4, currButton.textSurface.get_size()[1] + 4
                            atkButton = pygame.Surface((size[0] + 4, size[1] + 4), pygame.SRCALPHA)
                            logger.debug(f"{currButton.textSurfaceOutline=}")
                            logger.debug(f"{currButton.textSurface=}")
                            basePos = (0,2)
                            offset = 2
                            atkButton.blit(currButton.textSurfaceOutline, (basePos[0] + offset,basePos[1] - offset))
                            atkButton.blit(currButton.textSurfaceOutline, (basePos[0] + offset, basePos[1] + offset))
                            atkButton.blit(currButton.textSurfaceOutline, (basePos[0] - offset , basePos[1] + offset))
                            atkButton.blit(currButton.textSurfaceOutline, (basePos[0] - offset, basePos[1] - offset))
                            atkButton.blit(currButton.textSurface, basePos)
                            atkButton.set_alpha(130)
                            self.additionalBackgroundSurfs.append(atkButton)
                            self.additionalBackgroundSurfsPos.append((currButton.rect.x, currButton.rect.y))
                            self.currentButtonMenu = Battle.ButtonMenus.ATK
                            shiftRight = -self.buttonIndices[self.currentButtonMenu]
                            logger.debug(f"SHIFT RIGHT FOR {self.currentButtonMenu} MENU: {shiftRight}")
                            self.currentButtons = self.generatePlayerAttackButtons(self.player.moves, shiftRight) 
                            self.uiLock = False
                            self.buttonPressedName = Battle.NONE 

                    # Case where attack button pressed

                    elif buttonPressedNamePartition[0] == Battle.PlayerTurnButtonNames.ATTACK and buttonPressedNamePartition[2] != "":
                        secondButtonName = buttonPressedNamePartition[2]
                        # Back button selected 
                        if secondButtonName == "BACK":
                            for surf in self.additionalBackgroundSurfs:
                                step = 10
                                newAlpha = surf.get_alpha() - step 
                                if newAlpha < 0: newAlpha = 0
                                surf.set_alpha(newAlpha)
                            alphaChanging = False
                            for button in self.currentButtons:
                                if not button.textAnimationInfo.getAlphaChanging():
                                    continue
                                alphaChanging = True 

                            if not alphaChanging:
                                self.additionalBackgroundSurfs.clear()
                                self.additionalBackgroundSurfsPos.clear()
                                self.currentButtonMenu = Battle.ButtonMenus.PLAYER_TURN
                                shiftRight= -self.buttonIndices[self.currentButtonMenu]
                                logger.debug(f"SHIFT RIGHT FOR {self.currentButtonMenu} MENU: {shiftRight}")
                                self.currentButtons = self.generatePlayerTurnButtons(shiftRight)
                                self.uiLock = False
                                self.buttonPressedName = Battle.NONE 
                    
                        # Move selected
                        else:

                            buttonsFading = False
                            for button in self.currentButtons:
                                if not button.textAnimationInfo.getAlphaChanging():
                                    continue
                                buttonsFading = True

                            if not buttonsFading:
                                # Finished transition to animating move battle state
                                # now need to center the cam to be between player and  enemy so we're truly done.
                                
                                if self.zoomLerpFactor >= 1:
                                    self.zoomLerpFactor = 1
                                zoomLerpStep = 0.05
                                xoffset = self.zoomLerpFactor * ((self.enemy.rect.center[0] - self.player.rect.center[0])/2)

                                zoomToPos = (blittedSurface.get_width()/2 - (self.player.rect.center[0] + xoffset) , blittedSurface.get_height()/2 - self.player.rect.center[1])
                                if self.zoomLerpFactor != 1:
                                    self.zoomLerpFactor += zoomLerpStep 
                                else:
                                    # battle state finished when zoomLerpFactor is 1 (because camera lerping is finished)
                                    self.setBattleState(Battle.States.ANIMATING_MOVE)
                self.updateButtons(battle_state, self.currentButtons, self.currentButtonIdx, blittedSurface)
                self.updateZoomState(self.zoomState)
                #zoomToPos = (blittedSurface.get_width()/2 - self.player.rect.center[0], blittedSurface.get_height()/2 - self.player.rect.center[1])

                # for debugging vvv
                '''
                ellipsePos = Battle.BUTTON_OFFSET[0], Battle.BUTTON_OFFSET[1] - 20
                ellipseSize = Battle.BUTTON_MODEL_ELLIPSE[0] * 2, Battle.BUTTON_MODEL_ELLIPSE[1] * 2
                pygame.draw.ellipse(blittedSurface, (0,0,0), (ellipsePos[0] - ellipseSize[0]/2, ellipsePos[1] - ellipseSize[1]/2, 2*Battle.BUTTON_MODEL_ELLIPSE[0], 2*Battle.BUTTON_MODEL_ELLIPSE[1]), width=3)
                '''
                # Debuging Code end ^^^

                if self.uiLock:
                    self.checkUILock(self.uiLockTimeSet, self.uiLockCooldown)
            # case player choosing action ends here

            case self.States.ANIMATING_MOVE:
                if self.currentEntity.getState() == BattleSceneEntity.States.DOING_MOVE:
                    if self.currentEntity.moveState == BattleSceneEntity.MoveStates.DONE:
                        logger.debug("move is done, enemies turn to attack.");
                        # now going to set up enemy attacking after this cd is over..
                        postAttackCooldown = 200 # 200 ms cd after a entity finishes attacking.
                        timenow = pygame.time.get_ticks();
                        if self.timeAttackFinished == 0:
                            self.timeAttackFinished = timenow;
                        logger.debug(f"{timenow=}, {self.timeAttackFinished=}");
                        if timenow - self.timeAttackFinished >= postAttackCooldown:
                            logger.debug("post atk cooldown finished, enemy will now attack.");
                            self.timeAttackFinished = 0;
                            self.setBattleState(self.States.ENEMY_CHOOSING_MOVE);
                if self.currentEntity.getState() == BattleSceneEntity.States.IDLE:
                    self.currentEntity.setState(BattleSceneEntity.States.DOING_MOVE)

            # case entity being anamited ends here.
            case self.States.ENEMY_CHOOSING_MOVE:
                logger.debug("enemy is choosing a move");
                self.chooseEnemyMove(self.enemy)
                self.currentEntity = self.enemy;
                self.enemy.setSelectedTargetPos(self.player.rect.x + self.player.rect.width, self.player.rect.y);
                logger.debug(f"{self.enemy.selectedTargetPos=}")
                logger.debug(f"{self.player.rect.x=}")
                logger.debug(f"{self.player.rect.y=}")
                logger.debug(f"{self.enemy.rect.x=}")
                logger.debug(f"{self.enemy.rect.y=}")
                self.enemy.setState(BattleSceneEntity.States.DOING_MOVE);

        self.player.update(blittedSurface)
        self.enemy.update(blittedSurface)

        # this if check is needed so that zoomToPosition function has the updated info after self.player.update and self.enemy.update calls. 
        if battle_state == self.States.ANIMATING_MOVE:
            xoffset =((self.enemy.rect.center[0] - self.player.rect.center[0])/2) # camera centered b/t player and enemy after updating positiosns
            zoomToPos = (blittedSurface.get_width()/2 - (self.player.rect.center[0] + xoffset) , blittedSurface.get_height()/2 - self.player.rect.center[1])
            if self.currentEntity.checkWindUp() or self.currentEntity.checkPostWindUp():
                logger.debug(f"{self.currentEntity=} IS WINDING UP")
                self.outerRect.center = (self.player.rect.center[0], self.player.rect.center[1] - self.player.rect.height/1.5)
                self.timingRect.topleft = self.outerRect.topleft
                self.timingRect.height = self.outerRect.height
                self.updateTimingRect(self.timingRect, self.outerRect)
                logger.debug(f"{self.timingRect=}, {self.outerRect=}")
                self.drawTimingRect(self.timingRect, blittedSurface, self.timingRectColor)
                Misc.drawOutline(self.outerRect, blittedSurface)
                # drawing the percentage.
                accuracy = int(100 * self.timingRect.width / self.outerRect.width) # timing accuracy (measured in percents)
                self.printAccuracy(blittedSurface, accuracy, (self.outerRect.x - 60, self.outerRect.y)) 
        
        # end of battle_state == self.states.animating_move if.
        directionZoomX = 1;
        directionZoomY = 1;
        #this if is for keeping that middle zoom thats at the end of player animating move.
        if battle_state == self.States.ENEMY_CHOOSING_MOVE:
            xoffset =((self.enemy.rect.center[0] - self.player.rect.center[0])/2) # camera centered b/t player and enemy when enemy choosing move state is reached 
            zoomToPos = (blittedSurface.get_width()/2 - (self.enemy.rect.center[0] - xoffset) , blittedSurface.get_height()/2 - self.player.rect.center[1]);
            

        SETTINGS_FUNCTIONS.zoomToPosition(screen, blittedSurface, (0,0), zoomToPos, self.zoomScale, self.zoomScale-1, directionX=directionZoomX, directionY=directionZoomY)
        self.blitCover(screen, self.cover, self.coverPos)

        ## set self.lastFrame by getting a copy of the stuff thats blitted on the screen when scene is finishing 
        if self.state == SceneStates.FINISHING:
            self.lastFrame = screen.copy()

    def printAccuracy(self, screen, accuracy, position):
        fontSurf = Misc.turnStringToFontSurf(string=f"{accuracy}%", font_fp = SAVED_DATA.FONT_PATH, color=(255,255,255)) 
        screen.blit(fontSurf, position)

    def checkUILock(self, ui_time_set, ui_cooldown):
        if not self.uiLockTemp: return None

        timenow = pygame.time.get_ticks()
        if timenow - ui_time_set < ui_cooldown:
            return None
        self.uiLock = False

    def updateButtons(self, battle_state, current_buttons, current_button_idx, screen):
        assert battle_state == self.States.PLAYER_CHOOSING_ACTION
        logger.debug(f"{current_buttons=}")
        logger.debug(f"{current_button_idx=}")
        # draw buttons
        currentButtonLen = len(current_buttons)
        for i in range(currentButtonLen):
            currentButton = current_buttons[i]
            if currentButton.fontSize == currentButton.originalFontSize:
                continue
            if currentButton.textAnimationInfo.lerpXY:
                continue
            if self.buttonPressedName != Battle.NONE:
                continue
            adjustedPos = Misc.bottomToTopleftPos(Battle.ButtonPositions[current_button_idx-i], currentButton.textSurface) 
            currentButton.setX(adjustedPos[0])
            currentButton.setY(adjustedPos[1])
        for i in range(current_button_idx - currentButtonLen , current_button_idx+1, 1):
            logger.debug(f"{current_button_idx=}")
            logger.debug(f"{i=}")
            current_buttons[i].update(screen)

    def checkState(self, state: str, screen: pygame.Surface):
        match state:
            case SceneStates.RUNNING:
                self.checkBattleState(screen, self.battleState)
            case SceneStates.ON_ANIMATION:
                self.transitionToBattleSurface(screen)
                if self.animationHandler.state == AnimationStates.FINISHED:
                    self.setState(SceneStates.RUNNING)
                    self.setBattleState(Battle.States.PLAYER_CHOOSING_ACTION)
            case SceneStates.FINISHING:
                screen.blit(self.lastFrame, (0,0))
                self.background.empty()
                self.exitScene(SceneTypes.AREA)

    def update(self, screen):
        self.checkState(state= self.state, screen= screen)
        self.checkInput(self.state, self.battleState)
        logger.debug(f"current button pos: " + f"{self.currentButtons[self.currentButtonIdx].rect=}")
        for button in self.currentButtons:
            logger.debug(f"{button.name=}, {button.rect=}")
        if DEBUG_MODE:
            self.debugExit(state= self.state)
            

    def clear(self):
        pass

