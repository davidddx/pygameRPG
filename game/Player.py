import pygame
from debug.logger import logger
import globalVars.SettingsConstants as globalVars


class PlayerPart(pygame.sprite.Sprite):
    def __init__(self, pos : tuple[int, int], image : pygame.Surface, group : pygame.sprite.Group):
        super().__init__(group)
        self.image = image
        self.rect = image.get_rect(topleft= pos)

class Player:
    def __init__(self, pos : tuple[int,int], head_img : pygame.Surface, body_img : pygame.Surface):
        self.playerGroup = pygame.sprite.Group()
        try:
            logger.info(f"class {Player=} initializing....")
            self.playerGroup = Player.getPlayerGroup(head = head_img, body = body_img, group=self.playerGroup, pos=pos)
            logger.info(f"class {Player=} initialized.")

        except Exception as e:
            logger.info(f"Failed to initialize class {Player=}.\n Error: {e}")

    @staticmethod
    def render(player_group, screen):
        for _part in player_group:
            screen.blit(_part.image, (_part.rect.x, _part.rect.y))

    @staticmethod
    def getPlayerGroup(head : pygame.Surface, body : pygame.Surface,
                       group : pygame.sprite.Group, pos : tuple[int, int]) -> pygame.sprite.Group:
        partList = []

        partHead = PlayerPart(pos = (pos[0] - int(body.get_width() - head.get_width()), pos[1]), image= head, group= group)
        partBody = PlayerPart(pos = (pos[0], pos[1] + head.get_width()), image = body, group= group)
        return group

    def handleInput(self):
        if pygame.K_a:
            pass
        elif pygame.K_d:
            pass
        

    def update(self, screen):
        Player.render(self.playerGroup, screen=screen)