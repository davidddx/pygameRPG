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

        def handleWalkingInput(_keys):
            diagonalStep = 1.4
            nonDiagonalStep = 2
            noStep = 0
            if _keys[SAVED_DATA.PLAYER_RUN_KEY_ID]:
                self.movementState = PossiblePlayerStates.RUNNING
                diagonalStep *= 2
                nonDiagonalStep *= 2

            ### WALKING RIGHT ###

            if _keys[SAVED_DATA.PLAYER_WALK_RIGHT_KEY_ID]:
                if _keys[SAVED_DATA.PLAYER_WALK_DOWN_KEY_ID]:
                    logger.debug("Player currently walking right && down")
                    self.movePlayerGroup(step_x=diagonalStep, step_y=diagonalStep)
                elif _keys[SAVED_DATA.PLAYER_WALK_UP_KEY_ID]:
                    logger.debug("Player currently walking right && up")
                    self.movePlayerGroup(step_x=diagonalStep, step_y=-diagonalStep)
                else:
                    logger.debug("Player currently walking right")

                    self.movePlayerGroup(step_x=nonDiagonalStep, step_y=noStep)
            elif _keys[SAVED_DATA.PLAYER_WALK_LEFT_KEY_ID]:
                if _keys[SAVED_DATA.PLAYER_WALK_DOWN_KEY_ID]:
                    self.movePlayerGroup(step_x=-diagonalStep, step_y=diagonalStep)
                elif _keys[SAVED_DATA.PLAYER_WALK_UP_KEY_ID]:
                    self.movePlayerGroup(step_x=-diagonalStep, step_y=-diagonalStep)
                else:
                    logger.debug("Player currently walking left")
                    self.movePlayerGroup(step_x=-nonDiagonalStep, step_y=noStep)
            elif _keys[SAVED_DATA.PLAYER_WALK_UP_KEY_ID]:
                self.movePlayerGroup(step_x= noStep, step_y= -nonDiagonalStep)
                logger.debug("Player currently walking up")
            elif _keys[SAVED_DATA.PLAYER_WALK_DOWN_KEY_ID]:
                self.movePlayerGroup(step_x= noStep, step_y= nonDiagonalStep)
                logger.debug("Player currently walking down")
            else:
                logger.debug("Player currently not moving")
                self.movementState = PossiblePlayerStates.NOT_MOVING

        handleWalkingInput(keys)

    def movePlayerGroup(self, step_x: float, step_y:float):
        for part in self.playerGroup:
            part.rect.x += step_x
            part.rect.y += step_y

    def update(self, screen):
        Player.render(self.playerGroup, screen=screen)
        try:
            self.handleInput()
        except Exception as e:
            logger.errorg(f"Could not handle player input. Error: {e}")
