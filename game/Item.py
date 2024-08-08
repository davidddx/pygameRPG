import pygame
from game.Tile import Tile
from debug.logger import logger
class ItemConstants:
    ITEM = "ITEM"
    WATER = "WATER"

    HEART = "HEART"
    itemIds = {
            0: WATER,
            1: HEART,
            }
    
    itemDescriptions = {
            WATER: "Give +1 base hp",
            HEART: "Give higher hp growth rate",
            }
    
    BOOSTS = "BOOSTS"
    HEALING = "HEALING"
    
    itemCategories = {
            WATER: BOOSTS,
            HEART: HEALING,
            }
    
    DEFAULT_ID = 0
    DEFAULT_NAME = itemIds[DEFAULT_ID]
    DEFAULT_DESCRIPTION = itemDescriptions[DEFAULT_NAME]
    @staticmethod
    def checkValidItemId(item_id: int):
        try:
            ItemConstants.itemIds[item_id]
            return True
        except Exception as e:
            logger.error(f"Invalid Item Id {item_id=}")
            return False
    
    @staticmethod
    def checkValidItemName(item_name: str):
        try:
            ItemConstants.itemDescriptions[item_name]
            return True
        except Exception as e:
            logger.error(f"Invalid Item Name {item_name}")
            return False
    
    @staticmethod
    def checkValidItemDescription(item_description: str):
        if item_description not in ItemConstants.itemDescriptions.values():
            logger.error(f"Invalid Item Description {item_description}")
            return False
        return True

    @staticmethod
    def getCategoryById(item_id: int):
        if not ItemConstants.checkValidItemId(item_id): return ItemConstants.getCategoryByName(ItemConstants.DEFAULT_NAME)

        return ItemConstants.getCategoryByName(ItemConstants.itemIds[item_id])
    
    @staticmethod
    def getCategoryByName(item_name: str):
        if not ItemConstants.checkValidItemName(item_name):
            return ItemConstants.itemCategories[ItemConstants.DEFAULT_NAME]
        return ItemConstants.itemCategories[item_name]

    @staticmethod
    def getDescriptionByItemId(item_id: int):
        if not ItemConstants.checkValidItemId(item_id): return ItemConstants.itemDescriptions[ItemConstants.DEFAULT_NAME]  
        return ItemConstants.itemDescriptions[ItemConstants.itemIds[item_id]]
    
    @staticmethod
    def getItemNameById(id: int):
        return ItemConstants.itemIds[id]

    @staticmethod
    def getItemIdByName(name: str):
        if not ItemConstants.checkValidItemName(name):
            return ItemConstants.DEFAULT_ID
        ids = list(ItemConstants.itemIds.keys())
        names = list(ItemConstants.itemIds.values())       
        return ids[names.index(name)]

    @staticmethod
    def checkItemsEqual(name1: str, pos1, name2: str, pos2):
        if name1 != name2: return False
        if pos1[0] != pos2[0]: return False
        if pos1[1] != pos2[1]: return False
        return True

class Item(Tile):
    NAME_ID = 0
    POS_ID = 1
    def __init__(self, sprite : pygame.Surface, pos: tuple[int, int], name: str):
        super().__init__(pos= pos, collidable= True, image=sprite, _type= ItemConstants.ITEM)
        self.name = name

    @staticmethod
    def checkValidItem(item) -> bool:
        return (ItemConstants.checkValidItemId(item.getId()) and ItemConstants.checkValidItemName(item.getName()))
        
    def getId(self) -> int:
        return ItemConstants.getItemIdByName(name= self.getName())    
    def getName(self):
        return self.name
