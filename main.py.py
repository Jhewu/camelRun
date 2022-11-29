##Jun Yi He Wu and Tahsin Tasnim
##COM 110: Final project - Camel Run
## Due: 20 Dec 2021
##This program creates a cool running game with different characters,
##themes, and soundtracks!

import pygame
import sys
from pygameButton import button
from player import Player
from obstacle import Obstacle
from coin import Coins


from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    K_BACKSPACE,
    QUIT,
)

pygame.init()
pygame.mixer.init()

# loaded sound library 
                                           
def createText(screen, label, fontsize, fontcolor, x, y):
    font = pygame.font.SysFont('Corbel', fontsize)
    text = font.render(label, 1, fontcolor)
    screen.blit(text, (x, y))

def BeginPage(screen):

    pygame.mixer.music.load("menu_music.mp3")   # set up the background music 
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

    background = pygame.image.load('desert_background.png')
    background_rect = background.get_rect()         # load and blit the background image 
    screen.blit(background, background_rect)

    # ------------------------------------------
    
    background_size = background.get_size()
    background_rect = background.get_rect()
    screen = pygame.display.set_mode(background_size)

    w,h = background_size
    x = 0           # size up the background according to the image
    y = 0           # set variables to continuously place the background behind itself
                    # idea from Stack Overflow [https://stackoverflow.com/questions/17240442/how-to-make-the-background-continuously-scrolling-with-pygame]
    x1 = -w
    y1 = 0

    # ------------------------------------------

    font = pygame.font.SysFont('Corbel', 30)
    usertext = 'Default User'                   # render text to show user's input
    inputrect = pygame.Rect(350,400,350,40)     # text box surrounding user input
    
    continuebtn = button(320, 500, 250,70, 'Continue')

    run = True
    
    while run:        
        # ------------------------------------------

        x1 += 5         # to make the background continuously roll
        x += 5

        screen.blit(background,(x,y))
        screen.blit(background,(x1,y1))
        
        if x > w:
            x = -w
        if x1 > w:
            x1 = -w

        # ------------------------------------------

        continuebtn.draw(screen)

        title = pygame.image.load('camelrun.png').convert()     
        title.set_colorkey((0, 0, 0), RLEACCEL)     # load and display title image
        screen.blit(title, (175,10))
        
        createText(screen, 'Type your name to get started!', 40, (0,0,0), 200,325)

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()    # get the mouses position
            if event.type == pygame.QUIT:       # if the user clicks the X button
                pygame.quit()       # end everything
                sys.exit()

            continuebtn.isOver(screen, event, pos)      # to let the mouse position interact with button
            
            if continuebtn.isClicked(screen, event, pos):   # if the user has entered name and clicked continue
                name = usertext         # store user input as name
                
                user_rec = open('user_record.txt', 'r')
                user_rec.seek(0)                # open and read the file of past users
                rec_list = user_rec.readlines()

                coins = 0           # default values for coins and highest score is 0
                hScore = 0
                for line in rec_list:
                    x = line.split(',')
                    if name == x[0]:        # if name is already in the user record
                        coins = int(x[1])   # latest coin value will = coins
                        hScore = int(x[2])   # latest score value will = coins                         

##                print(name, coins, hScore)
                user_rec.close()
                        
                screen.blit(background, background_rect)
                return name, coins, hScore

                    # Modeled after Clear Code's tutorial on getting text input
                    # [https://www.youtube.com/watch?v=Rvcyf4HsWiw]
            if event.type == pygame.KEYDOWN:    # if the user presses down on a key
                if event.key == pygame.K_BACKSPACE:     # if the key is backspace
                    usertext = usertext[0:-1]       # reassign usertext without the last character
                else:
                    usertext += event.unicode       # translate each key hit into its unicode letter and add to usertext
                    
        text_surface = font.render(usertext, True, (0,0,0))     # render text and adjust the text box
    
        screen.blit(text_surface, (inputrect.x + 5, inputrect.y + 5))

        inputrect.w = text_surface.get_width() + 10 
        
        pygame.draw.rect(screen, (0,0,0), inputrect, width=2, border_radius=3)
         
        pygame.display.flip()


