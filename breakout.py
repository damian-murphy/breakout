"""# A simple Breakout Clone.
# By Damian Murphy
# Inspired by Tho' The Wall for the ZX Spectrum
# (https://en.wikipedia.org/wiki/Horizons:_Software_Starter_Pack)
# License: GNU GPL v3
#"""

import math
import sys
import pygame
import pygame.freetype
import pygame.locals
from icecream import install, ic

from ball import Ball
from wall import Wall, Block
from debug import DebugBox


# Setup
DEBUG = True
# Enable and install icecream for debugging
if DEBUG:
    install()
    ic.enable()
    ic.configureOutput(prefix='Debug| ')


# In the pygame screen, the cartesian co-ordinates are rotated right by 90 degrees
# So, traditionally north or 0 degress is vertically up, now it's right or East.
# And it's all mirrored, due to 0,0 being at the top left not bottom left.
# So 90 is up, 270 is down, 180 is left, 0 is right.


def init_game():
    """ Initialise game settings """
    pygame.init()

    global GAME_WIDTH, GAME_HEIGHT, BAT_IMG, BRICK_IMG, BALL_IMG,\
        BACKGROUND_IMG, INIT_PLAYERPOS, BGCOLOUR, WHITE

    GAME_WIDTH, GAME_HEIGHT = 800, 600
    BAT_IMG = pygame.image.load("graphics/images/bat.png")
    BRICK_IMG = pygame.image.load("graphics/images/brick.png")
    BALL_IMG = pygame.image.load("graphics/images/ball.png")
    BACKGROUND_IMG = pygame.image.load("graphics/images/sky_bg1.jpg")
    INIT_PLAYERPOS = [390, 560]

    BGCOLOUR = (0, 0, 0)
    WHITE = (255, 255, 255)



