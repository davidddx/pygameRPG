from debug.logger import logger
import pygame
from game.SceneHandler import SceneHandler
import gamedata.Save.SavedData as SAVED_DATA
import os
from game.Player import Player
class Game:
    def __init__(self):

        logger.debug(f"Class {Game=} initializing....")
        self.sceneHandler = SceneHandler(_player = Game.loadPlayerSprite(saved_data=SAVED_DATA));
        logger.debug(f"Class {Game=} intialized.")


    def run(self, screen):
        self.sceneHandler.run(screen=screen)

    @staticmethod
    def loadPlayerSprite(saved_data) -> Player:
        cwd = os.getcwd()
        playerImageDir = cwd + "/images/test/PlrSpriteTest"
        headDir = playerImageDir + "/PlrHead"
        hairDir = playerImageDir + "/PlrHair"
        eyesDir = playerImageDir + "/PlrEyes"
        eyebrowsDir = playerImageDir + "/PlrEyebrows"
        shoesDir = playerImageDir + "/PlrShoes"
        shirtDir = playerImageDir + "/PlrShirt"
        pantsDir = playerImageDir + "/PlrPants"
        armsDir = playerImageDir + "/PlrArms"

        plrParts = {
            "head" : pygame.image.load(f"{headDir}/PlrHead{saved_data.PLAYER_HEAD_ID}.png"),
            "hair" : pygame.image.load(f"{hairDir}/PlrHair{saved_data.PLAYER_HAIR_ID}.png"),
            "eyes" : pygame.image.load(f"{eyesDir}/PlrEyes{saved_data.PLAYER_EYES_ID}.png"),
            "eyebrows" : pygame.image.load(f"{eyebrowsDir}/PlrEyebrows{saved_data.PLAYER_EYEBROWS_ID}.png"),
            "shoes" : pygame.image.load(f"{shoesDir}/PlrShoes{saved_data.PLAYER_SHOES_ID}.png"),
            "shirt" : pygame.image.load(f"{shirtDir}/PlrShirt{saved_data.PLAYER_SHIRT_ID}.png"),
            "pants" : pygame.image.load(f"{pantsDir}/PlrPants{saved_data.PLAYER_PANTS_ID}.png"),
            "arms" : pygame.image.load(f"{armsDir}/PlrArms{saved_data.PLAYER_ARMS_ID}.png"),
        }

        return Player(pos= saved_data.PLAYER_POSITION, plrPartsDict=plrParts)
