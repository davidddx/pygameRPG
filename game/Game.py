import game.SceneHandler as SceneHandler
from game.Scenes.TitleScreen import TitleScreen
from debug.DebugMenu import DebugMenu
import pygame
import sys, os
import json
import globalVars.SettingsConstants as SETTINGS
from debug.logger import logger
import gamedata.playerdata.Inventory as Inventory
import gamedata.Save.SavedData as SAVED_DATA
import Font.FontPaths as FONT_PATHS

def generateScreenFromResolution(width:int, height:int, screen_size: str) -> pygame.Surface:
    if screen_size == "FULLSCREEN": return pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    horizontalTileRatio = 11
    verticalTileRatio = 7
    tileSize = 48
    tilesHorizontal = int(width/tileSize) 
    tilesVertical = int(height/tileSize)
    ratioMultiple = 0
    if screen_size == "LARGE":
        ratioMultiple = int(min(tilesHorizontal / horizontalTileRatio, tilesVertical / verticalTileRatio) - 1) * tileSize 
    elif screen_size == "MEDIUM":
        ratioMultiple = int(min(tilesHorizontal / horizontalTileRatio, tilesVertical / verticalTileRatio) - 1) * tileSize / 1.5
    elif screen_size == "SMALL":
        ratioMultiple = int(min(tilesHorizontal / horizontalTileRatio, tilesVertical / verticalTileRatio) - 1) * tileSize / 2
    return pygame.display.set_mode((horizontalTileRatio * ratioMultiple, verticalTileRatio * ratioMultiple))

def loadSavedData():

    fp = os.path.join(os.getcwd(), "gamedata", "settingsdata", "SettingsData.json")
    fileObj = open(fp, "r")
    gameSettings = json.load(fileObj)
    SAVED_DATA.FONT = gameSettings["FONT"]
    SAVED_DATA.SCREEN_SIZE = gameSettings["SCREEN_SIZE"]
    match SAVED_DATA.FONT:
        case "GOHU": SAVED_DATA.FONT_PATH = FONT_PATHS.GOHU
        case "AGAVE": SAVED_DATA.FONT_PATH = FONT_PATHS.AGAVE
        case "FIRA_CODE": SAVED_DATA.FONT_PATH = FONT_PATHS.FIRA_CODE
        case "MONOFUR": SAVED_DATA.FONT_PATH = FONT_PATHS.MONOFUR
        case "CASKAYDIA": SAVED_DATA.FONT_PATH = FONT_PATHS.CASKAYDIA
        case "ANONYMICE_PRO": SAVED_DATA.FONT_PATH = FONT_PATHS.ANONYMICE_PRO
        case _: SAVED_DATA.FONT_PATH = FONT_PATHS.GOHU


def getIcon(cwd: str) -> pygame.Surface: 
    return pygame.image.load(os.path.join(cwd, "icon", "icon.png"))

def loop():
    logger.info("Initializing Game....")
    ### Initializing Game ###
    pygame.init()
    running = True
    pygame.init()
    loadSavedData()
    cwd = os.getcwd()
    pygame.display.set_icon(getIcon(cwd))
    displayInfo = pygame.display.Info()
    displaySize = displayInfo.current_w, displayInfo.current_h
    screen = pygame.display.set_mode((SETTINGS.SCREEN_WIDTH, SETTINGS.SCREEN_HEIGHT))
    baseScreen = screen.copy()
    del screen
    screen = generateScreenFromResolution(displaySize[0], displaySize[1], SAVED_DATA.SCREEN_SIZE)
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

        pygame.display.flip()
        if sceneHandler.finished: 
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
    pygame.quit()



