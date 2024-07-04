import pygame
import globalVars.SettingsConstants as SETTINGS
from debug.logger import logger
import Font.FontPaths as FONT_PATHS

class ButtonStates:
    NEUTRAL = "NEUTRAL"
    ON_ANIMATION = "ON_ANIMATION"
    ALL_STATES = [NEUTRAL, ON_ANIMATION]

class Button:
    def __init__(self, name: str, x: int, y: int, width, height, toggle=False, starting_value= False):
        self.name = name
        self.pressed = starting_value
        self.selected = False
        self.toggle = toggle
        self.rect = pygame.Rect(x, y, width, height)
        self.scaledRect = self.scaleRectToCurrentSurface(self.rect)
        self.hover = False 
        self.mouseEnabled = True
        self.clickEnabled = True
        self.state = ButtonStates.NEUTRAL
    def getState(self): return self.state
    def setState(self, state: str):
        if state not in ButtonStates.ALL_STATES: 
            return None
        self.state = state
    def getName(self): return self.name
    def getPressed(self): return self.pressed
    def getClickEnabled(self): return self.clickEnabled
    def setClickEnabled(self, click_enabled: bool): self.clickEnabled = click_enabled
    def setPressed(self, pressed: bool): self.pressed = pressed
    def togglePressed(self): self.pressed = not self.pressed
    def setSelected(self, selected: bool): self.selected = selected
    def getHover(self): return self.hover
    def getRect(self): return self.rect
    def getMouseEnabled(self): return self.mouseEnabled
    def disableMouse(self): self.mouseEnabled = False
    def enableMouse(self): self.mouseEnabled = True
    def setHover(self, hover: bool): self.hover = hover 

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
        if not self.mouseEnabled: return None
        if not self.checkMouseInRange(mouse_pos=pygame.mouse.get_pos(), button_x=self.scaledRect.x, button_y=self.scaledRect.y, button_width=self.scaledRect.width, button_height=self.scaledRect.height):
            self.hover = False
            return None
        self.hover = True
        if not self.clickEnabled: return None
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

class TextAnimationInfo:
    def __init__(self, is_scaling = False, shrink=False, scale_step=1, size_on_scale_finished=30, outline= False, outline_size = "small", outline_color= (255, 255, 0), color_shifting= False, color_shifting_speed="slow", color= (0, 0, 0), min_scaled_size=20):
        self.maxScaledSize = size_on_scale_finished
        self.minScaledSize = min_scaled_size
        self.scaleStep = scale_step
        self.scale = is_scaling
        self.shrink= shrink
        self.outlineColor = outline_color
        self.outline = outline
        self.outlineFactor = 0
        self.outlineSize = outline_size
        self.colorShiftingSpeed = color_shifting_speed
        self.colorShift = color_shifting
        self.colorShiftColor = color
        self.lerpRGBStep = 0.1
        self.lerpRGBValue = 0
        self.validLerpSpeeds = ["very slow, slow, medium, fast, very fast"]
    def setOutline(self, outline: bool): self.outline = outline
    def getOutline(self): return self.outline
    def setOutlineColor(self, outline_color: tuple[int, int, int]): self.outlineColor = outline_color
    def getOutlineColor(self): return self.outlineColor
    def setOutlineSize(self, size: str):
        validOutlineSizes = ["small", "medium", "large"]
        if size not in validOutlineSizes: 
            return None
        self.outlineSize = size
        match size:
            case "small":
                self.outlineFactor = 1
            case "medium":
                self.outlineFactor = 2
            case "big":
                self.outlineFactor = 3
    def getOutlineFactor(self): return self.outlineFactor
    def getOutlineSize(self): return self.outlineSize
    def setScale(self, scale: bool): self.scale= scale
    def getScale(self): return self.scale
    def setScaleStep(self, scale_step: int): self.scaleStep = scale_step
    def getScaleStep(self): return self.scaleStep
    def setMaxScaledSize(self, max_scaled_size: int): self.maxScaledSize = max_scaled_size
    def getMaxScaledSize(self): return self.maxScaledSize
    def setMinScaledSize(self, min_scaled_size: int): self.minScaledSize= min_scaled_size
    def getMinScaledSize(self): return self.minScaledSize
    def setShrink(self, shrink: bool): self.shrink= shrink
    def getShrink(self): return self.shrink
    def setColorShift(self, color_shift: bool): self.colorShift = color_shift
    def getColorShift(self): return self.colorShift
    def setColorShiftColor(self, color: tuple[int, int, int]): self.colorShiftColor = color
    def getColorShiftColor(self): return self.colorShiftColor
    def setColorShiftingSpeed(self, color_shifting_speed: str):
        if not color_shifting_speed in self.validLerpSpeeds:
            self.colorShiftingSpeed = color_shifting_speed = "medium"
        else: self.colorShiftingSpeed = color_shifting_speed
        match color_shifting_speed:
            case "very slow": self.lerpRGBStep = 0.05
            case "slow": self.lerpRGBStep = 0.1
            case "medium": self.lerpRGBStep = 0.25
            case "fast":  self.lerpRGBStep = 0.5
            case "very fast": self.lerpRGBStep = 1
    def getColorShiftingSpeed(self): return self.colorShiftingSpeed
    def setLerpRGBValue(self, lerp_rgb_value: float): self.lerpRGBValue = lerp_rgb_value
    def getLerpRGBValue(self): return self.lerpRGBValue
    def setLerpRGBStep(self, lerp_rgb_step: float): self.lerpRGBStep = lerp_rgb_step
    def getLerpRGBStep(self): return self.lerpRGBStep



