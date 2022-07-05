# Ball Object - extends pygame sprite class
import pygame
import math
from icecream import ic

WHITE = (255, 255, 255)
SPEED = 5
INIT_ANGLE = 315


class Ball(pygame.sprite.Sprite):
    # Constructor. Pass in the x and y position, and an image
    def __init__(self, image, width, height, screenx, screeny):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image = image
        self.image.set_colorkey(WHITE)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.speed = SPEED
        self.angle = math.radians(INIT_ANGLE)
        self.max_x = screenx - image.get_width()
        self.max_y = screeny - image.get_height()
        self.vx, self.vy = self.speed, self.speed

    def _nextpos(self):
        self.rect.x = self.rect.x + (self.vx * math.cos(self.angle))
        self.rect.y = self.rect.y + (self.vy * math.sin(self.angle))
        ic(self.rect.x, self.rect.y, math.degrees(self.angle), self.vx, self.vy)

    def _reflection(self, hitx, hity):
        ic('REFLECTION')
        midx = self.rect.centerx - self.rect.topleft[0]
        midy = self.rect.centery - self.rect.topleft[1]
        self.angle = math.atan2((hity - midy), (midx - hitx))
        ic(math.degrees(self.angle), hitx, hity, midx, midy)
        # Add 2pi radians to the angle if it's less than zero
        # to keep us in the positive numbers.
        if self.angle < 0:
            self.angle += 2 * math.pi
        ic(math.degrees(self.angle))
        self._nextpos()

    def move(self, hitx=0, hity=0, isHit=False):
        # Keep the ball inside the play area
        # Anything else is a sprite collision and is handled with collision maps.
        # Here we'll also take care of the bounding box collisions

        # If there's a hit detected, then we calculate the position from the centre of the sprite to the
        # collision point. This gives us the angle of impact from the horizontal.
        if isHit:
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
        elif self.rect.x > self.max_x:
            self.rect.x = self.max_x - 5
            ic('RHS')
            self._reflection(hitx=(self.rect.midright[0] - self.rect.topleft[0]),
                             hity=(self.rect.topleft[1]) - self.rect.midright[1])
        elif self.rect.y < 5:
            self.rect.y = 5
            ic('ROOF')
            self._reflection(hitx=(self.rect.midtop[0] - self.rect.topleft[0]),
                             hity=(self.rect.topleft[1] - self.rect.midtop[1]))
        elif self.rect.y > self.max_y:
            self.rect.y = self.max_y - 5
            ic('FLOOR', self.rect.y, self.rect.x)
            self._reflection(hitx=(self.rect.topleft[0] - self.rect.midbottom[0]),
                             hity=(self.rect.midbottom[1] - self.rect.topleft[1]))
        else:
            # Otherwise, move normally in open game space
            # Calculate the next position based on angle and speed in x,y
            self._nextpos()
