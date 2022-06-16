# Ball Object - extends pygame sprite class
import pygame
import math

WHITE = (255, 255, 255)
SPEED = 5
INIT_ANGLE = 45


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
        self.angle = INIT_ANGLE
        self.max_x = screenx - image.get_width()
        self.max_y = screeny - image.get_height()
        self.vx, self.vy = self.speed, -self.speed
        self.midx = image.get_width() / 2
        self.midy = image.get_height() / 2

    def move(self, hitx=0, hity=0, isHit=False):
        # Keep the ball inside the play area
        # Anything else is a sprite collision and is handled with collision maps.

        # self.rect.x += ( SPEED * math.cos(self.angle))
        # self.rect.y += ( SPEED * math.sin(self.angle))

        # Here we'll take care of the bounding box collisions

        # If there's a hit detected, then we calculate the position from the centre of the sprite to the
        # collision point. This gives us the angle of impact from the horizontal.
        if isHit:
            self.angle = math.degrees(math.atan2((self.midy - hity), (self.midx - hitx)))
            self.rect.x = self.rect.x + (self.vx * math.sin(self.angle))
            self.rect.y = self.rect.y + (self.vy * math.cos(self.angle))
        # Check and see if you hit the side of the play area
        elif (self.rect.x < 5):
            self.rect.x = 5
            self.vx *= -1
            self.rect.x = self.rect.x + (self.vx * math.sin(self.angle))
            self.rect.y = self.rect.y + (self.vy * math.cos(self.angle))

        elif (self.rect.x > self.max_x):
            self.rect.x = self.max_x - 5
            self.vx *= -1
            self.rect.x = self.rect.x + (self.vx * math.sin(self.angle))
            self.rect.y = self.rect.y + (self.vy * math.cos(self.angle))
            # self.angle = 360 - self.angle
        elif (self.rect.y < 5):
            self.rect.y = 5
            self.vy *= -1
            self.rect.x = self.rect.x + (self.vx * math.sin(self.angle))
            self.rect.y = self.rect.y + (self.vy * math.cos(self.angle))
            # self.angle = 360 - self.angle
        elif (self.rect.y > self.max_y):
            self.rect.y = self.max_y - 5
            self.vy *= -1
            self.angle = self.angle - 90
            self.rect.x = self.rect.x + (self.vx * math.sin(self.angle))
            self.rect.y = self.rect.y + (self.vy * math.cos(self.angle))
            # self.angle = 360 - self.angle
        else:
            # Otherwise, move normally in open game space
            # Calculate the next position based on angle and speed in x,y
            self.rect.x = self.rect.x + (self.vx * math.sin(self.angle))
            self.rect.y = self.rect.y + (self.vy * math.cos(self.angle))
