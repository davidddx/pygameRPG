import pygame

class TileTypes:
    DOOR = "Door"
    SPAWN = "Spawn"
    ITEM = "Item"
    VISUAL = "Visual"
    WALL = "Wall"


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], collidable: bool, image: pygame.Surface,
                 _type=None):
        pygame.sprite.Sprite.__init__(self)

        self.collision = collidable
        self.tileType = _type
        self.image = image
        self.rect = image.get_rect(topleft=pos)
        self.inRange = False

    def getPos(self) -> tuple:
        return self.rect.x, self.rect.y

