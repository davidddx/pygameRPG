from debug.logger import logger
class SceneHandler:
    def __init__(self):
        try:
            logger.debug(f"Class {SceneHandler=} initializing....")
            self.scenes = []
            logger.debug(f"Class {SceneHandler=} intialized.")
        except Exception as e:
            logger.error(f"Failed {SceneHandler=} class initialization.\n Error: {e}")
    def changeSceneToNext(self):
        pass
    def changeSceneToPrevious(self):
        pass
    def changeSceneByName(self, scene_name):
        pass
    def run(self):
        pass