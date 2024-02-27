from abc import ABC, abstractmethod

import pygame


class Scene(ABC):

    @abstractmethod
    def update(self, screen: pygame.Surface):
        pass

    @abstractmethod
    def clearScene(self):
        pass