from abc import ABC, abstractmethod
import pygame


class SceneStates:
    INITIALIZING = "INITIALIZING"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    FINISHING = "FINISHING"
    FINISHED = "FINISHED"
    QUIT_GAME = "QUIT_GAME"
    ON_ANIMATION = "ANIMATION"
    NONE = "NONE"

class SceneTypes:
    NONE = "NONE"
    AREA = "AREA"
    INVENTORY = "INVENTORY"
    PAUSE_MENU = "PAUSE_MENU"
    TITLE_SCREEN = "TITLE_SCREEN"
    SETTINGS = "SETTINGS"

class Scene(ABC):

    def __init__(self, name):
        self.name = name
        self.state = SceneStates.NONE
        self.ptrNextScene = SceneTypes.NONE

    @abstractmethod
    def update(self, screen: pygame.Surface):
        pass

    def getPtrNextScene(self): return self.ptrNextScene

    def setPtrNextScene(self, ptrNextScene: str):
        self.ptrNextScene = ptrNextScene 

    def getState(self): return self.state
    
    def setState(self, state: str): self.state = state

    @abstractmethod
    def clear(self):
        pass
