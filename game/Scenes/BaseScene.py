from abc import ABC, abstractmethod


class Scene(ABC):

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def clearScene(self):
        pass