import gamedata.Save.SavedData as SAVED_DATA
class World:
    def __init__(self):
        self.areas = self.loadAreas()
        self.currentAreaID = SAVED_DATA.CURRENT_AREA_INDEX

    def loadAreas(self):
        pass
    def update(self):
        pass