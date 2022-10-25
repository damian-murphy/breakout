""" Ball Object - extends pygame sprite class """
import math
import pygame
from icecream import ic

WHITE = (255, 255, 255)
SPEED = 5
INIT_ANGLE = 315


class Ball(pygame.sprite.Sprite):
    """ Ball Object Constructor. Pass in the x and y position, and an image"""

    def __init__(self, image, width, height, screenx, screeny):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # Dict to contain the attributes of the ball object
        self._attribs = {}
        self.image = image
        self.rect = self.image.get_rect()

        # Now, fill in the values using CONSTANTS from top of file or passed in params
        self._attribs = {'surface': pygame.Surface([width, height]),
                        'mask': pygame.mask.from_surface(image),
                        'speed': SPEED,
                        'max_x': screenx - image.get_width(),
                        'max_y': screeny - image.get_height(),
                        'v_x': SPEED,
                        'v_y': SPEED,
                        'angle': math.radians(INIT_ANGLE)
                         }

        # Set the colour key to WHITE
        self.image.set_colorkey(WHITE)

    def _nextpos(self):
        self.rect.x = self.rect.x \
                                  + (self._attribs['v_x'] * math.cos(self._attribs['angle']))
        self.rect.y = self.rect.y + (self._attribs['v_y']
                                                             * math.sin(self._attribs['angle']))
        ic(self.rect.x, self.rect.y,
           math.degrees(self._attribs['angle']), self._attribs['v_x'], self._attribs['v_y'])

    def _reflection(self, hitx, hity):
        ic('REFLECTION')
        midx = self.rect.centerx - self.rect.topleft[0]
        midy = self.rect.centery - self.rect.topleft[1]
        self._attribs['angle'] = math.atan2((hity - midy), (midx - hitx))
        ic(math.degrees(self._attribs['angle']), hitx, hity, midx, midy)
        # Add 2pi radians to the angle if it's less than zero
        # to keep us in the positive numbers.
        if self._attribs['angle'] < 0:
            self._attribs['angle'] += 2 * math.pi
        ic(math.degrees(self._attribs['angle']))
        self._nextpos()

    def move(self, hitx=0, hity=0, is_hit=False):
        """# Keep the ball inside the play area
        # Anything else is a sprite collision and is handled with collision maps.
        # Here we'll also take care of the bounding box collisions

        # If there's a hit detected, then we calculate the position from the
        # centre of the sprite to the collision point.
        # This gives us the angle of impact from the horizontal."""
        if is_hit:
            ic('hit')
            self._reflection(hitx, hity)

        # Check and see if you hit the side of the play area
        elif self.rect.x < 5:
            ic('LHS')
            self.rect.x = 5
            # Remember, collisions using masks return the colliding point relative to the 0,0
            # point of sprite1 (the ball in this case), so we need to calculate the
            # relative y from the absolute y we're using as it's the screen edge not a sprite we hit
            # OK?
            self._reflection(hitx=0, hity=(self.rect.midleft[1] - self.rect.topleft[1]))
        elif self.rect.x > self._attribs['max_x']:
            self.rect.x = self._attribs['max_x'] - 5
            ic('RHS')
            self._reflection(hitx=(self.rect.midright[0] - self.rect.topleft[0]),
                             hity=(self.rect.topleft[1]) - self.rect.midright[1])
        elif self.rect.y < 5:
            self.rect.y = 5
            ic('ROOF')
            self._reflection(hitx=(self.rect.midtop[0] - self.rect.topleft[0]),
                             hity=(self.rect.topleft[1] - self.rect.midtop[1]))
        elif self.rect.y > self._attribs['max_y']:
            self.rect.y = self._attribs['max_y'] - 5
            ic('FLOOR', self.rect.y, self.rect.x)
            self._reflection(hitx=(self.rect.topleft[0] - self.rect.midbottom[0]),
                             hity=(self.rect.midbottom[1] - self.rect.topleft[1]))
        else:
            # Otherwise, move normally in open game space
            # Calculate the next position based on angle and speed in x,y
            self._nextpos()

    def setimage(self, image):
        """ Change the image used for the ball """
        self._attribs['image'] = image

    def v_x(self, vx=None):
        """ Set the X velocity if passed and return the current value """
        if vx is None:
            return self._attribs['v_x']
        else:
            self._attribs['v_x'] = vx
            return self._attribs['v_x']

    def v_y(self, vy=None):
        """ Set the Y velocity if passed and return the current value """
        if vy is None:
            return self._attribs['v_y']
        else:
            self._attribs['v_y'] = vy
            return self._attribs['v_y']


    def angle(self, angle=None):
        """ Return the current angle value or set it if angle= is passed
            Always returns the angle value after changing """
        if angle is None:
            return self._attribs['angle']
        else:
            self._attribs['angle'] = angle
            return self._attribs['angle']
