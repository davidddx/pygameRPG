from abc import ABC, abstractmethod
import pygame


class Scene(ABC):

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def update(self, screen: pygame.Surface):
        pass

    @abstractmethod
    def clear(self):
        pass
