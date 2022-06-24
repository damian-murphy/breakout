# A simple Breakout Clone.
# By Damian Murphy
# Inspired by Tho' The Wall for the ZX Spectrum
# (https://en.wikipedia.org/wiki/Horizons:_Software_Starter_Pack)
# License: GNU GPL v3
#

import pygame
import pygame.freetype
from ball import Ball
from wall import Wall, Block
from debug import DebugBox
from pygame.locals import *

# Setup
width, height = 800, 600
bat = pygame.image.load("graphics/images/bat.png")
brick = pygame.image.load("graphics/images/brick.png")
ball_img = pygame.image.load("graphics/images/ball.png")
background = pygame.image.load("graphics/images/sky_bg1.jpg")
playerpos = [390, 560]
keys = [False, False]
bgcolour = (0, 0, 0)
WHITE = (255, 255, 255)
DEBUG = True


def init_game():
    pygame.init()


class player(pygame.sprite.Sprite):
    # Constructor. Pass in its x and y position
    def __init__(self, image, width, height):
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

    def moveRight(self, pixels):
        self.rect.x += pixels

    def moveLeft(self, pixels):
        self.rect.x -= pixels

    def getLeftHandSide(self):
        return self.rect.left

    def getRightHandSide(self):
        return self.rect.right


def clear_callback(surf, rect):
    surf.fill(bgcolour, rect)


def main():
    # Call the init function of pygame, really, I should move all the initialise code there
    # and let it set globals? Woah, I'm a rule breaker.
    init_game()
    # Used to manage how fast the screen updates
    # Really handy, because this isn't a ZX Spectrum we're running on where I had to worry
    # about screen flicker and getting things done in 1/50sec
    clock = pygame.time.Clock()
    # Create the display surface
    screen = pygame.display.set_mode((width, height))
    # Set the caption on the Window
    pygame.display.set_caption("Breakout!")
    # Create player1, a controlled sprite
    player1 = player(bat, bat.get_width(), bat.get_height())
    players = pygame.sprite.GroupSingle(player1)
    # Create the ball, a moving sprite.
    the_ball = Ball(ball_img, ball_img.get_width(), ball_img.get_height(), width, height)

    # Group of balls.
    balls = pygame.sprite.Group(the_ball)

    # If we're running in debug mode, then setup the debugger. Otherwise, eh, don't.
    if (DEBUG):
        debugger = DebugBox(screen, height)

    # Blank screen & create background screen as well
    # So the we have something to put under moving things
    screen.fill(0)
    # Get the dimensions of the BG image, so we can try and centre it somewhat
    bgx, bgy = int(width / 2) - int(background.get_width() / 2), int(height / 2) - int(background.get_height() / 2)
    screen.blit(background, [bgx, bgy])
    bgScreen = pygame.Surface((width, height))
    bgScreen.blit(background, [bgx, bgy])

    # Create the Wall of blocks
    wall = pygame.sprite.Group()
    for y in range(10, 5 * brick.get_height(), brick.get_height()):
        for x in range(round(width / brick.get_width() - 1)):
            wall.add(Block(brick, brick.get_width(), brick.get_height(), (10 + (x * (brick.get_width() + 1))), y))

    # Set the player sprite starting position
    # Draw our player
    #player1.rect.x = 390
    player1.rect.x = 10
    player1.rect.y = 560
    the_ball.rect.x = 300
    the_ball.rect.y = 500
    # Draw the player sprite
    players.draw(screen)
    balls.draw(screen)
    wall.draw(screen)

    while 1:

        # Limit to 60 frames per second. Call this once per frame only.
        clock.tick(60)

        # Do a screen update, flicker free!
        pygame.display.flip()

        # Have a look, see did an event happen!
        for event in pygame.event.get():
            # check if the event is the X button
            if event.type == pygame.QUIT:
                # if it is quit the game
                pygame.quit()
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == K_z:
                    keys[0] = True
                elif event.key == K_x:
                    keys[1] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_z:
                    keys[0] = False
                elif event.key == pygame.K_x:
                    keys[1] = False

        # FIX (https://github.com/damian-murphy/breakout/issues/2)
        # Get the bat position, check if it's at the edge, adjust accordingly.
        # and make sure we don't move outside the play area, or the bat will disappear off screen
        if keys[0]:
            if (player1.getLeftHandSide() < 10) & (player1.getLeftHandSide() > 0):
                player1.moveLeft(10 - player1.getLeftHandSide())
            elif player1.getLeftHandSide() == 0 or player1.getLeftHandSide() < 0:
                player1.moveLeft(0)
            else:
                player1.moveLeft(10)
        elif keys[1]:
            if (player1.getRightHandSide() > (width-10)) and (player1.getRightHandSide() < width):
                player1.moveRight(10 - (width - player1.getRightHandSide()))
            elif player1.getRightHandSide() == width or player1.getRightHandSide() > width:
                player1.moveRight(0)
            else:
                player1.moveRight(10)

        # Check for collisions
        # Let's do all the collision logic here, then we just tell the objects
        # what went down during the frame.
        # First, the bat and any ball
        if pygame.sprite.spritecollide(player1, balls, False, pygame.sprite.collide_mask):
            try:
                (hitx, hity) = pygame.sprite.collide_mask(player1, the_ball)
                the_ball.move(hitx, hity, isHit=True)
            except TypeError:
                the_ball.move()
        # Now, see if a ball hit any wall block
        elif pygame.sprite.spritecollide(the_ball, wall, False, pygame.sprite.collide_mask):
            try:
                for b in iter(wall.sprites()):
                    if b.rect.colliderect(the_ball.rect):
                        (hitx, hity) = pygame.sprite.collide_mask(the_ball, b)
                        wall.remove(b)
                        the_ball.move(hitx, hity, isHit=True)
            except TypeError:
                the_ball.move()
        else:
            # No collision, so move normally.
            the_ball.move()

        # Update the sprites
        players.clear(screen, bgScreen)
        balls.clear(screen, bgScreen)
        wall.clear(screen, bgScreen)
        players.draw(screen)
        balls.draw(screen)
        wall.draw(screen)
        # So, use that debugger object from earlier and print some (hopefully) useful info.
        if (DEBUG):
            debugger.clear(bgcolour)
            debugmessage = "P {0: >4.0f},{1: >4.0f} B {2: >4.0f},{3: >4.0f} A {4: >4.0f} V {5: >4.0f},{6: >4.0f} FT {7: >4.0f}ms FR {8: >4.0f} frames/sec".format(
                player1.rect.x, player1.rect.y, the_ball.rect.x, the_ball.rect.y, the_ball.angle, the_ball.vx,
                the_ball.vy, clock.get_rawtime(), clock.get_fps())
            debugger.message(debugmessage)


if __name__ == "__main__":
    main()
