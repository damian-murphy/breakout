""" Player Class Object """
import pygame

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
