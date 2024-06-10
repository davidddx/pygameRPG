from abc import ABC, abstractmethod
import pygame


class SceneStates:
    INITIALIZING = "INITIALIZING"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    FINISHED = "FINISHED"
    ON_ANIMATION = "ANIMATION"

class Scene(ABC):

    def __init__(self, name):
        self.name = name
        self.state = ""

    @abstractmethod
    def update(self, screen: pygame.Surface):
        pass

    @abstractmethod
    def clear(self):
        pass
