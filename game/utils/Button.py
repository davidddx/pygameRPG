import pygame
import globalVars.SettingsConstants as SETTINGS
import game.utils.Misc as Misc
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
        self.description = ""
        self.state = ButtonStates.NEUTRAL

    def setDescription(self, description: str):
        self.description = description
    def getDescription(self):
        return self.description
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
    def setWidth(self, width): 
        rect = self.rect.copy()
        rect.width = width
        self.changeRect(rect)
    def setHeight(self, height):
        rect = self.rect.copy()
        rect.height = height
        self.changeRect(rect)
    def setDimensions(self, width, height):
        rect = self.rect.copy()
        rect.height = height
        rect.width = width
        self.changeRect(rect)
    def getWidth(self): return self.rect.width
    def getHeight(self): return self.rect.height
    def setY(self, yvalue):
        lastyValue = self.rect.y
        try:
            self.rect.y = yvalue
            self.scaleRectToCurrentSurface(self.rect)
        except Exception as e: 
            self.rect.y = lastyValue
            logger.error(f"could not set x value for button {self.name}, error: {e}")
    def setX(self, xvalue):
        lastxValue = self.rect.x
        try:
            self.rect.x = xvalue
            self.scaleRectToCurrentSurface(self.rect)
        except Exception as e: 
            self.rect.x = lastxValue
            logger.error(f"could not set x value for button {self.name}, error: {e}")

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
    def __init__(self, is_scaling = False, shrink=False, scale_step=1, size_on_scale_finished=30, outline= False, outline_size = "small", outline_color= (255, 255, 0), color_shifting= False, color_shifting_speed="slow", color= (0, 0, 0), min_scaled_size=20, is_xy_lerping=False, lerp_xy_pos = (0,0), lerp_xy_step = 0, is_xy_ellipse_interpolation = False, ellipse_interpolation_xy_size = 0, ellipse_interpolation_xy_direction = 0):
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
        self.colorShiftOutline = False
        self.colorShiftOutlineColor = False
        self.colorShiftingOutlineSpeed = False
        self.colorShiftOutlineLastColor = (0,0,0)
        self.lerpRGBStep = 0.1
        self.lerpRGBValue = 0
        self.lerpRGBOutlineStep = 0.1
        self.lerpRGBOutlineValue = 0
        self.lerpXYStep = lerp_xy_step
        self.lerpXYOriginalPos = lerp_xy_pos 
        self.lerpXYGoalPos = lerp_xy_pos 
        self.lerpXYCurrentPos = lerp_xy_pos
        self.lerpXY = is_xy_lerping
        self.givenLerpXYPositions = False
        self.lerpXYPositions = None 
        self.lerpXYIndex = 0
        self.lerpXYValue = 0
        self.ellipseInterpolationXY = is_xy_ellipse_interpolation
        self.ellipseInterpolationXYSize = ellipse_interpolation_xy_size 
        self.ellipseInterpolationXYDirection = ellipse_interpolation_xy_direction # x==0: not moving. x>=1: Clockwise, x<=-1: Counterclockwise
        self.alphaChanging = False 
        self.alphaGoal = 0
        self.lerpXYGoalPosIsMiddle = False
        self.alphaStep = 0
        self.validLerpSpeeds = ["very slow, slow, medium, fast, very fast"]
        self.finished = False

    def setLerpXYGoalPosIsMiddle(self, boolean: bool): self.lerpXYGoalPosIsMiddle = boolean
    def getLerpXYGoalPosIsMiddle(self): return self.lerpXYGoalPosIsMiddle 
    def getAlphaChanging(self): return self.alphaChanging
    def setAlphaChanging(self, alpha_changing: bool): self.alphaChanging = alpha_changing 
    def getAlphaGoal(self): return self.alphaGoal
    def setAlphaGoal(self, goal: int): self.alphaGoal = goal
    def getAlphaStep(self): return self.alphaStep
    def setAlphaStep(self, step): self.alphaStep = step
    def setLerpRGBOutlineValue(self, val): self.lerpRGBOutlineValue = val
    def getLerpRGBOutlineValue(self): return self.lerpRGBOutlineValue
    def setLerpRGBOutlineStep(self, step): self.lerpRGPOutlineStep = step
    def getLerpRGBOutlineStep(self): return self.lerpRGBOutlineStep
    def setColorShiftOutlineLastColor(self, color: tuple[int, int, int]):
        self.colorShiftOutlineLastColor = color
    def getColorShiftOutlineLastColor(self):
        return self.colorShiftOutlineLastColor
    def setLerpXYIndex(self, idx): self.lerpXYIndex = idx
    def getLerpXYIndex(self): return self.lerpXYIndex
    def setEllipseInterpolationXYDirection(self, direction: int): self.ellipseInterpolationXYDirection = direction
    def getEllipseInterpolationXYDirection(self): return self.ellipseInterpolationXYDirection
    def getEllipseInterpolationXYSize(self): return self.ellipseInterpolationXYSize
    def getEllipseInterpolationXY(self): return self.ellipseInterpolationXY
    def setEllipseInterpolationXY(self, val): self.ellipseInterpolationXY = val
    def setEllipseInterpolationXYSize(self, val: tuple[float | int]): self.ellipseInterpolationXYSize = val
    def setGivenLerpXYPositions(self, val: bool): self.givenLerpXYPositions = val 
    def setLerpXYPositions(self, val): self.lerpXYPositions = val
    def getGivenLerpXYPositions(self): return self.givenLerpXYPositions
    def setLerpXYValue(self, val): self.lerpXYValue = val
    def getLerpXYValue(self): return self.lerpXYValue
    def getLerpXYPositions(self): return self.lerpXYPositions
    def setLerpXYStep(self, lerp_xy_step: float | int): self.lerpXYStep = lerp_xy_step
    def getLerpXYStep(self): return self.lerpXYStep
    def setLerpXYOriginalPos(self, lerp_xy_original_pos: tuple[float | int]): self.lerpXYOriginalPos = lerp_xy_original_pos
    def setLerpXYCurrentPos(self, lerp_xy_pos: tuple[float | int]): self.lerpXYCurrentPos = lerp_xy_pos
    def setLerpXYGoalPos(self, lerp_xy_pos: tuple[float | int]): self.lerpXYGoalPos = lerp_xy_pos
    def getLerpXYOriginalPos(self): return self.lerpXYOriginalPos
    def getLerpXYGoalPos(self): return self.lerpXYGoalPos
    def getLerpXYCurrentPos(self): return self.lerpXYCurrentPos
    def getSlerpXY(self): return self.slerpXY
    def setLerpXY(self, lerp_xy: bool): self.lerpXY = lerp_xy
    def setSlerpXY(self, slerp_xy: bool): self.slerpXY = slerp_xy
    def setSlerpXYSize(self, size: int | float): self.slerpXYPathSize = size
    def getSlerpXYSize(self): return self.slerpXYPathSize
    def getLerpXY(self): return self.lerpXY
    def setFinished(self, finished): self.finished = finished
    def getFinished(self): return self.finished
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
    def setColorShiftOutline(self, color_shift: bool): self.colorShiftOutline = color_shift
    def getColorShiftOutline(self): return self.colorShiftOutline
    def setColorShiftOutlineColor(self, color: tuple[int, int, int]): self.colorShiftOutlineColor = color
    def getColorShiftOutlineColor(self): return self.colorShiftOutlineColor
    def setColorShiftingOutlineSpeed(self, color_shifting_speed: str):
        if not color_shifting_speed in self.validLerpSpeeds:
            self.colorShiftingSpeed = color_shifting_speed = "medium"
        else: self.colorShiftingSpeed = color_shifting_speed
        match color_shifting_speed:
            case "very slow": self.lerpRGBStepOutline = 0.05
            case "slow": self.lerpRGBStepOutline = 0.1
            case "medium": self.lerpRGBStepOutline = 0.25
            case "fast":  self.lerpRGBStepOutline = 0.5
            case "very fast": self.lerpRGBStepOutline = 1
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
        self.visible = True
        self.outlineColor = None
        self.textPosition = TextButton.loadTextPosition(self.rect, self.textSurface, self.textAlignment)
        self.textPositionOutline = self.textPosition
        if fit_to_text:
            self.textAlignment = TextAlignments.CENTER_LEFT
            self.changeRect(self.textSurface.get_rect(topleft= self.textPosition))
        if not mouseEnabled: self.disableMouse()
        self.backgroundColor = TextButton.loadBackgroundColor(background)
        self.textAnimationInfo = TextAnimationInfo()

    def updateAnimationToFinished(self):
        self.textAnimationInfo.setFinished(True)

    def setX(self, xvalue):
        super().setX(xvalue)
        self.textPosition = TextButton.loadTextPosition(self.rect, self.textSurface, self.textAlignment)
        self.textPositionOutline = self.textPosition
    def setY(self, yvalue):
        super().setY(yvalue)
        self.textPosition = TextButton.loadTextPosition(self.rect, self.textSurface, self.textAlignment)
        self.textPositionOutline = self.textPosition

    def getVisible(self): return self.visible
    def setVisible(self): self.visible = True
    def setInvisible(self): self.visible = False

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
        logger.debug(f"{self.textSurfaceOutline=}")
        #if self.textSurfaceOutline is None: return None
        self.textSurfaceOutlineAlpha = opacity

    def setTextAlignment(self, alignment: str):
        if alignment not in TextAlignments.LIST:
            logger.debug(f"Could not change alignment for button with name {self.name}, invalid alignment argument.")
            return None
        self.textAlignment = alignment
        self.textPosition = TextButton.loadTextPosition(self.rect, self.textSurface, alignment) 
   
    @staticmethod
    def turnStringToFontSurf(string: str, font_fp: str, base_size=24,  color= (255,255,255), bold= False):        
        font = pygame.font.Font(font_fp, int(base_size))
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

    def animateTextToAlpha(self, alpha, step=5):
        assert (step > 0 and alpha <= 255) or (step < 0 and alpha >= 0)
        assert (step >= -255 and step <= 255)
        self.setState(ButtonStates.ON_ANIMATION)
        self.textAnimationInfo.setAlphaChanging(True)
        self.textAnimationInfo.setAlphaStep(step)
        self.textAnimationInfo.setAlphaGoal(alpha)

    def updateTextSurface(self):
        self.textSurface = self.loadFontSurface(self.text, self.fontSize, self.textColor) 

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

    def animateTextOutlineToColor(self, speed="slow", lastColor = (0,0,0), color = (0,0,0)):
        color = list(color)
        for i in range(len(color)):
            if not (color[i] > 255 or color[i] < 0): continue
            if color[i] > 255: 
                color[i] = 255
            elif color[i] < 0:
                color[i] = 0
        color = tuple(color)
        self.setState(ButtonStates.ON_ANIMATION)
        self.textAnimationInfo.setColorShiftOutline(True)
        self.textAnimationInfo.setColorShiftingOutlineSpeed(speed)
        self.textAnimationInfo.setColorShiftOutlineColor(color)
        self.textAnimationInfo.setColorShiftOutlineLastColor(lastColor)

    def animateTextToPosition(self,goal_pos: tuple, current_pos: tuple, ellipse_interpolation= False, ellipse_size = (30,30), step=0.1, given_positions = False, positions = None, middle = False, num_steps = 0):
        self.setState(ButtonStates.ON_ANIMATION)
        if num_steps > 0 and type(num_steps) == int:
            step = 1/num_steps 
        self.textAnimationInfo.setLerpXY(True)
        self.textAnimationInfo.setLerpXYStep(step)
        self.textAnimationInfo.setLerpXYGoalPos(goal_pos)
        self.textAnimationInfo.setLerpXYGoalPosIsMiddle(middle)
        self.textAnimationInfo.setLerpXYCurrentPos(current_pos)
        self.textAnimationInfo.setLerpXYOriginalPos(current_pos)
        self.textAnimationInfo.setGivenLerpXYPositions(given_positions)
        self.textAnimationInfo.setLerpXYPositions(positions)
        self.textAnimationInfo.setEllipseInterpolationXY(ellipse_interpolation)
        self.textAnimationInfo.setEllipseInterpolationXYSize(ellipse_size)


    def animate(self, animationInfo, state):
        if state != ButtonStates.ON_ANIMATION: return None
        logger.debug(f"LERP XY: {animationInfo.getLerpXY()}")
        if not (animationInfo.getScale() or animationInfo.getColorShift() or animationInfo.getOutline() or animationInfo.getLerpXY() or animationInfo.getAlphaChanging()): return None 
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
        if animationInfo.getColorShiftOutline():
            lerpRGBValue = animationInfo.getLerpRGBOutlineValue()
            if not lerpRGBValue >= 1:
                lastTextColor = animationInfo.getColorShiftOutlineLastColor()
                animationInfo.setLerpRGBOutlineValue(lerpRGBValue + animationInfo.getLerpRGBOutlineStep())
                red = lastTextColor[0] + (animationInfo.getColorShiftOutlineColor()[0] - lastTextColor[0]) * lerpRGBValue 
                green = lastTextColor[1] + (animationInfo.getColorShiftOutlineColor()[1] - lastTextColor[1]) * lerpRGBValue 
                blue = lastTextColor[2] + (animationInfo.getColorShiftOutlineColor()[2] - lastTextColor[2]) * lerpRGBValue 
                animationInfo.setOutlineColor((red, green, blue))
            else:
                animationInfo.setColorShiftOutline(False)
                animationInfo.setLerpRGBOutlineValue(0)
        if animationInfo.getOutline():
            if self.textSurfaceOutline is None:
                self.textSurfaceOutline = self.loadFontSurface(self.text, self.fontSize, animationInfo.getOutlineColor())
                self.textPositionOutline = self.textPosition
            if animationInfo.getScale() or (animationInfo.getColorShift() and animationInfo.getColorShiftOutline()):
                self.textPositionOutline = self.textPosition
                self.textSurfaceOutline = self.loadFontSurface(self.text, self.fontSize, animationInfo.getOutlineColor())
            if animationInfo.getColorShiftOutline():
                self.textPositionOutline = self.textPosition
                self.textSurfaceOutline = self.loadFontSurface(self.text, self.fontSize, animationInfo.getOutlineColor())
        self.textSurface = self.loadFontSurface(self.text, self.fontSize, self.textColor) 
        if animationInfo.getScaleStep(): self.changeRect(self.textSurface.get_rect(topleft= self.textPosition))
        if animationInfo.getLerpXY(): 
            if animationInfo.getGivenLerpXYPositions():
                positions = animationInfo.getLerpXYPositions() 
                idx = animationInfo.getLerpXYIndex()
                if idx > len(positions) - 1:
                    idx = len(positions) - 1
                currentPosition = positions[int(idx)]
                logger.debug(f"ANIMATING TEXT TO POSITION. {positions=}, {idx=}, {currentPosition=}")
                self.setX(currentPosition[0])
                self.setY(currentPosition[1])
                animationInfo.setLerpXYIndex(idx + animationInfo.getLerpXYStep())
                lastPos = positions[-1] 
                if currentPosition[0] == lastPos[0] and currentPosition[1] == lastPos[1]:

                    animationInfo.setLerpXY(False)
                    animationInfo.setLerpXYIndex(0)
                    animationInfo.setLerpXYStep(0)
            else:
                if not animationInfo.getEllipseInterpolationXY():
                    basePos = animationInfo.getLerpXYOriginalPos()
                    goalPos = animationInfo.getLerpXYGoalPos()
                    lerpXYVal = animationInfo.getLerpXYValue()
                    if lerpXYVal >= 1:
                        lerpXYVal = 1
                        animationInfo.setLerpXY(False)
                        animationInfo.setLerpXYIndex(0)
                        animationInfo.setLerpXYStep(0)
                    x = basePos[0] + (goalPos[0] - basePos[0]) * lerpXYVal
                    y = basePos[1] + (goalPos[1] - basePos[1]) * lerpXYVal
                    lerpXYVal += animationInfo.getLerpXYStep()
                    animationInfo.setLerpXYValue(lerpXYVal)
                    pos = (x,y)
                    if animationInfo.getLerpXYGoalPosIsMiddle():
                        newPos = Misc.middleToTopleftPos((x, y), (self.rect.width, self.rect.height))
                        pos = newPos
                    self.setX(pos[0])
                    self.setY(pos[1])

                 
        if animationInfo.getAlphaChanging():
            step = animationInfo.getAlphaStep()
            goal = animationInfo.getAlphaGoal()
            newAlpha = step + self.textSurfaceAlpha
            logger.debug(f"BUTTON STEP: {step} \n BUTTON GOAL: {goal} \n BUTTON ALPHA: {newAlpha} \n BUTTON PREV ALPHA: {self.textSurfaceAlpha}")
            if step < 0 and newAlpha < goal:
                newAlpha = goal
                animationInfo.setAlphaChanging(False)
            if step > 0 and newAlpha > goal:
                newAlpha = goal
                animationInfo.setAlphaChanging(False)

            self.setTextSurfaceAlpha(newAlpha)
            if animationInfo.getOutline():
                self.setTextSurfaceOutlineAlpha(newAlpha)
            logger.debug(f"BUTTON STEP: {step} \n BUTTON GOAL: {goal} \n BUTTON ALPHA: {newAlpha} \n BUTTON PREV ALPHA: {self.textSurfaceAlpha}")


    def editText(self, new_text: str):
        self.textSurface = self.loadFontSurface(new_text, self.fontSize, self.textColor) 
        self.changeRect(self.textSurface.get_rect(topleft= self.textPosition))
        self.text = new_text

    def update(self, screen: pygame.Surface):
        #if self.hover: self.backgroundColor = (255, 255, 255)
        #else: self.backgroundColor = (0, 0, 0)
        if self.visible:
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

