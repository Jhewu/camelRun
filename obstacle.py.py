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

# Define the enemy object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite
class Obstacle(pygame.sprite.Sprite):
    ''' The Obstacle Class creates a sprite object of an image (a rock, a bird, or poop) that
        will move from right to left on the screen and then disappear. Inspired by 
        Real Python's simple pygame tutorial with some modifications
        [https://realpython.com/pygame-a-primer/#note-on-sources]'''
  
    def __init__(self, w,h):
        ''' Creates an obstacle sprite by loading an image chosen randomly from a list of
            rock, bird, and poop and then randomly generating it within specific boundaries,
            at a random speed from 5 to 20. Takes two parameters: width (w) and height (h) of the
            surface. Does not return. '''

        super(Obstacle, self).__init__()    # supercharge the class
        
        obstacleList = ["rock.png", "bird_structure.png", "poop_emoji.png"]
        # create a list of all obstacle images
        
        self.surf = pygame.image.load(random.choice(obstacleList)).convert()
            # randomly decide what obstacle to send in
        self.surf.set_colorkey((0,0,0), RLEACCEL)
            # colorkey is black to fade the png background
            # RLEACCEL to make the sprite move more fluidly
        
        self.rect = self.surf.get_rect(
            center=(            # origin position is randomly generated within the bounds of the road
                random.randint(w + 20, w + 100),
                random.randint(h - 350, h - 150),
            )
        )
        self.speed = random.randint(5, 20)      # speed at which obstacle moves is random as well


    def update(self):
        ''' Updates position of obstacle sprite by moving the obstacle sprite along the screen
            from right to left, killing it once it goes beyond the left edge. Takes no parameters.
            Does not return. '''        
        self.rect.move_ip(-self.speed, 0)       # move the obstacle to the left 
        if self.rect.right < 0:         # kill it if it goes beyond the left edge
            self.kill()
    
