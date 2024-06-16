from abc import ABC, abstractmethod
import pygame


class SceneStates:
    INITIALIZING = "INITIALIZING"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    FINISHED = "FINISHED"
    ON_ANIMATION = "ANIMATION"

class SceneTypes:
    NONE = "NONE"
    AREA = "AREA"
    INVENTORY = "INVENTORY"
    PAUSE_MENU = "PAUSE_MENU"
    TITLE_SCREEN = "TITLE_SCREEN"

class Scene(ABC):

    def __init__(self, name):
        self.name = name
        self.state = ""
        self.ptrNextScene = SceneTypes.NONE

    @abstractmethod
    def update(self, screen: pygame.Surface):
        pass

    def getPtrNextScene(self): return self.ptrNextScene

    def setPtrNextScene(self, ptrNextScene: str):
        self.ptrNextScene = ptrNextScene 


    @abstractmethod
    def clear(self):
        pass
