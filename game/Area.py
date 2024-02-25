from game.Player import Player as Player
from debug.logger import logger
import game.utils.TileMap as TileMap
class Area:
    def __init__(self, map : TileMap):
        self.map=None
        try:
            logger.debug(f"Class {Area=} initializing....")
            # self.player = Player();
            self.map = map
            logger.debug(f"Class {Area=} intialized.")
        except Exception as e:
            logger.error(f"Failed {Area=} class initialization.\n Error: {e}")

    def update(self, screen):
        # self.player.update();
        self.displayMap(map=self.map, screen=screen)

    def prepareForSceneSwitching(self):
        self.map.collidableSpriteGroup.empty()
        self.map.nonCollidableSpriteGroup.empty()
        del self.map
    def displayMap(self, map : TileMap, screen):
        for tile in map.nonCollidableSpriteGroup:
            screen.blit(tile.image, (tile.rect.x, tile.rect.y))
        for tile in map.collidableSpriteGroup:
            screen.blit(tile.image, (tile.rect.x, tile.rect.y))
