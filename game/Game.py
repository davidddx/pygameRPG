import game.SceneHandler as SceneHandler
from game.Scenes.TitleScreen import TitleScreen
from debug.DebugMenu import DebugMenu
import pygame
import os
import json
import globalVars.SettingsConstants as SETTINGS
from debug.logger import logger
import gamedata.playerdata.Inventory as Inventory
import game.utils.SettingsFunctions as SETTINGS_FUNCTIONS 
import gamedata.Save.SavedData as SAVED_DATA

def loop():
    '''
    SOME MISCILLANEOUS DEBUGGING CODE
    import game.utils.Misc as Misc
    from game.Player import DirectionNames
    logger.debug(f"{Misc.loadWalkAnimByDirection(DirectionNames.RIGHT)=}")
    '''
    logger.info("Initializing Game....")
    ### Initializing Game ###
    DEBUG_MODE = SETTINGS.DEBUG_MODE
    running = True
    pygame.init()
    pygame.mixer.init()
    SETTINGS_FUNCTIONS.loadSavedData()
    cwd = os.getcwd()
    pygame.display.set_icon(SETTINGS_FUNCTIONS.getIcon(cwd))
    displayInfo = pygame.display.Info()
    displaySize = displayInfo.current_w, displayInfo.current_h
    SETTINGS.SCREEN_RESOLUTION = displaySize
    baseScreen = pygame.Surface((SETTINGS.SCREEN_WIDTH, SETTINGS.SCREEN_HEIGHT))
    SETTINGS.SCREEN = SETTINGS_FUNCTIONS.generateScreenFromResolution(displaySize[0], displaySize[1], SAVED_DATA.SCREEN_SIZE)
    clock = pygame.time.Clock()
    running = True
    screenFillColor = "black"
    MAX_FPS = 45
    sceneHandler = SceneHandler.SceneHandler(DEBUG=DEBUG_MODE, display_size = displaySize)

    ### Initialization Done ###
    logger.info("Initializing Done.")
    while running:

        logger.debug(f"CURRENT FPS: {clock.get_fps()}")
        if DEBUG_MODE:
            if pygame.key.get_pressed()[pygame.K_l]:
                MAX_FPS = 5
            else: MAX_FPS = 45
        clock.tick(MAX_FPS)
        baseScreen.fill(screenFillColor)
        sceneHandler.runDebug(screen=baseScreen, clock= clock)
        SETTINGS.SCREEN.blit(pygame.transform.scale(baseScreen, SETTINGS.SCREEN.get_rect().size), (0, 0))

        pygame.display.flip()
        if sceneHandler.finished: 
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

    #game loop has finished
    pygame.quit()



