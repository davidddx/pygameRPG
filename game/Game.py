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
        plrParts = {
            "player": pygame.image.load(f"{playerImageDir}/PlrSpriteReferenceNew.png")
        }

        #
        # match saved_data.PLAYER_HEAD_ID:
        #     case 0: pass
        #     case 1: pass
        #     case 2: pass
        #     case 3: pass
        # shirt = None
        # match saved_data.PLAYER_SHIRT_ID:
        #     case 0: shirt = pygame.image.load(shirtDir + "/PlrBody0.png")
        #     case 1: pass
        #     case 2: pass
        #     case 3: pass
        # feet = None
        # match saved_data.PLAYER_FEET_ID:
        #     case 0: feet = pygame.image.load(feetDir + "/PlrFeet.png")
        #     case 1: pass
        #     case 2: pass
        #     case 3: pass
        # arms = None
        # match saved_data.PLAYER_ARMS_ID:
        #     case 0: arms = pygame.image.load(armsDir + "/PlrArms.png")
        #     case 1: pass
        #     case 2: pass
        #     case 3: pass
        # hair = None
        # match saved_data.PLAYER_HAIR_ID:
        #     case 0: hair = pygame.image.load(hairDir + "/Bald.png")
        #     case 1: pass
        #     case 2: pass
        #     case 3: pass
        # match saved_data.PLAYER_EYES_ID:
        #     case 0: pass
        # match saved_data.PLAYER_EYEBROWS_ID:
        #     case 0: pass
        return Player(pos= saved_data.PLAYER_POSITION, plrPartsDict=plrParts)
