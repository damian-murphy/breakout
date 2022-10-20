# Screen border and overlay for information
import pygame
import math
from icecream import ic

class infoScreen():

    def __init__(self, image, screenx, screeny):
        # Constructor for console display - anything that isn't a player graphic
        self.borderImage = image
        self.screenx = screenx
        self.screeny = screeny

    def border(self):
        return 0

    def scoreBoard(self):
        return 0

    
        
