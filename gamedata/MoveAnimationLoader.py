import pygame
import gamedata.Moves as MOVES
import os
from game.Player import PLAYER, PlayerPart
import pygame
import gamedata.Save.PlayerCustomization as PLAYER_CUSTOMIZATION
from game.MinimalPart import MinimalPart

MOVE_ANIM_DIR = os.path.join(os.getcwd(), "images", "test", "Moves", PLAYER)

def loadMoveAnim(move_name: str, is_enemy: bool) -> list[pygame.sprite.Group]:
    if move_name not in MOVES.MOVE_NAMES:
        raise Exception(f"'{move_name}' is not a valid move name")
    currDir = os.path.join(MOVE_ANIM_DIR, move_name)
    if not os.path.exists(currDir):
        return [] 
        raise Exception(f"DIRECTORY {currDir} is invalid. {move_name=}")
        # need to add this functionality later but rn testing player
    if not os.path.isdir(currDir):
        return []
        raise Exception(f"DIRECTORY {currDir} is invalid. {move_name=}")
        # need to add this functionality later but rn testing player
    frameList = [] # Holds the animation frames, is of type list[pygame.sprite.Group
    if is_enemy:
        # need to add this functionality later but rn testing player

        #
        # CODE LOADING ENEMY MOVE ANIM
        # 
        #raise Exception("I NEED TO ADD MOVE LOADING FOR ENEMIES")
        return frameList 
    # PLAYER CASE
    animData = MOVES.ANIMATION_DATA[MOVES.PUNCH[MOVES.NAME]]
    # loops thru frame numbers so sprite groups correspond 
    for frameNumber in range(animData[0]):
        group = pygame.sprite.Group()
        for name in PlayerPart.names:
            partBaseDir = os.path.join(currDir, name)
            partDir = ""
            if name == PlayerPart.hair:
                hairStyleId = str(PLAYER_CUSTOMIZATION.PLAYER_HAIR_STYLE_ID)
                hairColorId = str(PLAYER_CUSTOMIZATION.PLAYER_HAIR_COLOR_ID)
                partDir = os.path.join(partBaseDir, hairStyleId, hairColorId)
            else:
                partId = str(getattr(PLAYER_CUSTOMIZATION, "PLAYER_" + name.upper() + "_ID"))
                partDir = os.path.join(partBaseDir, partId)
            partPath = os.path.join(partDir, f"{frameNumber}.png")
            if not os.path.exists(partPath):
                raise Exception(f"PATH {partPath} is invalid. Please fix this by putting a image here or changing the path in the code.")
            img = pygame.image.load(partPath)
            myPart = MinimalPart(group, partPath, img)
        frameList.append(group)
    return frameList
