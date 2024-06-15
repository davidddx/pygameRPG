from game.Scenes.BaseScene import Scene
import os

class Inventory(Scene):
    def __init__(self):
        self.Items = self.loadInventoryData()
    def loadInventoryData(self):
        path = os.path.join(os.getcwd(), "")
