from game.Scenes.BaseScene import Scene, SceneStates,SceneTypes
import pygame
import gamedata.Save.SavedData as SAVED_DATA
import globalVars.SettingsConstants as SETTINGS
import Font.FontPaths as FONT_PATHS
from game.utils.Button import TextButton
from game.Scenes.Menu import Menu
import importlib

class PossibleSubMenus:
    NONE = "NONE"
    FONT = "FONT"
    SCREEN_SIZE = "SCREEN_SIZE"


class Settings(Menu):
    def __init__(self, pause_menu_last_frame: pygame.Surface, last_area_frame: pygame.Surface, screen_size: tuple):
        self.screenSizeButtonId = 0
        self.fontButtonId = 0
        self.backToMenuButtonId = 0
        super().__init__(name= SceneTypes.SETTINGS,last_area_frame = last_area_frame, last_scene_frame= pause_menu_last_frame, main_buttons = self.generateMainButtons(screen_size))
        self.settingsFontOutline = self.turnStringToFontSurf(string= "SETTINGS", font_fp = SAVED_DATA.FONT_PATH, base_size = SETTINGS.TILE_SIZE, anti_aliasing= True, color= (0, 150, 255))
        self.settingsFont = self.turnStringToFontSurf(string = "SETTINGS", font_fp = SAVED_DATA.FONT_PATH, base_size = SETTINGS.TILE_SIZE, anti_aliasing = True, color= (20, 52, 164)) 
        #self.settingsFontPos = (SETTINGS.SCREEN_WIDTH/2 - self.pausedFont.get_width() / 2, 0)
        fontPos = (SETTINGS.SCREEN_WIDTH/2 - self.settingsFont.get_width()/2, 0)
        self.addSurface(self.settingsFontOutline, (fontPos[0], fontPos[1] + 2))
        self.addSurface(self.settingsFontOutline, (fontPos[0] - 2, fontPos[1]))
        self.addSurface(self.settingsFontOutline, (fontPos[0] + 2, fontPos[1]))
        self.addSurface(self.settingsFontOutline, (fontPos[0], fontPos[1] - 2))
        self.addSurface(self.settingsFont, fontPos)

    def update(self, screen: pygame.Surface):
        super().update(screen)
        self.checkButtonPressed(self.buttonPressedName, screen)
        self.checkExitSignal() 

    def checkExitSignal(self):
        if self.uiLock: return None
        if self.state != SceneStates.RUNNING: return None 
        exitKey = pygame.K_f
        keys = pygame.key.get_pressed()
        if keys[exitKey]:
            for column in self.mainButtons: 
                for button in column:
                    button.setSelected(False)
                    button.setPressed(False)
                    button.disableMouse()
            self.uiLock = True
            self.state = SceneStates.FINISHING
            self.ptrNextScene = SceneTypes.PAUSE_MENU
            self.animation = Menu.animations[2]

    def updateFont(self):
        self.settingsFontOutline = self.turnStringToFontSurf(string= "SETTINGS", font_fp = SAVED_DATA.FONT_PATH, base_size = SETTINGS.TILE_SIZE, anti_aliasing= True, color= (0, 150, 255))
        self.settingsFont = self.turnStringToFontSurf(string = "SETTINGS", font_fp = SAVED_DATA.FONT_PATH, base_size = SETTINGS.TILE_SIZE, anti_aliasing = True, color= (20, 52, 164)) 
        fontPos = (SETTINGS.SCREEN_WIDTH/2 - self.settingsFont.get_width()/2, 0)
        self.surface = []
        self.clearSurfaces()
        self.addSurface(self.settingsFontOutline, (fontPos[0], fontPos[1] + 2))
        self.addSurface(self.settingsFontOutline, (fontPos[0] - 2, fontPos[1]))
        self.addSurface(self.settingsFontOutline, (fontPos[0] + 2, fontPos[1]))
        self.addSurface(self.settingsFontOutline, (fontPos[0], fontPos[1] - 2))
        self.addSurface(self.settingsFont, fontPos)
        for column in self.mainButtons:
            for button in column:
                button.textSurface = button.loadFontSurface(button.text, button.fontSize, button.textColor) 
                button.fontPath = SAVED_DATA.FONT_PATH

    def checkButtonPressed(self, name: str, screen: pygame.Surface):
        if name == "NONE": return None
        saveDataSignal = False
        parentButton = self.getSelectedButton()
        match name:
            case "BACK_TO_MENU":
                for col in self.mainButtons: 

                    for button in col: 
                        button.setSelected(False)
                        button.setPressed(False)
                        button.disableMouse()
                self.uiLock = True
                self.state = SceneStates.FINISHING
                self.ptrNextScene = SceneTypes.PAUSE_MENU
                self.animation = Menu.animations[2]
                self.buttonPressedName = "NONE"
            case "FONT":
                self.fadeOutUnselectedButtons(self.selectedButtonIdx)
                self.focusOnSubMenu(Settings.generateSubButtons(parent_button = parentButton, screen_size= screen.get_size()))
                self.buttonPressedName = "NONE"

            case "SCREEN_SIZE":
                self.fadeOutUnselectedButtons(self.selectedButtonIdx)
                self.focusOnSubMenu(Settings.generateSubButtons(parent_button = parentButton, screen_size= screen.get_size()))
                self.buttonPressedName = "NONE"
            case "FONT.1":
                SAVED_DATA.FONT = "GOHU"
                SAVED_DATA.FONT_PATH = FONT_PATHS.GOHU
                self.updateFont()
                saveDataSignal = True
            case "FONT.2":
                SAVED_DATA.FONT = "AGAVE"
                SAVED_DATA.FONT_PATH = FONT_PATHS.AGAVE
                self.updateFont()
                saveDataSignal = True
            case "FONT.3": 
                SAVED_DATA.FONT = "ANONYMICE_PRO"
                SAVED_DATA.FONT_PATH = FONT_PATHS.ANONYMICE_PRO
                self.updateFont()
                saveDataSignal = True
            case "FONT.4": 
                SAVED_DATA.FONT = "CASKAYDIA"
                SAVED_DATA.FONT_PATH = FONT_PATHS.CASKAYDIA
                self.updateFont()
                saveDataSignal = True
            case "FONT.5": 
                SAVED_DATA.FONT = "FIRA_CODE"
                SAVED_DATA.FONT_PATH = FONT_PATHS.FIRA_CODE
                self.updateFont()
                saveDataSignal = True
            case "FONT.6":
                SAVED_DATA.FONT = "MONOFUR"
                SAVED_DATA.FONT_PATH = FONT_PATHS.MONOFUR
                self.updateFont()
                saveDataSignal = True
            case "SCREEN_SIZE.SMALL": 
                function = importlib.import_module("game.utils.SettingsFunctions")
                displaySize = SETTINGS.SCREEN_RESOLUTION 
                SETTINGS.SCREEN = function.generateScreenFromResolution(displaySize[0], displaySize[1], "SMALL")
                self.buttonPressedName = "NONE"
                SAVED_DATA.SCREEN_SIZE = "SMALL"
                saveDataSignal = True
            case "SCREEN_SIZE.MEDIUM": 
                function = importlib.import_module("game.utils.SettingsFunctions")
                displaySize = SETTINGS.SCREEN_RESOLUTION 
                SETTINGS.SCREEN = function.generateScreenFromResolution(displaySize[0], displaySize[1], "MEDIUM")
                self.buttonPressedName = "NONE"
                SAVED_DATA.SCREEN_SIZE = "MEDIUM"
                saveDataSignal = True
            case "SCREEN_SIZE.LARGE": 
                function = importlib.import_module("game.utils.SettingsFunctions")
                displaySize = SETTINGS.SCREEN_RESOLUTION 
                SETTINGS.SCREEN = function.generateScreenFromResolution(displaySize[0], displaySize[1], "LARGE")
                self.buttonPressedName = "NONE"
                SAVED_DATA.SCREEN_SIZE = "LARGE"
                saveDataSignal = True
            case "SCREEN_SIZE.FULLSCREEN":
                function = importlib.import_module("game.utils.SettingsFunctions")
                displaySize = SETTINGS.SCREEN_RESOLUTION 
                SETTINGS.SCREEN = function.generateScreenFromResolution(displaySize[0], displaySize[1], "FULLSCREEN")
                self.buttonPressedName = "NONE"
                SAVED_DATA.SCREEN_SIZE = "FULLSCREEN"
                saveDataSignal = True
            case "FONT.BACK":
                self.focusOffSubMenu() 
                self.fadeAllButtons(resulting_opacity = 255)
                self.buttonPressedName = "NONE"
            case "SCREEN_SIZE.BACK":
                self.focusOffSubMenu() 
                self.fadeAllButtons(resulting_opacity = 255)
                self.buttonPressedName = "NONE"
        if saveDataSignal:
            function = importlib.import_module("game.utils.SettingsFunctions")
            function.saveSettingsFile()

    @staticmethod
    def generateSubButtons(parent_button: TextButton, screen_size: tuple) -> list:
        name = parent_button.getName()
        #rect = top_button.getRect()
        yValue = 0 
        xValue= screen_size[0] / 2 
        subButtonColor = (100, 149, 207)
        subButtonOutlineColor = (240, 255, 255)
        backButtonColor = (215, 43, 23)


        def setButtonsPos(buttons: list[list[TextButton]], starting_x, x_step, starting_y, y_step, rect_y_at_center= False, rect_x_at_center=False, screen_height=0, screen_width = 0):
            if rect_y_at_center: 
                subMenuHeight = 0
                rectWidth = 0
                sumButtonHeights = 0
                for column in buttons: 
                    for button in column: sumButtonHeights += button.getHeight() + y_step/2
                for column in buttons: 
                    for button in column:
                        subMenuHeight += button.getHeight() + y_step/2 
                        rectWidth = max(rectWidth, button.getWidth())
                    subMenuHeight -= y_step/2
                    starting_y = screen_height/2 - subMenuHeight/2
            for column in buttons:
                for button in column:
                    button.setY(starting_y)
                    button.setX(starting_x - button.getWidth()/2)
                    starting_y += y_step
                    starting_x += x_step

        def setButtonsOutline(buttons: list[list[TextButton]], color: tuple[int,int,int], name):
            for column in buttons:
                for button in column:
                    if button.getName() != name + ".BACK": 
                        button.animateTextWithOutline(color= color)
                        continue
                    button.animateTextWithOutline(color = (250, 128, 114))
        match name:
            case "SCREEN_SIZE":
                smallButton = TextButton("SMALL", name + ".SMALL", xValue, yValue, 0, 0, fit_to_text = True, color= subButtonColor, font_path = SAVED_DATA.FONT_PATH)
                mediumButton = TextButton("MEDIUM", name + ".MEDIUM", xValue, yValue, 0, 0, fit_to_text = True, color = subButtonColor, font_path = SAVED_DATA.FONT_PATH)
                largeButton = TextButton("LARGE", name + ".LARGE", xValue, yValue, 0, 0, fit_to_text = True, color = subButtonColor, font_path = SAVED_DATA.FONT_PATH)
                fullscreenButton = TextButton("FULLSCREEN", name + ".FULLSCREEN", xValue, yValue, 0, 0, fit_to_text = True, color= subButtonColor, font_path = SAVED_DATA.FONT_PATH)
                backButton = TextButton("BACK", name + ".BACK", xValue, yValue, 0, 0, fit_to_text=True, color= backButtonColor, font_path = SAVED_DATA.FONT_PATH)
                buttons = [[smallButton, mediumButton, largeButton, fullscreenButton, backButton]]
                setButtonsPos(buttons, starting_x = xValue , x_step = 0, starting_y = 0, rect_y_at_center = True, y_step = 2 * buttons[0][0].getHeight(), screen_height = screen_size[1])
                setButtonsOutline(buttons, subButtonOutlineColor, name)

                return buttons 
            case "FONT":
                font1Button = TextButton("FONT 1", name + ".1", xValue, yValue, 0, 0, fit_to_text = True, color= subButtonColor, font_path = FONT_PATHS.GOHU)
                font1Button.setX(xValue - font1Button.getWidth()/2)
                yValue += 2 * font1Button.getHeight()
                font2Button = TextButton("FONT 2", name + ".2", xValue, yValue, 0, 0, fit_to_text = True, color=subButtonColor, font_path = FONT_PATHS.AGAVE)
                font2Button.setX(xValue - font2Button.getWidth()/2)
                yValue += 2 * font2Button.getHeight()
                font3Button = TextButton("FONT 3", name + ".3", xValue, yValue, 0, 0, fit_to_text = True, color= subButtonColor, font_path = FONT_PATHS.ANONYMICE_PRO)
                font3Button.setX(xValue - font3Button.getWidth()/2)
                yValue += 2 * font3Button.getHeight()
                font4Button = TextButton("FONT 4", name + ".4", xValue, yValue, 0, 0, fit_to_text = True, color= subButtonColor, font_path = FONT_PATHS.CASKAYDIA)
                font4Button.setX(xValue - font4Button.getWidth()/2)
                yValue += 2 * font4Button.getHeight()
                font5Button = TextButton("FONT 5", name + ".5", xValue, yValue, 0, 0, fit_to_text = True, color= subButtonColor, font_path = FONT_PATHS.FIRA_CODE)
                font5Button.setX(xValue - font5Button.getWidth()/2)
                yValue += 2 * font5Button.getHeight()
                font6Button = TextButton("FONT 6", name + ".6", xValue, yValue, 0, 0, fit_to_text = True, color= subButtonColor, font_path = FONT_PATHS.MONOFUR)
                font6Button.setX(xValue - font6Button.getWidth()/2)
                backButton = TextButton("BACK", name + ".BACK", xValue, yValue, 0, 0, fit_to_text=True, color= backButtonColor)
                buttons = [[font1Button, font2Button, font3Button, font4Button, font5Button, font6Button, backButton]]

                setButtonsPos(buttons, starting_x = xValue , x_step = 0, starting_y = 0, rect_y_at_center = True, y_step = 2 * buttons[0][0].getHeight(), screen_height = screen_size[1])
                setButtonsOutline(buttons, subButtonOutlineColor, name)

                return buttons 
            case _: return []

    def generateMainButtons(self, screen_size: tuple):
        settingsButtonColor = (20, 30, 200)
        settingsButtonColorOutline = (100, 130, 215)
        backToMenuButtonColor = 136, 8, 8
        backToMenuButtonColorOutline = (255, 0, 0)
        fontButton = TextButton("FONT", "FONT", x= 48, y = screen_size[1] /4, width = 3*48, height = 2*48, fit_to_text = True, color = settingsButtonColor, font_path = SAVED_DATA.FONT_PATH)
        screenSizeButton = TextButton("SCREEN SIZE", "SCREEN_SIZE", x= 48, y = 2 * screen_size[1] / 4, width = 3*48, height = 2*48, fit_to_text = True, color = settingsButtonColor, font_path = SAVED_DATA.FONT_PATH)
        backToMenuButton = TextButton("BACK TO MENU", "BACK_TO_MENU", x= 48, y= 3 * screen_size[1]/4, width= 3 * 48, height = 2 * 48, fit_to_text = True, color=backToMenuButtonColor, font_path = SAVED_DATA.FONT_PATH)
        screenSizeButton.animateTextWithOutline(settingsButtonColorOutline)
        fontButton.animateTextWithOutline(settingsButtonColorOutline)
        backToMenuButton.animateTextWithOutline(backToMenuButtonColorOutline)
        self.fontButtonId = 0
        self.screenSizeButtonId = 1
        self.backToMenuButtonId = 2
        return [[fontButton, screenSizeButton, backToMenuButton]]

