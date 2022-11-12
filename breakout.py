"""# A simple Breakout Clone.
# By Damian Murphy
# Inspired by Tho' The Wall for the ZX Spectrum
# (https://en.wikipedia.org/wiki/Horizons:_Software_Starter_Pack)
# License: GNU GPL v3
#"""

# pylint: disable=no-member

import sys
import pygame
import pygame.freetype
import pygame.locals
from icecream import install, ic

from player import Player
from ball import Ball
from wall import Block
from debug import DebugBox

# Setup
DEBUG = True
# Enable and install icecream for debugging
if DEBUG:
    install()
    ic.enable()
    ic.configureOutput(prefix='Debug| ')

# Some Constants, could be settings taken from a file later
GAME_SCREEN = (800, 600)  # width, height tuple
BAT_IMG = pygame.image.load("graphics/images/bat.png")
BRICK_IMG = pygame.image.load("graphics/images/brick.png")
BALL_IMG = pygame.image.load("graphics/images/ball.png")
BACKGROUND_IMG = pygame.image.load("graphics/images/sky_bg1.jpg")
INIT_PLAYERPOS = (390, 560)
BGCOLOUR = (0, 0, 0)
WHITE = (255, 255, 255)
TICKS = 60
PLAYER_HEALTH = 3

# In the pygame screen, the cartesian co-ordinates are rotated right by 90 degrees
# So, traditionally north or 0 degress is vertically up, now it's right or East.
# And it's all mirrored, due to 0,0 being at the top left not bottom left.
# So 90 is up, 270 is down, 180 is left, 0 is right.


def init_game():
    """ Initialise game settings """
    pygame.init()
    # Set the caption on the Window
    pygame.display.set_caption("Breakout!")


def setup_screen():
    """ Setup the screen objects and layout the display
     :returns pygame screen, pygame bg_screen """
    screen = pygame.display.set_mode((GAME_SCREEN[0], GAME_SCREEN[1]))
    # Blank screen & create background screen as well
    # So the we have something to put under moving things
    screen.fill(0)
    # Get the dimensions of the BG image, so we can try and centre it somewhat
    bgx, bgy = int(GAME_SCREEN[0] / 2) - int(BACKGROUND_IMG.get_width() / 2), \
               int(GAME_SCREEN[1] / 2) - int(BACKGROUND_IMG.get_height() / 2)
    screen.blit(BACKGROUND_IMG, [bgx, bgy])
    bg_screen = pygame.Surface((GAME_SCREEN[0], GAME_SCREEN[1]))
    bg_screen.blit(BACKGROUND_IMG, [bgx, bgy])

    return screen, bg_screen


def generate_wall():
    """ Create the Wall, a group of bricks
     :return wall -> pygame.sprite.Group() object of bricks """

    wall = pygame.sprite.Group()
    for y_pos in range(10, 5 * BRICK_IMG.get_height(), BRICK_IMG.get_height()):
        for x_pos in range(round(GAME_SCREEN[0] / BRICK_IMG.get_width() - 1)):
            wall.add(Block(BRICK_IMG, (10 + (x_pos * (BRICK_IMG.get_width() + 1))), y_pos))

    return wall


def process_event(player, goleft=False, goright=False):
    """ Process the player input event. Assumes False, unless explicitly set True
    :param (required) player object
    :param (optional) goleft=False
    :param (optional) goright=False
    :return None
    """

    # FIX (https://github.com/damian-murphy/breakout/issues/2)
    # Get the bat position, check if it's at the edge, adjust accordingly.
    # and make sure we don't move outside the play area, or the bat will disappear off screen
    if goleft:
        if (player.get_left_hand_side() < 10) & (player.get_left_hand_side() > 0):
            player.moveleft(10 - player.get_left_hand_side())
        elif player.get_left_hand_side() == 0 or player.get_left_hand_side() < 0:
            player.moveleft(0)
        else:
            player.moveleft(10)
    elif goright:
        if (player.get_right_hand_side() > (GAME_SCREEN[0] - 10)) \
                and (player.get_right_hand_side() < GAME_SCREEN[0]):
            player.moveright(10 - (GAME_SCREEN[0] - player.get_right_hand_side()))
        elif player.get_right_hand_side() == GAME_SCREEN[0] \
                or player.get_right_hand_side() > GAME_SCREEN[0]:
            player.moveright(0)
        else:
            player.moveright(10)


def clear_callback(surf, rect):
    """ Callback function to reset the screen to background, wiping the sprite """
    surf.fill(BGCOLOUR, rect)


