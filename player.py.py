## Characters in Game
import pygame
import random

pygame.mixer.init()         # to load sounds

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

class Player(pygame.sprite.Sprite):
    ''' The Player Class creates a sprite object of an image (a camel, a flamingo, or dinosaur) that
        will back and forth, jump, duck, and die. Inspired by the player class in RealPython's simple
        pygame tutorial with some modifications
        [https://realpython.com/pygame-a-primer/#note-on-sources]'''
  
    def __init__(self, level, screen):
        ''' Creates a Player sprite by loading an image chosen based on level from a list of
            camel (level 1), flamingo (level 2), and dinosaur (level 3). It spawns and drops about 3/4
            to the bottom of the screen, and has set values to aid the jumping and ducking.
            Takes no parameters. Does not return. '''
        
        super(Player, self).__init__()      # supercharge the class 
        if level == 1:          # load image based on chosen level
            self.surf = pygame.image.load("camel_character.png").convert()
            
        elif level == 2:
            self.surf = pygame.image.load("flamingo.png").convert()
            
        elif level == 3:
            self.surf = pygame.image.load("dinosaur.png").convert()

        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # black colorkey fades the png bakcground
        # RLEACCEL to make the sprite move more fluidly 
        self.rect = self.surf.get_rect()
        self.rect.move_ip(0, + 500)     # drop the sprite right on top of the road

        self.isJump = False         # set variables for jumping
        self.jumpCount = 12

        self.isDuck = False         # set variables for ducking
        self.duckCount = 10

    def update(self, pressed_keys, w):
        ''' Updates the characters position according to the given key presses. Player sprite
            can move left, move right, jump, and duck. The Player sprite cannot move beyond the
            boundaries of the screen. Plays sound effect with each movement. Takes 2
            parameters: list of key presses and width of surface(w). Does not return. '''
        
        jumpSound = pygame.mixer.Sound("jump.mp3") # load jumping and ducking sound
        duckSound = pygame.mixer.Sound("duck.mp3")
        
        jumpSound.set_volume(0.15) # set volume

        if(self.rect.x >= (w - 100)):   # stop player from going beyond the edges of the screen
            self.rect.x -= 10
        elif(self.rect.x <= 0):
            self.rect.x += 10

        else:
            if pressed_keys[K_LEFT]:        # move character side to side based on left and right arrow key hits
                self.rect.move_ip(-10, 0)
                
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(+10, 0)


                ## the mathematical implementation of jumping is from Tech with Tim's
                ## tutorial on jumping and coming back down [https://www.youtube.com/watch?v=2-DNswzCkqk]
                
            if not (self.isJump):       # if the player is not already jumping (prevents double jump)
                if pressed_keys[K_UP]:      # if they hit the upward arrow key
                    jumpSound.play()            # play jump sound
                    self.isJump = True        # set jumping variable to true  
                    
            elif self.isJump:       
                if self.jumpCount >= -12:     # variable to create arch  
                    neg = 1                 # sprite moves upward
                    if self.jumpCount < 0:      # peak reached
                        neg = -1            # sprite moves downward
                    self.rect.y -= (self.jumpCount ** 2) * 0.5 * neg    
                    self.jumpCount -= 1     # increment jumpCount to keep player moving
                else: 
                    self.isJump = False    # jump is complete 
                    self.jumpCount = 12     # reset jumpCount for next jump

            if not (self.isDuck):       # if not already ducking (prevents double ducks)
                if pressed_keys[K_DOWN]:    # if player hits downward arrow key
                    duckSound.play()        # play duck sound
                    self.isDuck = True      # set ducking variable to true


                    ## the mathematical implementation of ducking is adopted
                    ## from the previous jumping implementation
            elif self.isDuck:       
                if self.duckCount >= -10:       # variable to create arch
                    neg = 1             # sprite moves downward
                    if self.duckCount < 0:          # peak reached
                        neg = -1            # sprite moves back upward
                    self.rect.y += (self.duckCount ** 2) * 0.5 * neg
                    self.duckCount -= 1         # increment duckCount to keep player moving
                else: 
                    self.isDuck = False         # duck is complete
                    self.duckCount = 10         # reset duckCount for next duck
                    
    def die(self, screen):          # show blood splatter for if the player collides with an obstacle
        ''' Loads and displays an image of blood splatter on top of the Player sprite
            to simulate violent death. Takes 1 parameter: the surface to blit onto. Does
            not return. '''
        
        surf = pygame.image.load("blood_splatter.png").convert()
        surf.set_colorkey((0,0,0), RLEACCEL)
        bloodrect = surf.get_rect()
        bloodrect.x = self.rect.x
        bloodrect.y = self.rect.y
        screen.blit(surf, bloodrect)
