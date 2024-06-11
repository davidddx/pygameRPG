from game.Scenes.BaseScene import Scene, SceneStates
from game.utils.ImagedButton import ImagedButton
import globalVars.SettingsConstants as SETTINGS
import pygame
import os

class TitleScreen(Scene):
    def __init__(self, background : pygame.Surface):
        self.playButtonName = playButtonName = "Play"
        self.state = SceneStates.INITIALIZING
        self.background = background
        image = pygame.image.load(os.getcwd() + "/images/test/playbutton.png")
        playButton = ImagedButton(name=playButtonName, image= image,
                                  x=int(SETTINGS.SCREEN_WIDTH/2 - image.get_width()/2), y= int(SETTINGS.SCREEN_HEIGHT/2 - image.get_height()/2))
        self.currentButtons = [playButton]


    def update(self, screen: pygame.Surface):

        self.render(screen=screen)
        self.state = self.checkFinished(buttons=self.currentButtons)

    def render(self, screen: pygame.Surface):
        screen.blit(self.background, (0, 0))
        for button in self.currentButtons:
            button.update(screen=screen)
        self.checkFinished(buttons=self.currentButtons)

    def checkFinished(self, buttons : list[ImagedButton]):
        state = SceneStates.RUNNING
        for button in buttons:
            if not button.name == self.playButtonName:

                continue
            if not button.pressed:
                continue
            state = SceneStates.FINISHED

        return state

    def clear(self):
        pass

    def getPlayButton(self):
        return self.currentButtons[0]

    def getState(self):
        return self.state