level = 1           # default value for level is 1 (player will take camel character with desert bg)

def MenuPage(screen, coins, level, name, hScore):
##    print('menu:', name, coins, hScore)
    introbtn = button(300, 150, 250,70, 'Introduction')
    introbtn.draw(screen)
    seecharbtn = button(300, 350,  250,70, 'See Skins')
    seecharbtn.draw(screen)
    startbtn = button(300, 550,  250,70, 'Start Game')
    startbtn.draw(screen)

    createText(screen, ('TOTAL COINS : ' + str(coins)), 30, (0,0,0), (620), (80))  
    createText(screen, ('HIGHEST SCORE : ' + str(hScore)), 30, (0,0,0), (40), (80))

    run = True
    
    while run:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False

            introbtn.isOver(screen, event, pos)         # let the mouse interact with the buttons 
            seecharbtn.isOver(screen, event, pos)
            startbtn.isOver(screen, event, pos)
            
            if introbtn.isClicked(screen, event, pos):      # if intro is clicked
                Intro(screen, coins, level, hScore, name)       # call Intro function
                
            if seecharbtn.isClicked(screen, event, pos):    # if you want to see character skins
                CharDisplay(screen, coins, level, hScore, name)     # call CharDisplay function
                
            if startbtn.isClicked(screen, event, pos):      # if start is clicked
                pygame.mixer.music.stop()               # stop main bg music
                Game(level, coins, hScore, name)        # call Game function

        pygame.display.update()
                
    pygame.quit()
    sys.exit()



def Intro(screen, coins, level, hScore, name):
    background = pygame.image.load('intro.png')     # load and display the inroduction background
    background_rect = background.get_rect()
    screen.blit(background, background_rect)
    
    instructions = ['You will become one of our characters to', 'evade multiple obstacles in your path', 'that will try to keep',
                    'you from reaching the next world!', 'Evade all your enemies to reach', 'the end of the desert, into the beach',
                    'into the abandoned city,','until you reach the stars!']
    space = 0
    for i in instructions:
            createText(screen, i, 35, (0,0,0), 175, 165 + space)
            space = space + 50      # display the instructions
    
    gotitbtn = button(450, 600, 200, 60,'Got It!')
    gotitbtn.draw(screen)
    
    arrowkeys = pygame.image.load('arrows.png')     # add an image of arrow keys to indicate 
    arrowkeys_rect = arrowkeys.get_rect()           # that those are the keys to move around
    arrowkeys_rect.move_ip(+5, + 500) 
    screen.blit(arrowkeys, arrowkeys_rect)    

    run = True
    
    while run:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            gotitbtn.isOver(screen, event, pos)         # let mouse interact with button
            
            if gotitbtn.isClicked(screen, event, pos):
                background = pygame.image.load('desert_background.png')
                background_rect = background.get_rect()         # reset background before calling MenuPage again
                screen.blit(background, background_rect)
                MenuPage(screen, coins, level, name, hScore)
                run = False

        pygame.display.update()


def CharDisplay(screen, coins, level, hScore, name):

        awwwSound = pygame.mixer.Sound("aww.mp3") # loading the sound  
    
