#  Copyright (c) 2020. murf@the1977project.org
#  "Though a program be but three lines long,
#  someday it will have to be maintained."
#  - Tao of Programming

""" Class to create a debug text box object, and then to render supplied text onto it for debugging
    during runtime"""
import pygame.freetype

DEBUGCOLOUR = (255, 255, 255)


class DebugBox:
    """ Debugbox class to show debug info"""
    def __init__(self, screen, height, colour=DEBUGCOLOUR):
        self.myfont = pygame.freetype.SysFont(pygame.font.get_default_font(), 14)
        self.text = "Debug: "
        self.colour = colour
        self.tsurf, self.trect = self.myfont.render(self.text, self.colour)
        self.pos = (5, height - 20)
        self.trect.x, self.trect.y = self.pos
        self.myscreen = screen

    def message(self, text):
        """ Show a message in the debug box """
        self.text = "Debug: " + text
        self.tsurf, self.trect = self.myfont.render(self.text, self.colour)
        self.myscreen.blit(self.tsurf, self.trect)

    def clear(self, bgcolour):
        """ Clear the debug box setting to background colour """
        self.tsurf.fill(bgcolour)
        self.myscreen.blit(self.tsurf, self.trect)
