from debug.logger import logger
import pygame
from game.SceneHandler import SceneHandler
import gamedata.Save.SavedData as SAVED_DATA
import os
from game.Player import Player
class Game:
    def __init__(self):
        try:
            logger.debug(f"Class {Game=} initializing....")
            self.sceneHandler = SceneHandler(_player = Game.loadPlayer(saved_data=SAVED_DATA));
            logger.debug(f"Class {Game=} intialized.")
        except Exception as e:
            logger.error(f"Failed {Game=} class initialization.\n Error: {e} \n File: Game.py")

    def run(self, screen):
        self.sceneHandler.run(screen=screen)

    @staticmethod
    def loadPlayer(saved_data) -> Player:
        cwd = os.getcwd()
        playerImageDir = cwd + "/images/test/"
        head = None
        match saved_data.PLAYER_HEAD_ID:
            case 0:
                head = pygame.image.load(playerImageDir + "/PlrHead.png")
            case 1:
                pass
            case 2:
                pass
            case 3:
                pass
        shirt = None
        match saved_data.PLAYER_SHIRT_ID:
            case 0:
                shirt = pygame.image.load(playerImageDir + "/PlrShirt.png")
            case 1:
                pass
            case 2:
                pass
            case 3:
                pass
        pants = None
        match saved_data.PLAYER_PANTS_ID:
            case 0:
                pants = pygame.image.load(playerImageDir + "/PlrPants.png")
            case 1:
                pass
            case 2:
                pass
            case 3:
                pass
        return Player(pos= saved_data.PLAYER_POSITION, head_img= head, shirt_img= shirt, pants_img= pants)

