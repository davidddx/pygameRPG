import pygame.sprite

class MinimalPart(pygame.sprite.Sprite):
    NONE = "NONE"
    def __init__(self, group: pygame.sprite.Group, name: str, image):
        super().__init__(group)
        self.name = name
        self.image = image

    def render(self, position: tuple, screen: pygame.Surface):
        if self.image is None:
            return None
        screen.blit(self.image, position)


