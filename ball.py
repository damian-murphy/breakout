""" Ball Object - extends pygame sprite class """
import math
import pygame
from icecream import ic

WHITE = (255, 255, 255)
SPEED = 5
INIT_POS = (300, 500)

class Ball(pygame.sprite.Sprite):
    """ Ball Object Constructor. Pass in the x and y position, and an image"""

    def __init__(self, image, screenx, screeny):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # Dict to contain the attributes of the ball object
        self._attribs = {}
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = INIT_POS

        my_width = image.get_width()
        my_height = image.get_height()

        # Now, fill in the values using CONSTANTS from top of file or passed in params
        self._attribs = {'surface': pygame.Surface([my_width, my_height]),
                         'mask': pygame.mask.from_surface(image),
                         'speed': SPEED,
                         'max_x': screenx - my_width,
                         'max_y': screeny - my_height,
                         'my_centerx': round(my_width/2),
                         'my_centery': round(my_height/2),
                         'health': 1,
                         'primary': True,
                         'position': pygame.math.Vector2(INIT_POS),
                         'direction': pygame.math.Vector2(self.rect.centerx + SPEED,
                                                          -(self.rect.centery - SPEED)).normalize()
                         }

        # Set the colour key to WHITE
        self.image.set_colorkey(WHITE)

    def _nextpos(self):
        self._attribs['position'] += self._attribs['direction'] * self._attribs['speed']
        self.rect.center = round(self._attribs['position'].x), round(self._attribs['position'].y)
        ic(self.rect.center,
           self._attribs['position'], self._attribs['direction'], self._attribs['speed'])

    def _reflection(self, force):
        """ Calculate the next position based on the 'force' or external vector and our own """
        ic('REFLECTION')
        self._attribs['direction'] = self._attribs['direction'].reflect(force)
        ic(self._attribs['direction'], self._attribs['position'])
        self._nextpos()

    def move(self, hitx=0, hity=0, is_hit=False):
        """ Keep the ball inside the play area
        Anything else is a sprite collision and is handled with collision maps.
        Here we'll also take care of the bounding box collisions

        If there's a hit detected, then we calculate the position from the
        centre of the sprite to the collision point.
        This gives us the angle of impact from the horizontal."""
        if is_hit:
            ic('hit')
            # Force vector is from this hit point towards the centre of the ball.
            # We bounce with equal and opposite force, directed away
            # on a line from the hitpoint to the centre of the ball.
            hitvector = pygame.math.Vector2(((hitx + self._attribs['my_centerx'],
                                              hity - self._attribs['my_centery']))).normalize()
            ic(hitvector)
            self._reflection(hitvector)

        # Check and see if you hit the side of the play area
        elif self.rect.x <= 5:
            ic('LHS')
            # LHS, so direction vector is to the right
            self._reflection((1,0))
        elif self.rect.x >= self._attribs['max_x']:
            ic('RHS')
            self._reflection((-1, 0))
        elif self.rect.y <= 5:
            ic('ROOF')
            self._reflection((0, 1))
        elif self.rect.y >= self._attribs['max_y']:
            ic('FLOOR', self.rect.y, self.rect.x)
            self._reflection((0, -1))
        else:
            # Otherwise, move normally in open game space
            # Calculate the next position based on angle and speed in x,y
            self._nextpos()

    def setimage(self, image):
        """ Change the image used for the ball """
        self._attribs['image'] = image

    def speed(self, v_xy=None):
        """ Set the X velocity if passed and return the current value """
        if v_xy is None:
            return self._attribs['speed']
        # else:
        self._attribs['speed'] = v_xy
        return self._attribs['speed']

    def hit(self):
        """ Hit/Life counter loses 1 health on hit,
        Allows us to have blocks that need more than one hit to destroy.
        Return the health left
        For the primary ball, this does nothing, just allows for standard procedures elsewhere """

        if not self._attribs['primary']:
            self._attribs['health'] -= 1

        return self._attribs['health']

    def is_primary(self):
        """ Return value of primary attrib.
        :returns True if this is the original primary ball, otherwise False """

        return self._attribs['primary']
