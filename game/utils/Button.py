import pygame
import globalVars.SettingsConstants as SETTINGS
from debug.logger import logger
import Font.FontPaths as FONT_PATHS

class Button:
    def __init__(self, name: str, x: int, y: int, width, height, toggle=False, starting_value= False):
        self.name = name
        self.pressed = starting_value
        self.toggle = toggle
        self.rect = pygame.Rect(x, y, width, height)
        self.scaledRect = self.scaleRectToCurrentSurface(self.rect)
        self.hover = False 
    def scaleRectToCurrentSurface(self, rect: pygame.Rect) -> pygame.Rect:
        currentSurface = pygame.display.get_surface()
        windowWidth = currentSurface.get_width()
        windowHeight = currentSurface.get_height()
        defaultWidth = SETTINGS.SCREEN_WIDTH
        defaultHeight = SETTINGS.SCREEN_HEIGHT
        scaleProportion = windowWidth/defaultWidth, windowHeight/defaultHeight
        rectCopy = rect.copy()
        scaledSurface = pygame.Surface((rectCopy.width, rectCopy.height))
        scaledSurface = pygame.transform.scale_by(scaledSurface, (scaleProportion))
        rectCopy = scaledSurface.get_rect()
        rectCopy.x, rectCopy.y = rect.x * scaleProportion[0], rect.y * scaleProportion[1]
        return rectCopy

    def changeRect(self, rect: pygame.Rect):
        self.rect = rect
        self.scaledRect = self.scaleRectToCurrentSurface(rect)

    def getScaledRect(self) -> pygame.Rect: return self.scaledRect

    def checkMouseInRange(self, mouse_pos, button_x, button_y, button_width, button_height):
        
        mousePosX = mouse_pos[0]
        mousePosY = mouse_pos[1]
        lowerXBound = button_x
        upperXBound = button_x + button_width
        lowerYBound = button_y
        upperYBound = button_y + button_height
        if lowerXBound > mousePosX or upperXBound < mousePosX:
            return None;
        if lowerYBound > mousePosY or upperYBound < mousePosY:
            return None;
        return True;

    def checkClicked(self, mouse_press):
        if mouse_press[0] and self.hover:  # element 0 is left click
            logger.debug(f"Button {self.name=}")

            return True;
        return None

    def update(self, screen: pygame.Surface):
        if not self.checkMouseInRange(mouse_pos=pygame.mouse.get_pos(), button_x=self.scaledRect.x, button_y=self.scaledRect.y, button_width=self.scaledRect.width, button_height=self.scaledRect.height):
            self.hover = False
            return None
        self.hover = True
        if self.checkClicked(mouse_press=pygame.mouse.get_pressed()):
            if not self.toggle:
                self.pressed = True;
                return None;
            if self.pressed:
                self.pressed = False;
                return None;
            else:
                self.pressed = True;
 

class ImagedButton(Button):
    def __init__(self, name: str, image: pygame.Surface, x: int, y: int, toggle=False, starting_value=False):
        super().__init__(name= name, x= x, y= y, width= image.get_width(), height= image.get_height(),toggle= toggle, starting_value= starting_value)
        self.image = image 
        
      
    def update(self, screen: pygame.Surface):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        super().update(screen)

class TextAlignments:
    TOP_LEFT = "TOP_LEFT"
    TOP_RIGHT = "TOP_RIGHT"
    TOP_MIDDLE = "TOP_MIDDLE"
    CENTER_LEFT = "CENTER_LEFT"
    CENTER_RIGHT = "CENTER_RIGHT"
    CENTER = "CENTER"
    BOTTOM_LEFT = "BOTTOM_LEFT"
    BOTTOM_RIGHT = "BOTTOM_RIGHT"
    BOTTOM_MIDDLE = "BOTTOM_MIDDLE"
    LIST = [
            TOP_LEFT, TOP_RIGHT, TOP_MIDDLE, CENTER_LEFT, CENTER_RIGHT, CENTER, BOTTOM_LEFT, BOTTOM_RIGHT, BOTTOM_MIDDLE
            ]

class TextButton(Button):
    def __init__(self, text: str, name: str, x, y, width, height, fit_to_text= False, toggle= False, starting_value= False, background = "NONE"):
        super().__init__(name= name, x= x, y= y, width= width, height= height, toggle= toggle, starting_value= starting_value)
        self.textAlignment = TextAlignments.CENTER
        self.textSurface = TextButton.loadFontSurface(text) 
        self.textPosition = TextButton.loadTextPosition(self.rect, self.textSurface, self.textAlignment)
        if fit_to_text:
            self.textAlignment = TextAlignments.CENTER_LEFT
            self.changeRect(self.textSurface.get_rect(topleft= self.textPosition))
        self.backgroundColor = TextButton.loadBackgroundColor(background)
        
    @staticmethod
    def loadBackgroundColor(background: str): 
        return (0, 0, 0)

    @staticmethod
    def loadTextPosition(rect: pygame.Rect, text_surface: pygame.Surface, alignment: str):
        if alignment not in TextAlignments.LIST:
            logger.debug(f"Could not load text position, invalid alignment argument {alignment=}")
        match alignment:
            case TextAlignments.CENTER:
                return rect.center[0]  - text_surface.get_width()/2, rect.center[1] - text_surface.get_height()/2
            case TextAlignments.CENTER_LEFT:
                return rect.left, rect.center[1] - text_surface.get_height()/2
            case TextAlignments.CENTER_RIGHT:
                return rect.right - text_surface.get_width(), rect.center[1] - text_surface.get_height()/2
            case TextAlignments.TOP_MIDDLE:
                return rect.center[0] - text_surface.get_width()/2, rect.y
            case TextAlignments.TOP_LEFT:
                return rect.topleft
            case TextAlignments.TOP_RIGHT:
                return rect.topright[0] - text_surface.get_width(), rect.topright[1]
            case TextAlignments.BOTTOM_LEFT:
                return rect.bottomleft[0], rect.bottomleft[1] - text_surface.get_height()
            case TextAlignments.BOTTOM_MIDDLE:
                return rect.midbottom[0] - text_surface.get_width()/2, rect.midbottom[1] - text_surface.get_height() / 2
            case TextAlignments.BOTTOM_RIGHT:
                return rect.bottomright[0] - text_surface.get_width(), rect.bottomright[1]- text_surface.get_height()

    def setTextAlignment(self, alignment: str):
        if alignment not in TextAlignments.LIST:
            logger.debug(f"Could not change alignment for button with name {self.name}, invalid alignment argument.")
            return None
        self.textAlignment = alignment
        self.textPosition = TextButton.loadTextPosition(self.rect, self.textSurface, alignment) 
    @staticmethod
    def turnStringToFontSurf(string: str, font_fp: str, base_size=24,  color= (255,255,255)):        
        return pygame.font.Font(font_fp, base_size).render(string, False, color)


    @staticmethod
    def loadFontSurface(text: str, size = 30, color = (255,255,255)):
        fontPath = FONT_PATHS.GOHU
        return TextButton.turnStringToFontSurf(text, fontPath, size, color)
        

    def update(self, screen: pygame.Surface):
        if self.hover: self.backgroundColor = (255, 255, 255)
        else: self.backgroundColor = (0, 0, 0)


        pygame.draw.rect(screen, self.backgroundColor, self.rect)
        screen.blit(self.textSurface, self.textPosition)
        super().update(screen)

