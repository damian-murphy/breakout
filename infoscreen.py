""" Setup the screen border and overlay for information """


class InfoScreen:
    """ InfoScreen Class:
        Display the game 'console' - anything that isn't a player graphic
        """

    def __init__(self, image, screenx, screeny):
        # Constructor for console display - anything that isn't a player graphic
        self.border_image = image
        self.screen_x = screenx
        self.screen_y = screeny

    def border(self):
        """ Draw or update the border area """
        return 0

    def scoreboard(self):
        """ Draw or update the scoreboard & lives """
        return 0
