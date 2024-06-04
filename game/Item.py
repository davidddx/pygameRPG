import pygame
from game.Tile import Tile
from debug.logger import logger
class ItemConstants:
    ITEM = "Item"
    WATER = "Water"
    HEART = "Heart"
    itemIds = {
            0: WATER,
            1: HEART,
            }
    itemDescriptions = {
            WATER: "Give +1 base hp",
            HEART: "Give higher hp growth rate",
            }
    @staticmethod
    def getDescriptionByItemId(itemId: int):
        try:
            return ItemConstants.itemDescriptions[ItemConstants.itemIds[itemId]]
        except Exception as exception:
            logger.debug(f"Could not get item description for {itemId=}, {exception=}")
            return ""

    @staticmethod
    def getItemIdByName(name: str):
        try:
            ids = list(ItemConstants.itemIds.keys())
            names = list(ItemConstants.itemIds.values())
            
            return ids[names.index(name)]
        except Exception as e:
            logger.error(f"Could not get item id by {name=}, {e}")
            return 0

class Item(Tile):
    def __init__(self, sprite : pygame.Surface, pos: tuple[int, int], name: str):
        super().__init__(pos= pos, collidable= True, image=sprite, _type= ItemConstants.ITEM)
        self.id = ItemConstants.getItemIdByName(name= name)
        self.name = name

