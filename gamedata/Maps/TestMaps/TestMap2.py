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


Layer0 = (
    ("G","G","G","G","G","G","G","G","G","G","G","G","G","G","G","G"),
    ("G","G","G","G","G","G","G","G","G","G","G","G","G","G","G","G"),
    ("G","G","G","G","G","G","G","G","G","G","G","G","G","G","G","G"),
)
Map = (Layer0)

cwd = os.getcwd()


grassSpriteProperties = TileSet.createTileProperties(name="Grass", image=pygame.image.load(cwd + '/images/test/GrassSprite.png'))
TileSet = {
    "G" : grassSpriteProperties,
}
