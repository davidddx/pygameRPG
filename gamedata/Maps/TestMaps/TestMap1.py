import os
import pygame
from game.TileMap import TileSet

# tile_map should be in the following form:
# MAP_ID = the map id
# Layer0 = ( (uniqueTileCharA0, uniqueTileCharB0, .... ), (uniqueTileCharA1, uniqueTileCharB1, ....), ...)
# Layer1 = ( (uniqueTileCharA0, uniqueTileCharB0, .... ), (uniqueTileCharA1, uniqueTileCharB1, ....), ...)
# .......
# .......
# .......
# Map = (Layer0, Layer1, ....)

MAP_ID = 0

Layer0 = [
    ["N","N","N","N","N","N","N","N","N","N","N","N","N","N","N","N","N","N","N","N","N","N","N","N","N","N","N","N","N","N"],
    ["Y","Y","Y","Y","Y","Y","Y","Y","Y","Y","Y","Y","Y","Y","Y","Y","Y","Y","Y","Y","Y","Y","Y","Y","Y","Y","Y","Y","Y","Y"],
    ["B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B"],
    ["G","G","G","G","G","G","G","G","G","G","G","G","G","G","G","G","G","G","G","G","G","G","G","G","G","G","G","G","G","G"],
    ["W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W"],
    ["P","P","P","P","P","P","P","P","P","P","P","P","P","P","P","P","P","P","P","P","P","P","P","P","P","P","P","P","P","P"],
    ["O","O","O","O","O","O","O","O","O","O","O","O","O","O","O","O","O","O","O","O","O","O","O","O","O","O","O","O","O","O"],
    ["R","R","R","R","R","R","R","R","R","R","R","R","R","R","R","R","R","R","R","R","R","R","R","R","R","R","R","R","R","R"],
]

Map = [Layer0]

cwd = os.getcwd()

yellowSpriteProperties = TileSet.createTileProperties(name="yellow", image=pygame.image.load(cwd + '/images/test/YellowBlock.png'))
blueSpriteProperties = TileSet.createTileProperties(name="blue", image=pygame.image.load(cwd + '/images/test/BlueBlock.png'))
blackSpriteProperties = TileSet.createTileProperties(name="black", image=pygame.image.load(cwd +'/images/test/BlackBlock.png'))
orangeSpriteProperties = TileSet.createTileProperties(name="orange", image=pygame.image.load(cwd +'/images/test/OrangeBlock.png'))
whiteSpriteProperties = TileSet.createTileProperties(name="white", image=pygame.image.load(cwd + '/images/test/WhiteBlock.png'))
purpleSpriteProperties = TileSet.createTileProperties(name="purple", image=pygame.image.load(cwd + '/images/test/PurpleBlock.png'))
greenSpriteProperties = TileSet.createTileProperties(name="green", image=pygame.image.load(cwd + '/images/test/GreenBlock.png'))
redSpriteProperties = TileSet.createTileProperties(name="red", image=pygame.image.load(cwd + '/images/test/RedBlock.png'))

TileSet = {
    "Y" : yellowSpriteProperties,
    "B" : blueSpriteProperties,
    "N" : blackSpriteProperties,
    "W" : whiteSpriteProperties,
    "P" : purpleSpriteProperties,
    "O" : orangeSpriteProperties,
    "G" : greenSpriteProperties,
    "R" : redSpriteProperties,
}
