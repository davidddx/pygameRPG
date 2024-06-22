from game.Scenes.BaseScene import Scene, SceneStates,SceneTypes
import pygame

class Settings(Scene):
    def __init__(self):
        super().__init__(name = SceneTypes.SETTINGS)
        self.state = SceneStates.RUNNING

    def clear(self):
        pass

    def update(self, screen: pygame.Surface):
        screen.fill("BLACK")
        self.checkSceneState()

    def checkSceneState(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_f]:

            self.state = SceneStates.FINISHED
            self.ptrNextScene = SceneTypes.PAUSE_MENU 
