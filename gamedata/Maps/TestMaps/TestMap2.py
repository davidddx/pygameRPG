import os
import pygame
from game.TileMap import TileSet

# tile_map should be in the following form:
# Layer0 = ( (uniqueTileCharA0, uniqueTileCharB0, .... ), (uniqueTileCharA1, uniqueTileCharB1, ....), ...)
# Layer1 = ( (uniqueTileCharA0, uniqueTileCharB0, .... ), (uniqueTileCharA1, uniqueTileCharB1, ....), ...)
# .......
# .......
# .......
# Map = (Layer0, Layer1, ....)
MAP_ID = 1

Layer0 = [
    ["G", "G", "G", "G", "G", "G", "G"],
    ["G", "G", "G", "G", "G", "G", "G"],
    ["G", "G", "G", "G", "G", "G", "G"],
    ["G", "G", "G", "G", "G", "G", "G"],
]
Layer1 = [
    [],
    ["UL", "U", "U", "U", "U", "U", "UR"],
    ["L", "M", "M", "M", "M", "M", "R"],
    ["DL", "D", "D", "D", "D", "D", "DR"],
]
Map = (Layer0, Layer1)

cwd = os.getcwd()


grassSpriteProperties = TileSet.createTileProperties(name="Grass", image=pygame.image.load(cwd + '/images/test/GrassSprite.png'))

middleDirtProperties = TileSet.createTileProperties(name="MiddleDirtSprite", image=pygame.image.load(cwd + '/images/test/DirtSpriteMiddle.png'))
rightDirtProperties = TileSet.createTileProperties(name="RightDirtSprite", image=pygame.image.load(cwd + '/images/test/DirtSpriteRight.png'))
leftDirtProperties = TileSet.createTileProperties(name="LeftDirtSprite", image=pygame.image.load(cwd + '/images/test/DirtSpriteLeft.png'))
upDirtProperties = TileSet.createTileProperties(name="UpDirtSprite", image=pygame.image.load(cwd + '/images/test/DirtSpriteUp.png'))
downDirtProperties = TileSet.createTileProperties(name="DownDirtSprite", image=pygame.image.load(cwd + '/images/test/DirtSpriteDown.png'))
upRightDirtProperties = TileSet.createTileProperties(name="UpRightDirtSprite", image=pygame.image.load(cwd + '/images/test/DirtSpriteUpRight.png'))
upLeftDirtProperties = TileSet.createTileProperties(name="UpLeftDirtSprite", image=pygame.image.load(cwd + '/images/test/DirtSpriteUpLeft.png'))
downRightDirtProperties = TileSet.createTileProperties(name="DownRightDirtSprite", image=pygame.image.load(cwd + '/images/test/DirtSpriteDownRight.png'))
downLeftDirtProperties = TileSet.createTileProperties(name="DownLeftDirtSprite", image=pygame.image.load(cwd + '/images/test/DirtSpriteDownLeft.png'))

TileSet = {
    "G" : grassSpriteProperties,
    "R" : rightDirtProperties,
    "L" : leftDirtProperties,
    "U" : upDirtProperties,
    "D" : downDirtProperties,
    "M" : middleDirtProperties,
    "UR": upRightDirtProperties,
    "DR": downRightDirtProperties,
    "UL": upLeftDirtProperties,
    "DL": downLeftDirtProperties
}
