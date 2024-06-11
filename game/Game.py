import game.SceneHandler as SceneHandler
from game.Scenes.TitleScreen import TitleScreen
from debug.DebugMenu import DebugMenu
import pygame
import sys, os
import globalVars.SettingsConstants as SETTINGS
from debug.logger import logger
def generateScreenFromResolution(width:int, height:int) -> pygame.Surface:
    horizontalTileRatio = 11
    verticalTileRatio = 7
    tileSize = 48
    tilesHorizontal = int(width/tileSize) 
    tilesVertical = int(height/tileSize)
    print(f"{tilesHorizontal=}, {tilesVertical=}")
    ratioMultiple = int(min(tilesHorizontal / horizontalTileRatio, tilesVertical / verticalTileRatio) - 1) * 48 
    print(f"{ratioMultiple=}")
    return pygame.display.set_mode((horizontalTileRatio * ratioMultiple, verticalTileRatio * ratioMultiple))

def loop():
    pygame.init()
    running = True
    clock = pygame.time.Clock();
    pygame.init()
    
    displayInfo = pygame.display.Info()
    print(displayInfo)
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

#        if type(sceneHandler.currentScene) == TitleScreen:
#            playButton = sceneHandler.getCurrentScene().getPlayButton()
#            rect = playButton.getScaledRect()
#            pygame.draw.rect(screen, (0,0,0), rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()



