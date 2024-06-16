import pygame
from debug.logger import logger
import globalVars.SettingsConstants as SETTINGS

class ImagedButton:
    def __init__(self, name: str, image: pygame.Surface, x: int, y: int, toggle=False, starting_value=False):
        self.name = name;
        self.pressed = starting_value;
        self.toggle = toggle;
        self.image = image
        self.rect = self.image.get_rect(topleft= (x,y))
        
        self.width = self.rect.width
        self.height = self.rect.height
        self.hover = False;
        self.scaledRect = None
        self.scale()
        

    def scale(self):
        currentSurface = pygame.display.get_surface()
        windowWidth = currentSurface.get_width()
        windowHeight = currentSurface.get_height()
        defaultWidth = SETTINGS.SCREEN_WIDTH
        defaultHeight = SETTINGS.SCREEN_HEIGHT
        scaleProportion = windowWidth/defaultWidth, windowHeight/defaultHeight
        image = self.image.copy()
        image = pygame.transform.scale_by(image, (scaleProportion))
        self.scaledRect = image.get_rect(topleft= self.rect.topleft)
        self.scaledRect.x*= scaleProportion[0]
        self.scaledRect.y *= scaleProportion[1]

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
        if mouse_press[0]:  # element 0 is left click
            logger.debug(f"Button {self.name=}")

            return True;
        return None

    def update(self, screen: pygame.Surface):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        if not self.checkMouseInRange(mouse_pos=pygame.mouse.get_pos(), button_x=self.scaledRect.x, button_y=self.scaledRect.y,
                                      button_width=self.scaledRect.width, button_height=self.scaledRect.height):
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
        
