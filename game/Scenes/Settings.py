from game.Scenes.BaseScene import Scene, SceneStates,SceneTypes
import pygame
import gamedata.Save.SavedData as SAVED_DATA
from game.utils.Button import TextButton

class Settings(Scene):
    def __init__(self, pause_menu_last_frame: pygame.Surface, last_area_frame: pygame.Surface, screen_size: tuple):
        super().__init__(name = SceneTypes.SETTINGS)
        self.state = SceneStates.ON_ANIMATION
        self.animatingSceneIn = True
        self.pauseMenuLastFrame = pause_menu_last_frame
        self.lastAreaFrame = last_area_frame
        size = 48
        self.settingsSurface = Settings.loadFontSurface("SETTINGS", size, (20, 52, 164), True)
        self.settingsSurface.set_alpha(0)
        self.settingsSurfaceOutline = Settings.loadFontSurface("SETTINGS", size, (0, 150, 255), True)
        self.settingsSurfaceOutline.set_alpha(0)
        self.settingsSurfacePosition = (screen_size[0] / 2 - self.settingsSurface.get_width()/2, 0)
        self.animatingSceneOut = False
        self.blackBackground = pygame.Surface(screen_size, pygame.SRCALPHA)
        self.blackBackground.fill((0,0,0,200))
        self.mainButtons = Settings.loadButtons(screen_size)
    def clear(self):
        pass

    @staticmethod
    def loadButtons(screen_size: tuple):
        settingsButtonColor = (20, 30, 200)
        fontButton = TextButton("FONT", "font button", x= 48, y = screen_size[1] /4, width = 3*48, height = 2*48, fit_to_text = True, color = settingsButtonColor)
        screenSizeButton = TextButton("SCREEN SIZE", "screen size button", x= 48, y = 2 * screen_size[1] / 4, width = 3*48, height = 2*48, fit_to_text = True, color = settingsButtonColor)
        backToMenuButton = TextButton("BACK TO MENU", "back to menu button", x= 48, y= 3 * screen_size[1]/4, width= 3 * 48, height = 2 * 48, fit_to_text = True, color=(136,8,8))
        return [fontButton, screenSizeButton, backToMenuButton]



    def update(self, screen: pygame.Surface):
        screen.blit(self.lastAreaFrame, (0,0))
        screen.blit(self.blackBackground, (0,0))
        if self.state == SceneStates.ON_ANIMATION: self.animate(screen)
        screen.blit(self.settingsSurfaceOutline, (self.settingsSurfacePosition[0]-2, self.settingsSurfacePosition[1]))
        screen.blit(self.settingsSurfaceOutline, (self.settingsSurfacePosition[0]+2, self.settingsSurfacePosition[1]))
        screen.blit(self.settingsSurfaceOutline, (self.settingsSurfacePosition[0], self.settingsSurfacePosition[1]-2))
        screen.blit(self.settingsSurfaceOutline, (self.settingsSurfacePosition[0], self.settingsSurfacePosition[1]+ 2))
        screen.blit(self.settingsSurface, self.settingsSurfacePosition)
        for button in self.mainButtons: button.update(screen)
        self.checkSceneState()


    @staticmethod
    def loadFontSurface(string: str, size=24, color= (255,255,255), anti_aliasing= False):
        return Settings.turnStringToFontSurf(string, SAVED_DATA.FONT_PATH,size, color, anti_aliasing)

    @staticmethod
    def turnStringToFontSurf(string: str, font_fp: str, base_size=24,  color= (255,255,255), anti_aliasing = False):        
        return pygame.font.Font(font_fp, base_size).render(string, anti_aliasing, color)


    def animate(self, screen):
        if self.animatingSceneIn:
            self.animateSceneIn(screen, self.pauseMenuLastFrame)
        if self.animatingSceneOut:
            self.animateSceneOut(screen, self.pauseMenuLastFrame)

    def animateSceneIn(self, screen: pygame.Surface, pause_menu_last_frame: pygame.Surface):
        opacityStep = 5
        if pause_menu_last_frame.get_alpha() - opacityStep <= 0: 
            pause_menu_last_frame.set_alpha(0)
            self.settingsSurface.set_alpha(255)
            screen.blit(self.pauseMenuLastFrame, (0,0))
            self.animatingSceneIn = False
            self.state = SceneStates.RUNNING
            return None
        pause_menu_last_frame.set_alpha(pause_menu_last_frame.get_alpha() - opacityStep)
        self.settingsSurface.set_alpha(self.settingsSurface.get_alpha() + opacityStep)
        self.settingsSurfaceOutline.set_alpha(self.settingsSurface.get_alpha() + opacityStep)

        screen.blit(self.pauseMenuLastFrame, (0,0))

    def animateSceneOut(self, screen: pygame.Surface, pause_menu_last_frame: pygame.Surface):
        opacityStep = 5
        if pause_menu_last_frame.get_alpha() + opacityStep >= 255:
            pause_menu_last_frame.set_alpha(255)
            self.settingsSurface.set_alpha(0)
            screen.blit(self.pauseMenuLastFrame, (0,0))
            self.animatingSceneOut = False
            self.state = SceneStates.FINISHED
            return None
        self.settingsSurfaceOutline.set_alpha(self.settingsSurfaceOutline.get_alpha() - opacityStep)
        self.settingsSurface.set_alpha(self.settingsSurface.get_alpha() - opacityStep)
        pause_menu_last_frame.set_alpha(pause_menu_last_frame.get_alpha() + opacityStep)

        screen.blit(self.pauseMenuLastFrame, (0,0))
    def checkSceneState(self):
        if self.state != SceneStates.RUNNING: return None
        keys = pygame.key.get_pressed()
        if keys[pygame.K_f]:
            self.state = SceneStates.ON_ANIMATION
            self.animatingSceneOut = True
            self.ptrNextScene = SceneTypes.PAUSE_MENU 
