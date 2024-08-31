from game.Scenes.BaseScene import SceneAnimations
from game.utils.SettingsFunctions import checkVariableInClass
from debug.logger import logger
import pygame


class AnimationStates:
    INITIALIZING = "INITIALIZING"
    RUNNING = "RUNNING"
    FINISHED = "FINISHED"

class AnimationAttributes:
    OPACITY = "OPACITY"
    OPACITY_STEP = "OPACITY_STEP"
    RECTS = "RECTS"
    RECT_COLOR = "RECT_COLOR"
    RECT_INDEX = "RECT_INDEX"
    RECT_LIMIT = "RECT_LIMIT"
    NUM_RECTS = "NUM_RECTS"
    RECT_STEP = "RECT_STEP"
    RADIUS = "RADIUS"
    RADIUS_STEP = "RADIUS_STEP"

class SceneAnimation:
    def __init__(self, name: str, screen_size: tuple):
        logger.info(f"Initiliazing Scene Animation {name=}")
        assert checkVariableInClass(name, SceneAnimations)
        self.state = AnimationStates.INITIALIZING
        self.name = name
        self.attributes = self.loadAttributesByName(name, screen_size)
        self.state = AnimationStates.RUNNING

    def setState(self, state: str):
        self.state = state

    def loadAttributesByName(self, animation_name: str, screen_size: tuple) -> dict:
        attributes = {}
        if animation_name == SceneAnimations.DRAG_IN_WITH_WHITE_HORIZONTAL_LINES or animation_name ==  SceneAnimations.DRAG_IN_WITH_BLACK_HORIZONTAL_LINES:
            pass
        match animation_name:
            case SceneAnimations.DRAG_IN_WITH_WHITE_HORIZONTAL_LINES:
                attributes[AnimationAttributes.RECTS] = self.loadRects(animation_name, screen_size)
                attributes[AnimationAttributes.RECT_COLOR] = self.loadRectColor(animation_name)
                attributes[AnimationAttributes.RECT_INDEX] = 0
                attributes[AnimationAttributes.RECT_LIMIT] = screen_size[0]
                attributes[AnimationAttributes.NUM_RECTS] = 5
                attributes[AnimationAttributes.RECT_STEP] = 50
            case SceneAnimations.DRAG_IN_WITH_BLACK_HORIZONTAL_LINES:
                attributes[AnimationAttributes.RECTS] = self.loadRects(animation_name, screen_size)
                attributes[AnimationAttributes.RECT_COLOR] = self.loadRectColor(animation_name)
                attributes[AnimationAttributes.RECT_INDEX] = 0
                attributes[AnimationAttributes.RECT_LIMIT] = screen_size[0]
                attributes[AnimationAttributes.NUM_RECTS] = 5
                attributes[AnimationAttributes.RECT_STEP] = 50
            case SceneAnimations.FADE_IN:
                attributes[AnimationAttributes.OPACITY] = 0 
                attributes[AnimationAttributes.OPACITY_STEP] = 5
            case SceneAnimations.FADE_OUT:
                attributes[AnimationAttributes.OPACITY] = 255
                attributes[AnimationAttributes.OPACITY_STEP] = 5
            case SceneAnimations.FADE_IN_AND_OUT:
                attributes[AnimationAttributes.OPACITY] = 0 
                attributes[AnimationAttributes.OPACITY_STEP] = 5
            case SceneAnimations.CIRCLE_TRANSITION:
                attributes[AnimationAttributes.RADIUS] = int(screen_size[0]/2)
                attributes[AnimationAttributes.RADIUS_STEP] = 20
        return attributes

    def loadOpacity(self, animation_name: str):
        assert animation_name == SceneAnimations.FADE_IN or animation_name == SceneAnimations.FADE_OUT or animation_name == SceneAnimations.FADE_IN_AND_OUT
        if animation_name == SceneAnimations.FADE_IN or animation_name == SceneAnimations.FADE_IN_AND_OUT:
            return 255
        return 0

    def loadRects(self, animation_name, screen_size, num_rects=3):
        assert animation_name == SceneAnimations.DRAG_IN_WITH_WHITE_HORIZONTAL_LINES or animation_name == SceneAnimations.DRAG_IN_WITH_BLACK_HORIZONTAL_LINES
        rects = []
        step = screen_size[1] / num_rects 
        height = step + 5 # + 5 used for edge cases on float rounding
        top = 0
        for i in range(num_rects):
            rect = pygame.Rect(0, top, 0, height)
            rects.append(rect) 
            top += step
        return rects

    def loadRectColor(self, animation_name: str):
        assert animation_name == SceneAnimations.DRAG_IN_WITH_WHITE_HORIZONTAL_LINES or animation_name == SceneAnimations.DRAG_IN_WITH_BLACK_HORIZONTAL_LINES
        match animation_name:
            case SceneAnimations.DRAG_IN_WITH_BLACK_HORIZONTAL_LINES:
                return 0,0,0
            case SceneAnimations.DRAG_IN_WITH_WHITE_HORIZONTAL_LINES:
                return 255,255,255
            case _:
                return 0,0,0

    def updateRects(self, rects: list[pygame.Rect], animation_name):
        logger.debug(f"UPDATING RECTS FOR {animation_name=}")
        if self.state == AnimationStates.FINISHED:
            return None
        assert animation_name == SceneAnimations.DRAG_IN_WITH_BLACK_HORIZONTAL_LINES or animation_name == SceneAnimations.DRAG_IN_WITH_WHITE_HORIZONTAL_LINES
        rectIndex = self.attributes[AnimationAttributes.RECT_INDEX]
        rectLimit = self.attributes[AnimationAttributes.RECT_LIMIT]
        rectStep = self.attributes[AnimationAttributes.RECT_STEP]
        for i in range(rectIndex + 1):
            if i == rectIndex:
                if rects[i].width >= rectLimit/2 and i != len(rects) - 1:
                    rectIndex += 1
            if rects[i].width >= rectLimit:
                rects[i].width = rectLimit
                if i == len(rects) - 1:
                    self.setState(AnimationStates.FINISHED)
                self.attributes[AnimationAttributes.RECT_INDEX] = rectIndex
                continue 
            rects[i].width += rectStep 
        if rectIndex >= len(rects):
            self.state = AnimationStates.FINISHED

    def renderHorizontalLineAnimation(self, screen, rects, background, color):
        screen.blit(background, (0,0))
        for rect in rects:
            pygame.draw.rect(screen, color, rect)

    def renderFadeInAndOutAnimation(self, screen, background1, background2, opacity, opacity_step):
        opacity += opacity_step
        if opacity >= 255: opacity = 255
        fadeOutSurf = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        fadeOutSurf.set_alpha(255 - opacity)
        fadeInSurf = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        fadeInSurf.set_alpha(opacity)
        fadeOutSurf.blit(background1, (0,0))
        fadeInSurf.blit(background2, (0,0))
        screen.blit(fadeInSurf, (0,0))
        screen.blit(fadeOutSurf, (0,0))
        if opacity == 255:
            self.setState(AnimationStates.FINISHED)
        self.attributes[AnimationAttributes.OPACITY] = opacity

    def renderFadeAnimation(self, screen, background, opacity, opacity_step):
        if self.name == SceneAnimations.FADE_IN:
            opacity += opacity_step
            if opacity >= 255: opacity = 255
        else:
            opacity -= opacity_step
            if opacity <= 0: opacity = 0
        fadeSurf = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        fadeSurf.set_alpha(opacity)
        fadeSurf.blit(background, (0,0))
        screen.blit(fadeSurf, (0,0))
        
        if opacity == 255:
            if self.name == SceneAnimations.FADE_IN:
                self.setState(AnimationStates.FINISHED)
        elif opacity == 0:
            if self.name == SceneAnimations.FADE_OUT: self.setState(AnimationStates.FINISHED)
        self.attributes[AnimationAttributes.OPACITY] = opacity

    def cropBackgroundToCircle(self, background_surf: pygame.Surface, radius, screen: pygame.Surface):
        assert self.name == SceneAnimations.CIRCLE_TRANSITION
        croppedSurf = pygame.Surface(background_surf.get_size(), pygame.SRCALPHA)
        circleCenter = background_surf.width / 2 , background_surf.height / 2
        pygame.draw.aacircle(croppedSurf, (255, 255, 255, 255), circleCenter, radius)
        croppedSurf.blit(background_surf, (0,0), special_flags=pygame.BLEND_RGBA_MIN)
        screen.blit(croppedSurf, (0,0))

    def updateRadius(self, radius_step, radius_limit):
        assert radius_step != 0
        assert radius_limit >= 0
        assert self.name == SceneAnimations.CIRCLE_TRANSITION
        radius = self.attributes[AnimationAttributes.RADIUS]
        self.radius += radius_step
        if radius_step > 0:
            if self.radius >= radius_limit:
                self.radius = radius_limit
        else:
            if self.radius <= radius_limit:
                self.radius = radius_limit
        self.attributes[AnimationAttributes.RADIUS] = radius

    def animate(self, animation_name, screen, background1, background2):
        match animation_name:
            case SceneAnimations.DRAG_IN_WITH_WHITE_HORIZONTAL_LINES:
                rects = self.attributes[AnimationAttributes.RECTS] 
                self.updateRects(rects, animation_name)
                self.renderHorizontalLineAnimation(screen, rects, background1, self.attributes[AnimationAttributes.RECT_COLOR]) 
            case SceneAnimations.DRAG_IN_WITH_BLACK_HORIZONTAL_LINES:
                rects = self.attributes[AnimationAttributes.RECTS] 
                self.updateRects(rects, animation_name)
                self.renderHorizontalLineAnimation(screen, rects, background1, self.attributes[AnimationAttributes.RECT_COLOR]) 
            case SceneAnimations.FADE_IN_AND_OUT:
                self.renderFadeInAndOutAnimation(screen, background1, background2, self.attributes[AnimationAttributes.OPACITY], self.attributes[AnimationAttributes.OPACITY_STEP]) 
            case SceneAnimations.FADE_IN:
                self.renderFadeAnimation(screen, background1, self.attributes[AnimationAttributes.OPACITY], self.attributes[AnimationAttributes.OPACITY_STEP])
    def update(self, screen, background1=None, background2=None):
        #backgrounds numbered by blitting order
        self.animate(self.name, screen, background1, background2) 
        logger.debug(f"OUTPUTTING ANIMATION INFO: \n{self.name=} \n{self.attributes=} \n{self.state=}  ")
