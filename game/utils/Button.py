import pygame
import globalVars.SettingsConstants as GLOBAL_VARS
class ImagedButton:
    def __init__(self, image : pygame.Surface, x : int, y : int, toggle=False, starting_value=False):
        self.pressed = starting_value;
        self.toggle = toggle;
        self.image = image
        rect = self.image.get_rect()
        self.width = rect.width;
        self.height = rect.height
        self.hover = False;
        self.x = x - self.width/2;
        self.y = y - self.height/2;

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

    @staticmethod
    def checkClicked(mouse_press):
        if mouse_press[0]:  # element 0 is left click
            return True;
        return None

    def update(self):
        GLOBAL_VARS.SCREEN.blit(self.image, (self.x, self.y))
        if self.checkMouseInRange(mouse_pos=pygame.mouse.get_pos(), button_x=self.x, button_y=self.y,
                                  button_width=self.width, button_height=self.height):
            self.hover = True
            # print("mouse is in range!")
            if ImagedButton.checkClicked(mouse_press=pygame.mouse.get_pressed()):
                if not self.toggle:
                    self.pressed = True;
                    return None;
                if self.pressed == True:
                    self.pressed = False;
                    return None;
                else:
                    self.pressed = True;
        else:
            self.hover = False;