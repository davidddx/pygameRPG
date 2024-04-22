from debug.logger import logger
import pygame
from game.SceneHandler import SceneHandler
import gamedata.Save.SavedData as SAVED_DATA
import os
from game.Player import Player
class Game:
    def __init__(self):

        logger.debug(f"Class {Game=} initializing....")
        self.sceneHandler = SceneHandler(_player = Game.loadPlayer(saved_data=SAVED_DATA));
        logger.debug(f"Class {Game=} intialized.")


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
        body = None
        match saved_data.PLAYER_BODY_ID:
            case 0:
                body = pygame.image.load(playerImageDir + "/PlrBody.png")
            case 1:
                pass
            case 2:
                pass
            case 3:
                pass

        return Player(pos= saved_data.PLAYER_POSITION, head_img= head, body_img= body)

