import pygame
import math
import os
import PIL.Image as Image

def bottomToTopleftPos(bottom_pos: tuple, base_sprite: pygame.Surface):
    topleftPos = bottom_pos[0] - base_sprite.get_width()/2, bottom_pos[1] - base_sprite.get_height()
    return topleftPos

def topleftToBottomPos(topleft_pos: tuple, base_sprite: pygame.Surface):
    bottomPos = topleft_pos[0] + base_sprite.get_width()/2, topleft_pos[1] + base_sprite.get_height()
    return bottomPos

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
    return (round(distance_from_origin * math.cos(angle), decimal_places), round(distance_from_origin * math.sin(angle), decimal_places))

def getPolarCoordinates(angle, major_axis_size, minor_axis_size):
    print(f"{angle=}")
    a = minor_axis_size * math.cos(angle)
    b = major_axis_size*math.sin(angle)
    denominator = math.sqrt(a**2 + b**2)
    numerator = major_axis_size * minor_axis_size
    return numerator/denominator

