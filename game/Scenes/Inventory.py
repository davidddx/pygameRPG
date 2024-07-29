from game.Scenes.BaseScene import Scene
from debug.logger import logger
import os
import importlib
class Inventory(Scene):
    def __init__(self):
        self.inventory = self.loadInventoryData()
    def loadInventoryData(self) -> dict:
        inventoryModule = importlib.import_module("gamedata.playerdata.Inventory")
        return inventoryModule.loadInventory()
