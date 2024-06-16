import game.SceneHandler as SceneHandler
from game.Scenes.TitleScreen import TitleScreen
from debug.DebugMenu import DebugMenu
import pygame
import sys, os
import globalVars.SettingsConstants as SETTINGS
from debug.logger import logger
import gamedata.playerdata.Inventory as Inventory

def generateScreenFromResolution(width:int, height:int, fullscreen = False) -> pygame.Surface:
    if fullscreen == True: return pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    horizontalTileRatio = 11
    verticalTileRatio = 7
    tileSize = 48
    tilesHorizontal = int(width/tileSize) 
    tilesVertical = int(height/tileSize)
    ratioMultiple = int(min(tilesHorizontal / horizontalTileRatio, tilesVertical / verticalTileRatio) - 1) * 48 
    return pygame.display.set_mode((horizontalTileRatio * ratioMultiple, verticalTileRatio * ratioMultiple))

def getIcon(cwd: str) -> pygame.Surface: 
    return pygame.image.load(os.path.join(cwd, "icon", "icon.png"))

def loop():
    logger.info("Initializing Game....")
    ### Initializing Game ###
    pygame.init()
    running = True
    pygame.init()
    cwd = os.getcwd()
    pygame.display.set_icon(getIcon(cwd))
    displayInfo = pygame.display.Info()
    displaySize = displayInfo.current_w, displayInfo.current_h
    screen = pygame.display.set_mode((SETTINGS.SCREEN_WIDTH, SETTINGS.SCREEN_HEIGHT))
    baseScreen = screen.copy()
    del screen
    screen = generateScreenFromResolution(displaySize[0], displaySize[1])
    clock = pygame.time.Clock()
    running = True
    screenFillColor = "black"
    MAX_FPS = 45
    sceneHandler = SceneHandler.SceneHandler(DEBUG=True, display_size = displaySize)
    Inventory.Inventory = Inventory.loadInventory()
    ### Initialization Done ###
    logger.info("Initializing Done.")
    windowResizeCooldown = 100
    upscaleWindowKeyId = pygame.K_PLUS
    downscaleWindowKeyId = pygame.K_MINUS
    while running:
        keys = pygame.key.get_pressed()
        if keys[upscaleWindowKeyId]:
            pass
        elif keys[downscaleWindowKeyId]:
            pass
        logger.debug(f"CURRENT FPS: {clock.get_fps()}")
        clock.tick(MAX_FPS)
        baseScreen.fill(screenFillColor)

        sceneHandler.runDebug(screen=baseScreen, clock= clock)

        
        screen.blit(pygame.transform.scale(baseScreen, screen.get_rect().size), (0, 0))
        '''
        if type(sceneHandler.currentScene) == TitleScreen:
            playButton = sceneHandler.getCurrentScene().getPlayButton()
            rect = playButton.getScaledRect()
            pygame.draw.rect(screen, (0,0,0), rect)
        '''
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
    pygame.quit()



