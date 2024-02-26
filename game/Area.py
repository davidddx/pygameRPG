from debug.logger import logger
import game.TileMap as TileMap
import pygame
class Area:
    def __init__(self, maps : tuple[TileMap.TileMap]):
        self.currentMap = None
        self.maps = ()
        self.mapidx = 0
        self.timeLastChangedArea = 0
        try:
            logger.debug(f"Class {Area=} initializing....")
            # self.player = Player();
            self.maps = maps
            self.currentMap = maps[self.mapidx]
            logger.debug(f"Class {Area=} intialized.")
        except Exception as e:
            logger.error(f"Failed {Area=} class initialization.\n Error: {e}")

    def update(self, screen):
        # self.player.update();
        AREA_SWITCH_COOLDOWN = 70
        self.displayMap(_map=self.currentMap, screen=screen)
        self.checkChangeAreaSignal(cool_down = AREA_SWITCH_COOLDOWN)

    def delete(self):
        self.currentMap.collidableSpriteGroup.empty()
        self.currentMap.nonCollidableSpriteGroup.empty()

    def displayMap(self, _map : TileMap, screen):
        for tile in _map.nonCollidableSpriteGroup:
            screen.blit(tile.image, (tile.rect.x, tile.rect.y))
        for tile in _map.collidableSpriteGroup:
            screen.blit(tile.image, (tile.rect.x, tile.rect.y))


    def checkChangeAreaSignal(self, cool_down : int):
        timenow = pygame.time.get_ticks()
        if timenow - self.timeLastChangedArea <= cool_down:
            return None
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.changeAreaToNext(time_now= timenow)
        elif keys[pygame.K_a]:
            self.changeAreaToPrevious(time_now= timenow)

    def changeAreaToNext(self, time_now: int, step=1):
        self.timeLastChangedArea = time_now
        logger.info(f"Leaving area {self.maps[self.mapidx]} \n \t \t Trying to change area to map idx {self.mapidx+step=}...")
        originalIdx = self.mapidx
        self.mapidx += step

        if self.mapidx >= len(self.maps):
            self.mapidx = originalIdx
            logger.error(
                f"Issue changing area to previous: \n \t \t \twhen {self.mapidx=} added by {step=}, self.mapidx is out of range.")
            return None
        self.currentMap = 0
        self.currentMap = self.maps[self.mapidx]
        logger.info(f"Succefully changed map to {self.maps[self.mapidx]=}")


    def changeAreaToPrevious(self, time_now : int, step=1):
        logger.info(f"Leaving area {self.maps[self.mapidx]} \n \t \t Trying to change area to map idx {self.mapidx-step=}...")
        self.timeLastChangedArea = time_now
        originalidx = self.mapidx
        self.mapidx -= step

        if self.mapidx < 0:
            self.mapidx=originalidx
            logger.error(
                f"Issue changing area to previous: \n \t \t \twhen {self.mapidx=} subtracted by {step=}, self.mapidx is out of range.")
            return None
        self.currentMap = 0
        self.currentMap = self.maps[self.mapidx]
        logger.info(f"Succefully changed map to {self.maps[self.mapidx]=}")
