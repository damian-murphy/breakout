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
        self.mask = pygame.mask.from_surface(self.image.convert_alpha())
        self.mask.fill()  # set all bits to 1 in the mask, otherwise transparency makes things wonky

        self._attribs = {
            'health': 0
        }

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

    def hit(self):
        """ Hit/Life counter loses 1 health on hit,
        Allows us to have objects that need more than one hit to destroy.
        Return the health left
        This is the 'player lives' """

        self._attribs['health'] -= 1

        return self._attribs['health']

    def set_lives(self, number):
        """ Add number to the player lives left
        Can be used to add/subtract bonus lives, and is used at the start to set the
        default number of lives
        Calling this with number = 0 will return the health left (no action)
        ::param number - integer to be added or removed (if negative) from the 'health' counter
        ::return resulting health value """

        self._attribs['health'] += number
        return self._attribs['health']
