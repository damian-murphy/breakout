# Wall class
import pygame

WHITE = (255,255,255)

class Block(pygame.sprite.Sprite):
    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, image, width, height, init_x, init_y ):
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
        self.rect.x = init_x
        self.rect.y = init_y

class Wall():
    # Constructor.
    # Pass in the block image, width and height, also , screen width
    # Returns a list of block objects of wall (num x rows)
    #WallArray = ()

    def __init__(self, screen, image, width, height, screen_width, rows):

        for y in range(10, rows * height, height):
            for x in range(round(screen_width / width - 1)):
                screen.blit(image, (10 + (x * (width + 1)), y))
                #WallArray[xy] = (x,y)
                # Create a group of sprites to represent the wall


