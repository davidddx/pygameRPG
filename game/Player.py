import pygame
from debug.logger import logger
import globalVars.SettingsConstants as globalVars
import gamedata.Save.SavedData as SAVED_DATA
from typing import NamedTuple

class PlayerPart(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], image: pygame.Surface, group: pygame.sprite.Group):
        super().__init__(group)
        self.image = image
        self.rect = image.get_rect(topleft=pos)

class PossiblePlayerStates:
    RUNNING = "RUNNING"
    WALKING = "WALKING"
    NOT_MOVING = "NOT_MOVING"

class Player:
    def __init__(self, pos: tuple[int, int], head_img: pygame.Surface, body_img: pygame.Surface):
        self.playerGroup = pygame.sprite.Group()
        self.movementState = ""
        try:
            logger.info(f"class {Player=} initializing....")

            self.playerGroup = Player.generatePlayerGroup(head=head_img, body=body_img, group=self.playerGroup, pos=pos)
            self.movementState = PossiblePlayerStates.NOT_MOVING

            logger.info(f"class {Player=} initialized.")

        except Exception as e:
            logger.info(f"Failed to initialize class {Player=}.\n Error: {e}")

    @staticmethod
    def render(player_group, screen):
        for _part in player_group:
            screen.blit(_part.image, (_part.rect.x, _part.rect.y))

    @staticmethod
    def generatePlayerGroup(head: pygame.Surface, body: pygame.Surface,
                            group: pygame.sprite.Group, pos: tuple[int, int]) -> pygame.sprite.Group:
        partList = []

        partHead = PlayerPart(pos=(pos[0] - int(body.get_width() - head.get_width()), pos[1]), image=head, group=group)
        partBody = PlayerPart(pos=(pos[0], pos[1] + head.get_width()), image=body, group=group)
        return group

    def handleInput(self):
        keys = pygame.key.get_pressed()
        self.handleWalkingInput(keys)

    def handleWalkingInput(self, keys):
        diagonalStep = 2
        nonDiagonalStep = 3
        noStep = 0

        if keys[SAVED_DATA.PLAYER_RUN_KEY_ID]:
            self.movementState = PossiblePlayerStates.RUNNING
            diagonalStep *= 2
            nonDiagonalStep *= 2

        if keys[SAVED_DATA.PLAYER_WALK_RIGHT_KEY_ID]:
            if keys[SAVED_DATA.PLAYER_WALK_DOWN_KEY_ID]:
                self.movePlayerGroup(diagonalStep, diagonalStep)
            elif keys[SAVED_DATA.PLAYER_WALK_UP_KEY_ID]:
                self.movePlayerGroup(diagonalStep, -diagonalStep)
            else:
                self.movePlayerGroup(nonDiagonalStep, noStep)
        elif keys[SAVED_DATA.PLAYER_WALK_LEFT_KEY_ID]:
            if keys[SAVED_DATA.PLAYER_WALK_DOWN_KEY_ID]:
                self.movePlayerGroup(-diagonalStep, diagonalStep)
            elif keys[SAVED_DATA.PLAYER_WALK_UP_KEY_ID]:
                self.movePlayerGroup(-diagonalStep, -diagonalStep)
            else:
                self.movePlayerGroup(-nonDiagonalStep, noStep)
        elif keys[SAVED_DATA.PLAYER_WALK_UP_KEY_ID]:
            self.movePlayerGroup(noStep, -nonDiagonalStep)
        elif keys[SAVED_DATA.PLAYER_WALK_DOWN_KEY_ID]:
            self.movePlayerGroup(noStep, nonDiagonalStep)
        else:
            self.movementState = PossiblePlayerStates.NOT_MOVING

    def movePlayerGroup(self, step_x: int, step_y:int):
        logger.debug(f"Moving Player group. Walkspeed: ({step_x=}, {step_y=}")
        for part in self.playerGroup:
            part.rect.x += step_x
            part.rect.y += step_y

    def update(self, screen):
        Player.render(self.playerGroup, screen=screen)
        try:
            self.handleInput()
        except Exception as e:
            logger.errorg(f"Could not handle player input. Error: {e}")
