## Characters in Game
import pygame
import random

# Import pygame.locals for easier access to key coordinates
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_SPACE,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

class Coins(pygame.sprite.Sprite):
    ''' The Coins class creates a sprite object of a coin, which is spawned and then
        moves across a screen once from right to left, then disappears. Inspired by 
        Real Python's simple pygame tutorial (although it does not include coins or money)
        [https://realpython.com/pygame-a-primer/#note-on-sources]'''

    def __init__(self, w,h):
        ''' Creates a coin sprite by loading an image of a coin and randomly
            generating it within specific boundaries, at a random speed from 5 to 20.
            takes two parameters: width (w) and height (h) of the surface. Does not return. '''
            
        super(Coins, self).__init__()   # supercharging out class

        self.surf = pygame.image.load("coin.png").convert()
        self.surf.set_colorkey((0,0,0), RLEACCEL)
            # a black colorkey gets rid of the png background of the images
            # RLEACCEL allows the characters to move more fluidly
        
        self.rect = self.surf.get_rect(
            center=(            # origin position is randomized within the given bounds of the road
                random.randint(w + 20, w + 100),
                random.randint(h - 350, h - 150),
            )
        )
        self.speed = random.randint(5, 20)      # speed at which the coins move is also randomized

    def update(self):
        ''' Updates the position of the coin sprite by moving the coin sprite along the screen
            from right to left, killing it once it goes beyond the left edge. Takes no parameters.
            Does not return. '''
        self.rect.move_ip(-self.speed, 0)   # move the character to the left along the road
        if self.rect.right < 0:     # kill if it moves past the end of the screen
            self.kill()

    def consume(self):          # kill coin sprite, for when player collides with coin
        '''Kills the coin sprite, before it leaves screen.'''
        self.kill()

    