##        print('char:', coins, hScore)
        background = pygame.image.load('bubbles.png')       # load and display the character display background
        background_rect = background.get_rect()
        screen.blit(background, background_rect)

        createText(screen, ('COINS : ' + str(coins)), 30, (0,0,0), (700), (20))
        createText(screen, 'Choose a skin!', 60, (0,0,0), 300, 100)         # display total coin value

        donebtn = button(350, 600, 200, 60,'Done!')
        donebtn.draw(screen)

        firstbtn = button(175, 500, 200, 50,'This one!')
        secondbtn = button(375, 500, 200, 50,'This one!')
        thirdbtn = button(575, 500, 200, 50,'This one!')
        
        firstbtn.draw(screen)

        if 150 <= coins < 250:
            secondbtn.draw(screen)      # show buttons to chose a character based on coin total

        elif coins > 250:
            secondbtn.draw(screen)
            thirdbtn.draw(screen)
            
        firstSkin = Player(1, screen)
        firstSkin.rect.move_ip(200,-200)

        secondSkin = Player(2, screen)
        secondSkin.rect.move_ip(400,-200)        

        thirdSkin = Player(3, screen)
        thirdSkin.rect.move_ip(600,-200)

        createText(screen, '150C Milestone!', 30, (0,0,0), 375, 250)        # 150C to access flamingo
        createText(screen, '250C Milestone!', 30, (0,0,0), 600, 250)        # 250C to access dinosaur

        all_sprites = pygame.sprite.Group()         # group all sprites together to blit them together
        all_sprites.add(firstSkin)
        all_sprites.add(secondSkin)
        all_sprites.add(thirdSkin)
        for i in all_sprites:
            screen.blit(i.surf, i.rect)     

        run = True
        level = 1   # default level is 1, the camel and beach
        
        while run:
                for event in pygame.event.get():
                    pos = pygame.mouse.get_pos()
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    donebtn.isOver(screen, event, pos)      # let mouse interact with button
                    
                    if firstbtn.isClicked(screen, event, pos):      # if the first button is clicked 
                        awwwSound.play()            # play cute sound    
                        level = 1                   # user chose camel 

                    if 150 <= coins < 250:
                        if secondbtn.isClicked(screen, event, pos):     # if second button is clicked
                            awwwSound.play()        # play cute sound
                            level = 2               # user chose flamingo
                            
                    if coins > 250:
                        if secondbtn.isClicked(screen, event, pos):     
                            awwwSound.play()       
                            level = 2
                        elif thirdbtn.isClicked(screen, event, pos):    # if third button is clicked
                            awwwSound.play()        # play cute sound
                            level = 3               # user chose dinosaur
                        
                    if donebtn.isClicked(screen, event, pos):       # if done is clicked, player is finished chosing
                        background = pygame.image.load('desert_background.png')     # reset background
                        background_rect = background.get_rect()
                        screen.blit(background, background_rect)
                        MenuPage(screen, coins, level, name, hScore)        # call MenuPage
                        
                pygame.display.update()

def Game(level, coins, hScore, name):               # game is in session
    level = int(level)                      
    coins = int(coins)
    
    if level == 1:              # camel and desert
        pygame.mixer.music.load("desert_music.mp3")
        pygame.mixer.music.set_volume(0.8) # set volume 
        pygame.mixer.music.play(-1)
        
    if level == 2:              # flamingo and beach
        pygame.mixer.music.load("beach_music.mp3")
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play(-1)

    if level == 3:              # dinosaur and jungle
        pygame.mixer.music.load("jungle_music.mp3")
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play(-1)

    collideSound = pygame.mixer.Sound("collide.mp3") # loading the sounds
    ouchSound = pygame.mixer.Sound("ouch.mp3")
    loseSound = pygame.mixer.Sound("lose_music.mp3")
    coinSound = pygame.mixer.Sound("coin.mp3")

