import pygame
import os
#from game.utils.Button import Button
from game.Scenes.BaseScene import Scene, SceneStates, SceneTypes
class PauseMenu(Scene):
    def __init__(self, name: str, last_world_frame: pygame.Surface, time_last_paused):
        self.name = name
        self.state = SceneStates.INITIALIZING
        self.lastWorldFrame = last_world_frame 
        self.timeLastPaused = time_last_paused
        self.state = SceneStates.RUNNING
    def render(self, screen):
        screen.blit(self.lastWorldFrame, (0,0))

    def update(self, screen):
        self.checkUnpauseSignal()
        self.render(screen)
    
    def getTimeLastPaused(self): return self.timeLastPaused

    def checkUnpauseSignal(self):
        timenow = pygame.time.get_ticks()
        pauseCooldown = 300
        if timenow - self.timeLastPaused < pauseCooldown:
            return None

        pauseKey = pygame.K_x
        keys = pygame.key.get_pressed()
        if keys[pauseKey]:
            self.state = SceneStates.FINISHED
            self.timeLastPaused = timenow    
            self.ptrNextScene = SceneTypes.AREA
    def clear(self):
        pass
