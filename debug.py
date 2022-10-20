#  Copyright (c) 2020. murf@the1977project.org
#  "Though a program be but three lines long,
#  someday it will have to be maintained."
#  - Tao of Programming

# Class to create a debug text box object, and then to render supplied text onto it for debugging
# during runtime
import pygame.freetype

DEBUGCOLOUR = (255, 255, 255)


class DebugBox:
    def __init__(self, screen, height, colour=DEBUGCOLOUR):
        self.myfont = pygame.freetype.SysFont(pygame.font.get_default_font(), 18)
        self.text = "Debug: "
        self.tsurf, self.trect = self.myfont.render(self.text, DEBUGCOLOUR)
        self.YPOS = height - 20
        self.XPOS = 5
        self.trect.x = self.XPOS
        self.trect.y = self.YPOS
        self.myscreen = screen

    def message(self, text):
        self.text = "Debug: " + text
        self.tsurf, self.trect = self.myfont.render(text, DEBUGCOLOUR)
        self.trect.x = self.XPOS
        self.trect.y = self.YPOS
        self.myscreen.blit(self.tsurf, self.trect)

    def clear(self, bgcolour):
        self.tsurf.fill(bgcolour)
        self.myscreen.blit(self.tsurf, self.trect)
