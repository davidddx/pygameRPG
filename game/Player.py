import pygame
from debug.logger import logger
import globalVars.SettingsConstants as globalVars


class PlayerPart(pygame.sprite.Sprite):
    def __init__(self, pos : tuple[int, int], image : pygame.Surface, group : pygame.sprite.Group):
        super().__init__(group)
        self.image = image
        self.rect = image.get_rect(topleft= pos)

class Player:
    def __init__(self, pos : tuple[int,int], head_img : pygame.Surface, shirt_img : pygame.Surface, pants_img : pygame.Surface):
        self.playerGroup = pygame.sprite.Group()
        try:
            logger.debug(f"class {Player=} initializing....")
            self.playerGroup = Player.getPlayerGroup(head = head_img,
                                                     shirt = shirt_img, pants = pants_img, group=self.playerGroup, pos=pos)
            logger.debug(f"class {Player=} intialized.")

        except Exception as e:
            logger.info(f"Failed to intialize class {Player=}.\n Error: {e}")

    @staticmethod
    def render(player_group, screen):
        for _part in player_group:
            screen.blit(_part.image, (_part.rect.x, _part.rect.y))

    @staticmethod
    def getPlayerGroup(head : pygame.Surface, shirt : pygame.Surface, pants : pygame.Surface,
                       group : pygame.sprite.Group, pos : tuple[int, int]) -> pygame.sprite.Group:
        partHead = PlayerPart(pos = pos, image = head, group = group)
        partShirt = PlayerPart(pos = (pos[0], pos[1] + int(head.get_height())), image = shirt, group= group)
        partPants = PlayerPart(pos = (pos[0], int(partShirt.rect.y + shirt.get_height())), image=pants, group=group)
        group.add(partHead)
        group.add(partShirt)
        group.add(partPants)

        return group

    def update(self, screen):
        Player.render(self.playerGroup, screen=screen)