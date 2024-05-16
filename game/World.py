import gamedata.Save.SavedData as SAVED_DATA
class World:
    def __init__(self):
        self.areaLocations = self.loadAreas()
        self.currentArea = self.loadCurrentArea(SAVED_DATA.CURRENT_AREA_INDEX)
    def loadAreas(self):
        pass
    def loadCurrentArea(self):
        pass
    def update(self):
        pass
