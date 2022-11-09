""" Wall Class - The wall as a collection of brick objects """
import pygame

WHITE = (255, 255, 255)


class Block(pygame.sprite.Sprite):
    """ block: pass in the colour of the block, and it's x,y position """

    def __init__(self, image, init_x, init_y):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([image.get_width(), image.get_height()])
        self.image = image
        self.image.set_colorkey(WHITE)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image.convert_alpha())
        self.rect.x = init_x
        self.rect.y = init_y

        self._attribs = {
            'health': 1
        }

    def setimage(self, image):
        """ Set the block image to 'image' """
        self.image = image

    def hit(self):
        """ Brick loses 1 health on hit,
        Allows us to have blocks that need more than one hit to destroy.
        Return the health left """

        self._attribs['health'] -= 1
        return self._attribs['health']


# class Wall:
#     """    # Constructor.
#     # Pass in the block image, width and height, also , screen width
#     # Returns a list of block objects of wall (num x rows)
#     """
#
#     def __init__(self, screen, image, width, height, screen_width, rows):
#
#         for y_pos in range(10, rows * height, height):
#             for x_pos in range(round(screen_width / width - 1)):
#                 screen.blit(image, (10 + (x_pos * (width + 1)), y_pos))
#                 # WallArray[xy] = (x,y)
#                 # Create a group of sprites to represent the wall