def check_collisions(sprite, group):
    """ Check for collisions between two sprite groups
    :param sprite: A pygame sprite object
    :param group: A group of sprite objects that 'sprite' might have collided with
    :returns Three values, the x and y position of the detected hit and True, otherwise 0,0,False
    """
    d_x = 0
    d_y = 0

    if pygame.sprite.spritecollide(sprite, group, False):
        try:
            for sprite_n in iter(group.sprites()):
                if sprite_n.rect.colliderect(sprite.rect):
                    (hitx, hity) = pygame.sprite.collide_mask(sprite, sprite_n)
                    ic("collide_mask:", hitx, hity)

                    diff_x = sprite.rect.x - sprite_n.rect.centerx
                    diff_y = sprite.rect.y - sprite_n.rect.centery

                    v_dir = sprite.get_direction()

                    if abs(diff_x) > abs(diff_y):
                        d_x = sprite_n.rect.left - (sprite.rect.width/2) \
                            if diff_x < 0 else sprite_n.rect.right + (sprite.rect.width/2)
                        if (diff_x < 0 and v_dir[0] > 0) or (diff_x > 0 and v_dir[0] < 0):
                            v_dir.reflect_ip(pygame.math.Vector2(1, 0))
                    else:
                        d_y = sprite_n.rect.top - (sprite.rect.width/2) \
                            if diff_y < 0 else sprite_n.rect.bottom + (sprite.rect.width/2)
                        if (diff_y < 0 and v_dir[1] > 0) or (diff_y > 0 and v_dir[1] < 0):
                            v_dir.reflect_ip(pygame.math.Vector2(0, 1))

                    if sprite_n.hit() == 0:
                        group.remove(sprite_n)
                    return d_x, d_y, v_dir, True

        except TypeError:
            return 0, 0, None, False  # zero, zero, False means no hit
    return 0, 0, None, False  # zero, zero, False means no hit


def main():
    """ Main Loop """
    # Call the init function of pygame, and set up some game state basics.
    # Putting it in a procedure here to keep things cleaner
    init_game()

    # Used to manage how fast the screen updates
    # Really handy, because this isn't a ZX Spectrum we're running on where I had to worry
    # about screen flicker and getting things done in 1/50sec
    clock = pygame.time.Clock()

    # Create the display surface
    screen, bg_screen = setup_screen()

    # Create player1, a controlled sprite
    player1 = Player(BAT_IMG, BAT_IMG.get_width(), BAT_IMG.get_height())
    players = pygame.sprite.GroupSingle(player1)
    # Create the ball, a moving sprite.
    the_ball = Ball(BALL_IMG, GAME_SCREEN[0], GAME_SCREEN[1])

    # Group of balls.
    balls = pygame.sprite.Group(the_ball)

    # If we're running in debug mode, then setup the debugger. Otherwise, eh, don't.
    if DEBUG:
        debugger = DebugBox(screen, GAME_SCREEN[1])

    # Create the Wall of blocks
    wall = generate_wall()

    # Set the player sprite starting position
    # Draw our player
    # player1.rect.x = 390
    player1.rect.x = 10
    player1.rect.y = 560

    # Set the starting player health
    player1.set_lives(PLAYER_HEALTH)

    # Draw the player sprite
    players.draw(screen)
    balls.draw(screen)
    wall.draw(screen)

    # Container for keypresses, to allow us to change on key down/up and maintain
    # a repetitive action, i.e. pressing left will keep moving left until key is released
    # Otherwise, we detect keydown, move once, stop. Not what you expect in an arcade game
    keys_pressed = {
        'left': False,
        'right': False,
        'fire': False
    }

    while 1:

        # Limit to 60 frames per second. Call this once per frame only.
        clock.tick(TICKS)

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
                    keys_pressed['left'] = True
                elif event.key == pygame.K_x:
                    keys_pressed['right'] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_z:
                    keys_pressed['left'] = False
                elif event.key == pygame.K_x:
                    keys_pressed['right'] = False

        # Do the player actions
        process_event(player1, goleft=keys_pressed['left'], goright=keys_pressed['right'])

        # Check if player has any health left
        if the_ball.hit_floor():
            player1.hit(FLOOR=True)
        if player1.hit() <= 0:
            pygame.quit()

        # Check for collisions and do movement
        # Bat and ball(s)
        for a_ball in balls:
            hit_x, hit_y, new_vector, is_hit = check_collisions(a_ball, players)
            ic("Premove on bat hit", hit_x, hit_y, is_hit)
            if is_hit:
                a_ball.move(hit_x, hit_y, new_vector, is_hit)
            else:
                a_ball.move(hit_x, hit_y, None, is_hit)

        # Primary ball and the wall bricks
        hit_x, hit_y, new_vector, is_hit = check_collisions(the_ball, wall)
        the_ball.move(hit_x, hit_y, new_vector, is_hit)

        ic(the_ball.rect.x, the_ball.rect.y, player1.rect.x, player1.rect.y,
           the_ball.rect.width, the_ball.rect.height, player1.rect.width, player1.rect.height)

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
            debugmessage = f"P {player1.rect.x:>4.0f},{player1.rect.y:>4.0f} " \
                           f"B {the_ball.rect.x:>4.0f},{the_ball.rect.y:>4.0f} " \
                           f"V {the_ball.speed():>4.0f} " \
                           f"FT {clock.get_rawtime():>4.0f}ms FR {clock.get_fps():>4.0f} frames/sec"
            debugger.message(debugmessage)


if __name__ == "__main__":
    main()