class Player(pygame.sprite.Sprite):
    """ Player Class - this is the player object, the bat """
    # Constructor. Pass in its x and y position
    def __init__(self, image, player_width, player_height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([player_width, player_height])
        self.image = image
        self.image.set_colorkey(WHITE)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def moveright(self, pixels):
        """ Move to the right by x pixels"""
        self.rect.x += pixels

    def moveleft(self, pixels):
        """ Move to the left by x pixels"""
        self.rect.x -= pixels

    def get_left_hand_side(self):
        """ Return LHS x co-ord value"""
        return self.rect.left

    def get_right_hand_side(self):
        """ Return RHS x co-ord value"""
        return self.rect.right


def clear_callback(surf, rect):
    """ Callback function to reset the screen to background, wiping the sprite """
    surf.fill(BGCOLOUR, rect)


def main():
    """ Main Loop """
    # Call the init function of pygame, really, I should move all the initialise code there
    # and let it set globals? Woah, I'm a rule breaker.
    init_game()
    # Used to manage how fast the screen updates
    # Really handy, because this isn't a ZX Spectrum we're running on where I had to worry
    # about screen flicker and getting things done in 1/50sec
    clock = pygame.time.Clock()
    # Create the display surface
    screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
    # Set the caption on the Window
    pygame.display.set_caption("Breakout!")
    # Create player1, a controlled sprite
    player1 = Player(BAT_IMG, BAT_IMG.get_width(), BAT_IMG.get_height())
    players = pygame.sprite.GroupSingle(player1)
    # Create the ball, a moving sprite.
    the_ball = Ball(BALL_IMG, BALL_IMG.get_width(), BALL_IMG.get_height(), GAME_WIDTH, GAME_HEIGHT)

    # List to contain keypresses
    keys_pressed = [False, False]

    # Group of balls.
    balls = pygame.sprite.Group(the_ball)

    # If we're running in debug mode, then setup the debugger. Otherwise, eh, don't.
    if DEBUG:
        debugger = DebugBox(screen, GAME_HEIGHT)

    # Blank screen & create background screen as well
    # So the we have something to put under moving things
    screen.fill(0)
    # Get the dimensions of the BG image, so we can try and centre it somewhat
    bgx, bgy = int(GAME_WIDTH / 2) - int(BACKGROUND_IMG.get_width() / 2), int(GAME_HEIGHT / 2) \
               - int(BACKGROUND_IMG.get_height() / 2)
    screen.blit(BACKGROUND_IMG, [bgx, bgy])
    bg_screen = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
    bg_screen.blit(BACKGROUND_IMG, [bgx, bgy])

    # Create the Wall of blocks
    wall = pygame.sprite.Group()
    for y_pos in range(10, 5 * BRICK_IMG.get_height(), BRICK_IMG.get_height()):
        for x_pos in range(round(GAME_WIDTH / BRICK_IMG.get_width() - 1)):
            wall.add(Block(BRICK_IMG, BRICK_IMG.get_width(), BRICK_IMG.get_height(),
                           (10 + (x_pos * (BRICK_IMG.get_width() + 1))), y_pos))

    # Set the player sprite starting position
    # Draw our player
    # player1.rect.x = 390
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
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    keys_pressed[0] = True
                elif event.key == pygame.K_x:
                    keys_pressed[1] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_z:
                    keys_pressed[0] = False
                elif event.key == pygame.K_x:
                    keys_pressed[1] = False

        # FIX (https://github.com/damian-murphy/breakout/issues/2)
        # Get the bat position, check if it's at the edge, adjust accordingly.
        # and make sure we don't move outside the play area, or the bat will disappear off screen
        if keys_pressed[0]:
            if (player1.get_left_hand_side() < 10) & (player1.get_left_hand_side() > 0):
                player1.moveleft(10 - player1.get_left_hand_side())
            elif player1.get_left_hand_side() == 0 or player1.get_left_hand_side() < 0:
                player1.moveleft(0)
            else:
                player1.moveleft(10)
        elif keys_pressed[1]:
            if (player1.get_right_hand_side() > (GAME_WIDTH - 10)) \
                    and (player1.get_right_hand_side() < GAME_WIDTH):
                player1.moveright(10 - (GAME_WIDTH - player1.get_right_hand_side()))
            elif player1.get_right_hand_side() == GAME_WIDTH \
                    or player1.get_right_hand_side() > GAME_WIDTH:
                player1.moveright(0)
            else:
                player1.moveright(10)

        # Check for collisions
        # Let's do all the collision logic here, then we just tell the objects
        # what went down during the frame.
        # First, the bat and any ball
        # if pygame.sprite.spritecollide(player1, balls, False, pygame.sprite.collide_mask):
        #     try:
        #         (hitx, hity) = pygame.sprite.collide_mask(player1, the_ball)
        #         the_ball.move(hitx, hity, isHit=True)
        #     except TypeError:
        #         the_ball.move()
        # # Now, see if a ball hit any wall block
        # elif pygame.sprite.spritecollide(the_ball, wall, False, pygame.sprite.collide_mask):
        #     try:
        #         for b in iter(wall.sprites()):
        #             if b.rect.colliderect(the_ball.rect):
        #                 (hitx, hity) = pygame.sprite.collide_mask(the_ball, b)
        #                 wall.remove(b)
        #                 the_ball.move(hitx, hity, isHit=True)
        #     except TypeError:
        #         the_ball.move()
        # else:
        # No collision, so move normally.
        the_ball.move()

        # Update the sprites
        players.clear(screen, bg_screen)
        balls.clear(screen, bg_screen)
        wall.clear(screen, bg_screen)
        players.draw(screen)
        balls.draw(screen)
        wall.draw(screen)
        # So, use that debugger object from earlier and print some (hopefully) useful info.
        if DEBUG:
            debugger.clear(BGCOLOUR)
            debugmessage = "P {0: >4.0f},{1: >4.0f} B {2: >4.0f},{3: >4.0f} A {4: >4.0f} " \
                           "V {5: >4.0f},{6: >4.0f} FT {7: >4.0f}ms FR {8: >4.0f} " \
                           "frames/sec".format(
                            player1.rect.x, player1.rect.y, the_ball.rect.x, the_ball.rect.y,
                            math.degrees(the_ball.angle()), the_ball.v_x(),
                the_ball.v_y(), clock.get_rawtime(), clock.get_fps())
            debugger.message(debugmessage)


if __name__ == "__main__":
    main()
