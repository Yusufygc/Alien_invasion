import pygame

class Ship():
    """ A class to manage the ship. """

    def __init__(self,ai_game):
        """ Initialize the ship and set its starting position. """
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect() # get_rect() method to access the screen’s rectangle attribute.
        self.moving_right = False # Movement flag
        self.moving_left = False
        
        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/ottomans.bmp')
        self.rect = self.image.get_rect() # get_rect() method to access the ship’s surface rectangle.

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom # The ship’s midbottom attribute is set to match the midbottom attribute of the screen’s rectangle.

        self.settings = ai_game.settings
        self.x = float(self.rect.x) # Store a decimal value for the ship’s horizontal position.
    
    def update(self):
        """ Update the ship's position based on the movement flag. """
        # self.rect.right returns the x-coordinate of the right edge of the ship’s rect.
        # self.screen_rect.right returns the x-coordinate of the right edge of the screen.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed # Update the ship’s x value, not the rect.

        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed # Update the ship’s x value, not the rect.
           
        
        # Update rect object from self.x
        self.rect.x = self.x



    
    def blitme(self):
        """ Draw the ship at its current location. """
        # blitme() draws the image to the screen at the position specified by self.rect.
        self.screen.blit(self.image,self.rect)

   