import pygame
import os
import json
import gamedata.Save.SavedData as SAVED_DATA
import Font.FontPaths as FONT_PATHS
import pathlib
from debug.logger import logger

def checkVariableInClass(variable_value, _class) -> bool:
    return True if hasattr(_class, variable_value) else False

def getIcon(cwd: str) -> pygame.Surface: 
    return pygame.image.load(os.path.join(cwd, "icon", "icon.png"))

#this function assumes that param blitted_surface already has everything drawn on it for the frame.
# screen: destination screen
# blitted surface: zooming screen 
# rect: rect to zoom in to
# zoom_scale: scale of zoom
def zoomToSurface(screen: pygame.Surface, blitted_surface: pygame.Surface, rect: pygame.Rect, zoom_scale: float, position_transition_scalar=1):
    blitted_surface = pygame.transform.smoothscale_by(blitted_surface, zoom_scale)
    blittedSurfaceRect = blitted_surface.get_rect()
    screenRect = screen.get_rect()
    blittedSurfaceRect.x = (screenRect.centerx - rect.centerx * zoom_scale) * position_transition_scalar
    blittedSurfaceRect.y = (screenRect.centery - rect.centery * zoom_scale) * position_transition_scalar
    screen.blit(blitted_surface, blittedSurfaceRect)

def zoomToPosition(screen: pygame.Surface, blitted_surface:pygame.Surface, position1, position2, zoom_scale: float, position_transition_scalar=1):
    
    '''
    ex:
    (x1, y1) to (x2, y2)
    (0,0) to (30,50), numsteps = 5
    (6, 10), (12, 20), (18, 30), (24, 40), (30,50)
    (x = (x2-x1)/5, y=(y2 - y1)/5))
    but user controls position transition scalar
    '''
    logger.debug(f"{position_transition_scalar=}")
    logger.debug(f"{position2=}")
    logger.debug(f"{position1=}")
    blitted_surface = pygame.transform.smoothscale_by(blitted_surface, zoom_scale)
    scaleOffsetX = screen.get_width()/2 * position_transition_scalar
    scaleOffsetY = screen.get_height()/2 * position_transition_scalar
    blittedSurfX = (position2[0]- position1[0] ) * position_transition_scalar  * zoom_scale - scaleOffsetX

    blittedSurfY = (position2[1] - position1[1] ) * position_transition_scalar * zoom_scale - scaleOffsetY

    #logger.debug(f"{(blittedSurfX, blittedSurfY)=}")
    '''
    center of goal position on bottom left
    '''

    screen.blit(blitted_surface, (blittedSurfX, blittedSurfY))
    #screen.blit(blitted_surface, (0,0))
    pass


    

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

def getSettingsDataFp():
    return os.path.join(os.getcwd(), "gamedata", "settingsdata", "SettingsData.json")

def loadSavedData():
    fileObj = open(getSettingsDataFp(), "r")
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
    fileObj.close()
    del fileObj

def saveSettingsFile():
    fileObjRead = open(getSettingsDataFp(), "r")
    fileContents = json.load(fileObjRead)
    fileContents["FONT"] = SAVED_DATA.FONT 
    fileContents["SCREEN_SIZE"] = SAVED_DATA.SCREEN_SIZE
    fileObjRead.close()
    fileObjWrite = open(getSettingsDataFp(), "w")
    json.dump(fileContents, fileObjWrite)
    fileObjWrite.close()

def backupJsonFile(file_path: str, file_content: dict):
    stemName = os.path.splitext(os.path.basename(file_path))[0]
    dataDirPath = pathlib.Path(os.getcwd(), 'gamedata')
    backupDirPath = pathlib.Path(dataDirPath, 'backup')
    backupFilePath = pathlib.Path(backupDirPath, f"{stemName}.json")
    if not dataDirPath.exists() or not dataDirPath.is_dir(): dataDirPath.mkdir() 
    if not backupDirPath.exists() or not backupDirPath.is_dir(): backupDirPath.mkdir() 
    if not backupFilePath.exists() or not backupFilePath.is_file(): backupFilePath.touch() 
    backupFile = open(backupFilePath, 'w')
    json.dump(file_content, backupFile)
    backupFile.close()


def updateSavedData(file_content: dict):
    fileObj = open(getSettingsDataFp(), "r")
    savedData = json.load(fileObj)
    backupJsonFile(getSettingsDataFp(), savedData)
