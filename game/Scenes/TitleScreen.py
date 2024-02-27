from game.Scenes.BaseScene import Scene
from game.utils.Button import ImagedButton
from game.utils.Camera import Camera
from game.utils.Button import ImagedButton
import globalVars.SettingsConstants as globalVars
import globalVars.PathConstants as PATH_CONSTANTS
import globalVars.SceneConstants as SCENE_CONSTANTS
import pygame
import os

class TitleScreen(Scene):
    def __init__(self, background : pygame.Surface):
        self.state = SCENE_CONSTANTS.STATE_INITIALIZING
        self.background = background
        playButtonDir = os.getcwd() + "/images/test/playbutton.png"
        playButton = ImagedButton(name=SCENE_CONSTANTS.PLAY_BUTTON_NAME,image=playButtonDir)
        self.currentButtons = [playButton]
        pass

    def update(self, screen: pygame.Surface):

        self.render(screen=screen)
        self.state = self.checkFinished(buttons=self.visibleButtons)

    def render(self, screen: pygame.Surface):
        screen.blit(self.background, (globalVars.SCREEN_WIDTH/2, globalVars.SCREEN_HEIGHT/2))
        for button in self.currentButtons:
            button.update(screen=screen)
        self.checkFinished(buttons=self.currentButtons)

    def checkFinished(self, buttons : list[ImagedButton]):
        state = SCENE_CONSTANTS.STATE_RUNNING
        for button in buttons:
            if not button.name == SCENE_CONSTANTS.PLAY_BUTTON_NAME:
                continue
            if not button.pressed:
                continue
            state = SCENE_CONSTANTS.STATE_FINISHED

        return state

    def clearScene(self):
        pass