##    print('game:', name, coins, hScore)
    clock = pygame.time.Clock()

    bg_list = ['desert_background.png', 'beach.png', 'jungle.png']  
    
    background = pygame.image.load(bg_list[level - 1])      # display the background for the given level
    
    background_size = background.get_size()
    background_rect = background.get_rect()
    screen = pygame.display.set_mode(background_size)           # set background

    w,h = background_size           # variables to put the bg images one behind the other
    x = 0
    y = 0

    x1 = -w
    y1 = 0

    # create custom events with for adding things in the run
    ADDTHINGS = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDTHINGS, 2200)        # add either an obstacle or a coin every 2200ms

    # load the user's character 
    player = Player(level, screen)

    # create different sprite groups to hold all sprites (makes it easier for rendering and controlling)
    obstacles = pygame.sprite.Group()       # used for player collision and position updates
    coin_sprites = pygame.sprite.Group()    # used for player collision
    all_sprites = pygame.sprite.Group()         # add all together 
    all_sprites.add(player)

    screen.blit(background, background_rect)

    score = 0       # start score and coin values are 0
    game_coins = 0 
    pygame.display.update()
        
    running = True

            ## basic setup of game while loop is modeled after the game code provided
            ## in Real Python's simple pygame tutorial [https://realpython.com/pygame-a-primer/#note-on-sources]
    while running:

        x1 += 5         # keep the background continually rolling
        x += 5

        screen.blit(background,(x,y))
        screen.blit(background,(x1,y1))
        
        if x > w:
            x = -w
        if x1 > w:
            x1 = -w

        # display score and coin values at the top of the screen
        createText(screen, ('SCORE : ' + str(score)), 30, (0,0,0), (90), (30))
        createText(screen, ('COINS : ' + str(game_coins)), 30, (0,0,0), (w - 250), (30))
        coinImage = pygame.image.load("coin.png")
        screen.blit(coinImage, (w - 350, 0))
        clockImage = pygame.image.load("clock.png")
        screen.blit(clockImage, (10, 10))

        for event in pygame.event.get():            # check every event in the event queue
            if event.type == QUIT:          # if the user hit X
                running = False             # end everything
                pygame.quit()
                sys.exit()

            elif event.type == ADDTHINGS:       # unique event to add obstacles or coins every 2200ms 
                newObstacle = Obstacle(w,h)     # create obstacle and add to group
                obstacles.add(newObstacle)      
                all_sprites.add(newObstacle)

                newCoin = Coins(w,h)        # create coin and add to group
                coin_sprites.add(newCoin)
                all_sprites.add(newCoin)


        pressed_keys = pygame.key.get_pressed()     # check all the keys that were pressed by user
        player.update(pressed_keys, w)          # update player position based on keys hit

        obstacles.update()          # update positions of obstacles and coins
        coin_sprites.update()

        for i in all_sprites:              # blit all items in the all_sprites group onto screen
            screen.blit(i.surf, i.rect)

        for c in coin_sprites:          # for every coin in the group
            if pygame.sprite.spritecollideany(player, coin_sprites):    # if the player collides with a coin
                c.consume()         # consume(aka kill) the coin so it disappears
                coinSound.play()        # play coin sound
                game_coins = game_coins + 10        # increment game_coins value by 10
            
        if pygame.sprite.spritecollideany(player, obstacles): # if the player collides with an obstacle
            collideSound.play()     # play collision sound
            ouchSound.play()        # play ouch sound
            loseSound.play()        # play loser sound

            pygame.mixer.music.stop() # stop background music 

            player.die(screen)      # show blood splatter and kill player
            player.kill()
            
            coins = coins + game_coins      # update total coin value by amount gained in game
            if score > hScore:          # if current score beats highest score, update highest score
                hScore = score
                
            testfile = open('user_record.txt', 'r')
            test_list = testfile.readlines()        # open and read user record of past players and stats
            testfile.seek(0)
            testfile.close()

            testfile = open('user_record.txt', 'w')
            testfile.seek(0)
            for line in test_list:
                x = line.split(',')
                if name != x[0]:    # rewrite every line of the file excluding the one for the current user
                    testfile.write(line)

##            print((str(name) + ',' + str(coins)))   
            
            text_to_append = (str(name) + ',' + str(coins) + ',' + str(hScore) + '\n')
            testfile.write(text_to_append)      # append new line with user's updated stats to the end of the record
            testfile.close()

            # Stop the loop
            running = False
            
        score = score + 60         # increment the score

        pygame.display.flip()

        # Ensure we maintain a 20 frames per second rate
        clock.tick(20)

    MenuPage(screen, coins, level, name, hScore)    # once player dies, show Menu again to give the option to play again


def main():
    # create initial screen
    screen = pygame.display.set_mode((900,708))     
        
    name, coins, hScore = BeginPage(screen)
    ##print('first"',name, coins, hScore)
    MenuPage(screen, coins, level, name, hScore)

main()