class TextButton(Button):
    def __init__(self, text: str, name: str, x, y, width, height, fit_to_text= False, toggle= False, starting_value= False, background = "NONE", mouseEnabled= True, color = (255,255,255), font_path = FONT_PATHS.GOHU):
        super().__init__(name= name, x= x, y= y, width= width, height= height, toggle= toggle, starting_value= starting_value)
        self.fontPath = font_path
        self.textAlignment = TextAlignments.TOP_LEFT
        self.text = text
        self.fontSize = self.originalFontSize = self.lastFontSize =  30
        self.textColor = self.originalTextColor = self.lastTextColor = color
        self.textSurface = self.loadFontSurface(text, self.fontSize, self.textColor) 
        self.textSurfaceOutline = None
        self.textSurfaceAlpha = 255
        self.textSurfaceOutlineAlpha = 255
        self.originalOutlineColor = None

        self.outlineColor = None
        self.textPosition = TextButton.loadTextPosition(self.rect, self.textSurface, self.textAlignment)
        self.textPositionOutline = self.textPosition
        if fit_to_text:
            self.textAlignment = TextAlignments.CENTER_LEFT
            self.changeRect(self.textSurface.get_rect(topleft= self.textPosition))
        if not mouseEnabled: self.disableMouse()
        self.backgroundColor = TextButton.loadBackgroundColor(background)
        self.textAnimationInfo = TextAnimationInfo()

    def setFont(self, font: str):
        match font:
            case "GOHU":
                self.fontPath = FONT_PATHS.GOHU
            case "FIRA_CODE":
                self.fontPath = FONT_PATHS.FIRA_CODE
            case "MONOFUR":
                self.fontPath = FONT_PATHS.MONOFUR
            case "CASKAYDIA":
                self.fontPath = FONT_PATHS.CASKAYDIA
            case "AGAVE":
                self.fontPath = FONT_PATHS.AGAVE
            case "ANONYMICE_PRO":
                self.fontPath = FONT_PATHS.ANONYMICE_PRO

            case _:
                self.fontPath = FONT_PATHS.GOHU


    def setFontPath(self, font_path: str):
        match font_path:
            case FONT_PATHS.GOHU:
                self.fontPath = FONT_PATHS.GOHU

            case FONT_PATHS.FIRA_CODE:
                self.fontPath = FONT_PATHS.FIRA_CODE

            case FONT_PATHS.MONOFUR:
                self.fontPath = FONT_PATHS.MONOFUR
            case FONT_PATHS.CASKAYDIA:
                self.fontPath = FONT_PATHS.CASKAYDIA
            case FONT_PATHS.AGAVE:
                self.fontPath = FONT_PATHS.AGAVE

            case FONT_PATHS.ANONYMICE_PRO:
                self.fontPath = FONT_PATHS.ANONYMICE_PRO

            case _:
                self.fontPath = FONT_PATHS.GOHU

    @staticmethod
    def loadBackgroundColor(background: str):
        match background:
            case "NONE":
                return None
            case "BLACK":
                return (0,0,0)
            case "WHITE":
                return (255,255,255)
            case "RED":
                return (255, 0, 0)
            case "GREEN":
                return (0, 255, 0)
            case "BLUE":
                return (0, 0, 255)
            case "PURPLE":
                return (255, 0, 255)
            case "YELLOW": return (255, 255, 0)
            case "TEAL": return (0, 255, 255)

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

    def setTextSurfaceAlpha(self, opacity: int):
        if opacity<0 or opacity > 255: opacity = 255
        self.textSurfaceAlpha = opacity

    def setTextSurfaceOutlineAlpha(self, opacity: int):
        if opacity < 0 or opacity > 255: opacity = 255
        if self.textSurfaceOutline is None: return None
        self.textSurfaceOutlineAlpha = opacity

    def setTextAlignment(self, alignment: str):
        if alignment not in TextAlignments.LIST:
            logger.debug(f"Could not change alignment for button with name {self.name}, invalid alignment argument.")
            return None
        self.textAlignment = alignment
        self.textPosition = TextButton.loadTextPosition(self.rect, self.textSurface, alignment) 
   
    @staticmethod
    def turnStringToFontSurf(string: str, font_fp: str, base_size=24,  color= (255,255,255), bold= False):        
        font = pygame.font.Font(font_fp, base_size)
        font.bold = bold
        return font.render(string, False, color)


    def loadFontSurface(self, text: str, size = 30, 
                        color = (255,255,255), bold= False):
        return TextButton.turnStringToFontSurf(text, self.fontPath, size, color, bold)
        
    def animateTextToSize(self, size: int, step: int, shrink: bool):
        self.lastFontSize = self.fontSize
        self.setState(ButtonStates.ON_ANIMATION)
        if shrink:
            self.textAnimationInfo.setMinScaledSize(size)
        else:
            self.textAnimationInfo.setMaxScaledSize(size)


        self.textAnimationInfo.setScaleStep(step)
        self.textAnimationInfo.setShrink(shrink)
        self.textAnimationInfo.setScale(True)


    def animateTextWithOutline(self, color=(255, 255, 0), size= "medium"):
        if self.originalOutlineColor is None: self.originalOutlineColor = color
        self.outlineColor = color
        self.setState(ButtonStates.ON_ANIMATION)
        self.textAnimationInfo.setOutline(True)
        self.textAnimationInfo.setOutlineColor(color)
        self.textAnimationInfo.setOutlineSize(size)

    def updateTextSurface(self):
        self.textSurface = self.loadFontSurface(self.text, self.fontSize, self.textColor) 

    def animateTextToOutline(self, color= (0, 255, 255), size= "medium", speed= "slow"):
        self.setState(ButtonStates.ON_ANIMATION)

    def removeTextOutline(self): 
        self.textAnimationInfo.setOutline(False)
        self.textSurfaceOutline = None

    def animateTextToColor(self, speed="slow", color= (0,0,0)):
        color = list(color)
        for i in range(len(color)):
            if not (color[i] > 255 or color[i] < 0): continue
            if color[i] > 255: 
                color[i] = 255
            elif color[i] < 0:
                color[i] = 0
        color = tuple(color)
        self.setState(ButtonStates.ON_ANIMATION)
        self.textAnimationInfo.setColorShift(True)
        self.textAnimationInfo.setColorShiftingSpeed(speed)
        self.textAnimationInfo.setColorShiftColor(color)

    def animate(self, animationInfo, state):
        if state != ButtonStates.ON_ANIMATION: return None
        if not (animationInfo.getScale() or animationInfo.getColorShift() or animationInfo.getOutline()): return None 
        ### Animation text size###
        if animationInfo.shrink:
            if self.fontSize <= animationInfo.getMinScaledSize():
                self.fontSize = animationInfo.getMinScaledSize()
                animationInfo.setScale(False)
                if animationInfo.getOutline():


                    self.textSurfaceOutline = self.loadFontSurface(self.text, self.fontSize, animationInfo.getOutlineColor())
        else:
            if self.fontSize >= animationInfo.getMaxScaledSize(): 
                self.fontSize = animationInfo.getMaxScaledSize() 
                animationInfo.setScale(False)
                if animationInfo.getOutline():
                    self.textSurfaceOutline = self.loadFontSurface(self.text, self.fontSize, animationInfo.getOutlineColor())
        if animationInfo.getScale():
            if animationInfo.shrink:
                self.fontSize -= animationInfo.getScaleStep()
            else:

                self.fontSize += animationInfo.getScaleStep() 
        if animationInfo.getColorShift():
            lerpRGBValue = animationInfo.getLerpRGBValue()
            if not lerpRGBValue >= 1:
                animationInfo.setLerpRGBValue(lerpRGBValue + animationInfo.getLerpRGBStep())
                red = self.lastTextColor[0] + (animationInfo.getColorShiftColor()[0] - self.lastTextColor[0]) * lerpRGBValue 
                green = self.lastTextColor[1] + (animationInfo.getColorShiftColor()[1] - self.lastTextColor[1]) * lerpRGBValue 
                blue = self.lastTextColor[2] + (animationInfo.getColorShiftColor()[2] - self.lastTextColor[2]) * lerpRGBValue 
                self.textColor = (red, green, blue)
            else:
                self.lastTextColor = animationInfo.getColorShiftColor()
                animationInfo.setColorShift(False)
                animationInfo.setLerpRGBValue(0)
        if animationInfo.getOutline():
            if self.textSurfaceOutline is None:
                self.textSurfaceOutline = self.loadFontSurface(self.text, self.fontSize, animationInfo.getOutlineColor())
                self.textPositionOutline = self.textPosition
            if animationInfo.getScale():
                self.textPositionOutline = self.textPosition
                self.textSurfaceOutline = self.loadFontSurface(self.text, self.fontSize, animationInfo.getOutlineColor())
        self.textSurface = self.loadFontSurface(self.text, self.fontSize, self.textColor) 
        if animationInfo.getScaleStep(): self.changeRect(self.textSurface.get_rect(topleft= self.textPosition))

    def update(self, screen: pygame.Surface):
        #if self.hover: self.backgroundColor = (255, 255, 255)
        #else: self.backgroundColor = (0, 0, 0)
        self.animate(animationInfo = self.textAnimationInfo, state= self.state)
        self.textSurface.set_alpha(self.textSurfaceAlpha)
        if self.backgroundColor: pygame.draw.rect(screen, self.backgroundColor, self.rect)
        if self.textSurfaceOutline is not None:
            self.textSurfaceOutline.set_alpha(self.textSurfaceOutlineAlpha)
            outlineFactor = self.textAnimationInfo.getOutlineFactor()
            screen.blit(self.textSurfaceOutline, (self.textPosition[0], self.textPosition[1] + outlineFactor))
            screen.blit(self.textSurfaceOutline, (self.textPosition[0], self.textPosition[1] - outlineFactor))
            screen.blit(self.textSurfaceOutline, (self.textPosition[0]+ outlineFactor, self.textPosition[1] ))
            screen.blit(self.textSurfaceOutline, (self.textPosition[0] - outlineFactor, self.textPosition[1] ))
        screen.blit(self.textSurface, self.textPosition)
        super().update(screen)

