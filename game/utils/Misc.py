import pygame
from collections import deque
import numpy 
import os
import PIL.Image as Image
from debug.logger import logger
import gamedata.Save.PlayerCustomization as PLAYER_OUTFIT
from game.Player import PlayerPart, MinimalPart

def bottomToTopleftPos(bottom_pos: tuple, base_sprite: pygame.Surface):
    topleftPos = bottom_pos[0] - base_sprite.get_width()/2, bottom_pos[1] - base_sprite.get_height()
    return topleftPos

# S for tuple parameter b/c python doesnt have method overloading
def bottomToTopleftPosS(bottom_pos: tuple | numpy.ndarray, size: tuple):
    topleftPos = bottom_pos[0] - size[0]/2, bottom_pos[1] - size[1]
    return topleftPos

def topleftToBottomPos(topleft_pos: tuple, base_sprite: pygame.Surface):
    bottomPos = topleft_pos[0] + base_sprite.get_width()/2, topleft_pos[1] + base_sprite.get_height()
    return bottomPos

def bottomToMiddlePos(bottom_pos, size):
    middlePos = bottom_pos[0], bottom_pos[1] + size[1]/2
    return middlePos

def middleToTopleftPos(middle_pos, size):
    topleftPos = middle_pos[0] - size[0]/2, middle_pos[1] - size[1] / 2
    return topleftPos

def tileImage(tile_size: int, image_path: str, output_dir: str):
    image = Image.open(image_path)
    imageSize = image.size
    assert imageSize[0] % tile_size == 0 and imageSize[1] % tile_size == 0
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir) 
    # padding with zeros for easier sorting and to support big images
    # baseDirs = [] line used for debugging
    for i in range(0, imageSize[0], tile_size):
        baseDir = os.path.join(output_dir, padZeros(str(int(i/tile_size))))
        # baseDirs.append(baseDir) line used for debugging
        if not os.path.isdir(baseDir):
            os.makedirs(baseDir)
        for j in range(0, imageSize[1], tile_size):
            saveDir = os.path.join(baseDir, padZeros(str(int(j/tile_size))) + ".png")
            left = i
            right = i+tile_size
            upper = j
            lower = j+tile_size
            tiledImage = image.crop((left, upper, right, lower))
            tiledImage.save(saveDir)
    ''' CODE BELOW USED FOR DEBUGGING
    baseDirs.sort()
    for i in range(len(baseDirs)):
        baseDirs[i] = baseDirs[i].rpartition('/')[2]
    print(f"{baseDirs=}")
    '''

def padZeros(mystr: str, num_chars = 5, at_beginning = True, at_end=False):
    while len(mystr) < num_chars:
        if at_beginning:
            mystr = "0" + mystr 
        if at_end:
            mystr = mystr + "0"

    if len(mystr) > num_chars:
        mystr[0:len(mystr)-2]

    return mystr

def getCartesianFromPolar(distance_from_origin, angle, decimal_places=2):
    x = numpy.round(distance_from_origin * numpy.cos(angle), decimal_places)
    y = -numpy.round(distance_from_origin * numpy.sin(angle), decimal_places)
    return numpy.c_[x,y]

def changeButtonsToOpacity(current_buttons, opacity, outline_opacity=255):
    for button in current_buttons:
        button.setTextSurfaceAlpha(opacity)
        if button.textAnimationInfo.outline:
            button.setTextSurfaceOutlineAlpha(outline_opacity)

def shiftList(list_to_shift, shift_right=0):
    #using deque for performance purposes.
    # shifts a list list_to_shift right by amount shift_right
    # positive int arguments do right shift, negative int arguments do left shift
    if shift_right != 0:
        dequedList = deque(list_to_shift)
        dequedList.rotate(shift_right)
        list_to_shift = list(dequedList)
    return list_to_shift

def getPolarCoordinates(angle, vertical_radius_size, horizontal_radius_size):
    a = vertical_radius_size * numpy.cos(angle)
    b = horizontal_radius_size * numpy.sin(angle)
    denominator = numpy.sqrt(a**2 + b**2)
    numerator = vertical_radius_size * horizontal_radius_size
    logger.debug(f"{vertical_radius_size=}, {horizontal_radius_size=}, {numerator=}, {denominator=}")
    return numerator/denominator

def getPlayerPartImage(direction_path: str, name: str):
    direction_path += "/" + name
    if (name == PlayerPart.hair):
        direction_path += f"/{PLAYER_OUTFIT.PLAYER_HAIR_STYLE_ID}"
        direction_path += f"/{PLAYER_OUTFIT.PLAYER_HAIR_COLOR_ID}"
    else:
    
        direction_path +=  "/" + str(getattr(PLAYER_OUTFIT, "PLAYER_" + name.upper() + "_ID"))
    return direction_path

def loadWalkAnimByDirection(direction: str):
    assert (direction == "Front" or direction == "Back" or direction == "Left" or direction == "Right" or direction == "FrontRight" or direction == "FrontLeft" or direction == "BackRight" or direction == "BackLeft")
    walkAnimDir = os.path.join(os.getcwd(), "images", "test", "PlrSpriteTest", "AnimationTesting", "Parts", direction) 
    groupWalkAnimFrames = []
    
    numWalkFrames = 4
    for i in range(numWalkFrames):
        groupWalkAnimFrames.append(pygame.sprite.Group())
    for partName in PlayerPart.names:
        

        partIdPath = getPlayerPartImage(walkAnimDir, partName)
        logger.debug(f"{partIdPath=}")

        for i in range(numWalkFrames):
            group = groupWalkAnimFrames[i]
            imgLocation = os.path.join(partIdPath, f"{i}.png")
            logger.debug(f"{imgLocation=}")
            try:
                img = pygame.image.load(imgLocation)
                MinimalPart(group=group, name = imgLocation, image = img) # creates & adds part to group 
                logger.debug(f"{imgLocation} is a VALID IMG LOCATION")
                
            except:
                MinimalPart(group=group, name=f"({MinimalPart.NONE}) {imgLocation}", image=None) # creates & adds adds part to group
                logger.debug(f"{imgLocation} is NOT a VALID IMG LOCATION")

    return groupWalkAnimFrames
