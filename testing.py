import pygame
from pygame.locals import *
import sys
import time
import pyganim
import random

class Player(pygame.sprite.Sprite):
    """player parent class"""
    # Set speed vector
    change_x = 0
    change_y = 0
    
    def __init__(self, x, y):

        pygame.sprite.Sprite.__init__(self)
       
        self.images = ["hero1.png","hero2.png","hero3.png"]

        # Set height, width
        
        self.image = pygame.image.load(self.images[0]).convert()
        
        self.image = pygame.transform.scale(self.image,(33, 43))
        
        self.image = pygame.transform.flip(self.image, 180, 0)
        
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        
    def changespeed(self, x, y):
        """ Change the speed of the player. Called with a keypress. """
        self.change_x += x
        self.change_y += y

    def move(self):
        """ Find a new position for the player """

        # Move left/right
        self.rect.x += self.change_x
                
        # Move up/down
        self.rect.y += self.change_y        

class Luffy (Player): 
    '''Defines the attributes of a Luffy in the game. Inherits the constructor and methods
    of the Player class '''
    def __init__(self, x, y, name):
        Player.__init__(self, x, y, name)

        self.level = 1
        self.max_health = 500
        self.max_mana = 500
        self.attack = 5 
        self.defense = 10 
        self.health = self.max_health
        self.mana = self.max_mana
        self.mana_potions = 1
        self.health_potions = 1
        self.gold = 0
        self.experience = 0       

def main(WIDTH, HEIGHT):
    """main loop"""
    pygame.init() 

    #remain the resolution as the previous file has
    if WIDTH == 1366 and HEIGHT == 767:
        screen = pygame.display.set_mode((WIDTH, HEIGHT), FULLSCREEN)
    else:
        screen = pygame.display.set_mode((WIDTH, HEIGHT),0 ,32)
    
    #set the title
    pygame.display.set_caption("Unimaginable Powers!!!")

    rightNow = time.clock() #get the instant time
    
    WHITE = (255, 255, 255)
    BGCOLOR = (100, 50, 50)


    hero1 = pygame.image.load("hero1.jpg").convert()
    hero2 = pygame.image.load("hero2.jpg").convert()
    hero3 = pygame.image.load("hero3.jpg").convert()
    
    anime = pyganim.PygAnimation([(hero1, 5),
                                  (hero2, 5),
                                  (hero3, 5)])#loop once by adding "loop = False"
    anime.set_colorkey((0,0,0))
    
    #copy animation
    anime1, anime2, anime3 = anime.getCopies(3)
    
    #set the speed of the each animation
    anime.rate = 1
    anime2.rate = 2.5
    animes = [anime, anime1, anime2, anime3]
    

    #set the angle
    anime3.rotate(50)
    spining = 0
    
    #need to convert the image to get rid off default aplha value , then set the transparent
    anime.set_colorkey((0,0,0)) #set black as a transparent color
    anime.set_alpha(50)
    anime.scale((200,200))
    anime.play()

    

    print(anime.getRect())

    
    for each_anime in range(len(animes)):
        if each_anime == 0:
            continue   #skip playing anime2
        animes[each_anime].scale((200,200))#Bigger size
        animes[each_anime].convert() #convert image to pixel
        animes[each_anime].set_alpha(50)
        animes[each_anime].play(rightNow) #make each anime play in sync
        
    
    """---movement images---"""
    # load the "standing" sprites (these are single images, not animations)
    front_standing = pygame.image.load("hero1.jpg")
    front_standing = pygame.transform.scale(front_standing, (200,200))
    
    back_standing = pygame.image.load("hero1.jpg")
    back_standing = pygame.transform.scale(back_standing, (200,200))
    
    left_standing = pygame.image.load("hero1.jpg")
    left_standing = pygame.transform.scale(left_standing, (200,200))
    
    right_standing = pygame.transform.flip(left_standing, True, False) #.flip(image, x, y)
    right_standing = pygame.transform.scale(right_standing, (200,200))

    #get the size of the image for moving purpose
    playerWidth, playerHeight = front_standing.get_size()

    # creating the PygAnimation objects for walking/running in all directions
    animTypes = 'back_run back_walk front_run front_walk left_run left_walk'.split()
    animObjs = {}
    for animType in animTypes:
        #find images that has format of : crono."animeTypes".number(000).gif, the rightest "0" would be replace with range of numer from 0 to 5
        imagesAndDurations = [("hero1.jpg", 100)] #[('gameimages/crono_%s.%s.gif' % (animType, str(num).rjust(3, '0')), 100) for num in range(6)] 
        animObjs[animType] = pyganim.PygAnimation(imagesAndDurations)

##        list of axis use get rect
        
        animObjs[animType].scale((200,200))#Bigger size
        
    # create the right-facing sprites by copying and flipping the left-facing sprites
    animObjs['right_walk'] = animObjs['left_walk'].getCopy()
    animObjs['right_walk'].flip(True, False)
    animObjs['right_walk'].makeTransformsPermanent()
    
    animObjs['right_run'] = animObjs['left_run'].getCopy()
    animObjs['right_run'].flip(True, False)
    animObjs['right_run'].makeTransformsPermanent()

    multiAnime = pyganim.PygConductor(animObjs) #conductor allows multiple animations act at the same time

    # define some constants
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'
    x = 300 # x and y are the player's position
    y = 200
    WALKRATE = 4
    RUNRATE = 12

    direction = DOWN # player starts off facing down (front)

    running = moveUp = moveDown = moveLeft = moveRight = False

    
    arial_16font = pygame.font.SysFont('arial', 16)#(font type, size)
    
    instructionSurf = arial_16font.render('Arrow keys to move. Hold shift to run.', True, WHITE)
    instructionRect = instructionSurf.get_rect()
    instructionRect.bottomleft = (10, HEIGHT - 10)

    alAnim = pyganim.PygAnimation([("hero1.jpg", 50),
                               ("hero1.jpg", 50)])
    alAnim.set_alpha(50)
    alAnim.play()

    hi = pygame.image.load("hero3.jpg")
    hi = pygame.transform.scale(hi, (200,200))
    hi_rect = hi.get_rect()
    
    clock = pygame.time.Clock()
    
    while True:
        
        screen.fill(BGCOLOR)
        
        #events occur here 
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                       
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                
                elif event.key == pygame.K_f:
                    WIDTH = 1366
                    HEIGHT = 767
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                    background_image = pygame.transform.scale(background_image,(WIDTH, HEIGHT))
                    
                elif event.key == pygame.K_n:
                    WIDTH = 1100
                    HEIGHT = 680
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))
                    background_image = pygame.transform.scale(background_image,(WIDTH, HEIGHT))
                    
                elif event.key == pygame.K_i: #press i to disappear anime1
                    anime1.visibility = not anime.visibility

                
                elif event.key in (K_LSHIFT, K_RSHIFT):
                    # player has started running
                    running = True

                elif event.key == K_UP:
                    moveUp = True
                    moveDown = False
                    if not moveLeft and not moveRight:
                        # only change the direction to up if the player wasn't moving left/right
                        direction = UP
                elif event.key == K_DOWN:
                    moveDown = True
                    moveUp = False
                    if not moveLeft and not moveRight:
                        direction = DOWN
                elif event.key == K_LEFT:
                    moveLeft = True
                    moveRight = False
                    if not moveUp and not moveDown:
                        direction = LEFT
                elif event.key == K_RIGHT:
                    moveRight = True
                    moveLeft = False
                    if not moveUp and not moveDown:
                        direction = RIGHT

            elif event.type == KEYUP:
                if event.key in (K_LSHIFT, K_RSHIFT):
                    # player has stopped running
                    running = False

                if event.key == K_UP:
                    moveUp = False
                    # if the player was moving in a sideways direction before, change the direction the player is facing.
                    if moveLeft:
                        direction = LEFT
                    if moveRight:
                        direction = RIGHT
                elif event.key == K_DOWN:
                    moveDown = False
                    if moveLeft:
                        direction = LEFT
                    if moveRight:
                        direction = RIGHT
                elif event.key == K_LEFT:
                    moveLeft = False
                    if moveUp:
                        direction = UP
                    if moveDown:
                        direction = DOWN
                elif event.key == K_RIGHT:
                    moveRight = False
                    if moveUp:
                        direction = UP
                    if moveDown:
                        direction = DOWN

        if moveUp or moveDown or moveLeft or moveRight:
            # draw the correct walking/running sprite from the animation object
            multiAnime.play() # calling play() while the animation objects are already playing is okay; in that case play() is a no-op
            if running:
                if direction == UP:
                    animObjs['back_run'].blit(screen, (x, y))
                elif direction == DOWN:
                    animObjs['front_run'].blit(screen, (x, y))
                elif direction == LEFT:
                    animObjs['left_run'].blit(screen, (x, y))
                elif direction == RIGHT:
                    animObjs['right_run'].blit(screen, (x, y))
            else:
                # walking
                if direction == UP:
                    animObjs['back_walk'].blit(screen, (x, y))
                elif direction == DOWN:
                    animObjs['front_walk'].blit(screen, (x, y))
                elif direction == LEFT:
                    animObjs['left_walk'].blit(screen, (x, y))
                elif direction == RIGHT:
                    animObjs['right_walk'].blit(screen, (x, y))


            # actually move the position of the player
            if running:
                rate = RUNRATE
            else:
                rate = WALKRATE

            if moveUp:
                y -= rate
            if moveDown:
                y += rate
            if moveLeft:
                x -= rate
            if moveRight:
                x += rate

        else:
            # standing still
            multiAnime.stop() # calling stop() while the animation objects are already stopped is okay; in that case stop() is a no-op
            if direction == UP:
                screen.blit(back_standing, (x, y))
            elif direction == DOWN:
                screen.blit(front_standing, (x, y))
            elif direction == LEFT:
                screen.blit(left_standing, (x, y))
            elif direction == RIGHT:
                screen.blit(right_standing, (x, y))

        # make sure the player does move off the screen
        if x < 0:
            x = 0
        if x > WIDTH - playerWidth:
            x = WIDTH - playerWidth
        if y < 0:
            y = 0
        if y > HEIGHT - playerHeight:
            y = HEIGHT - playerHeight
                    
        #spinging or rotate
        spining += 1 #spinng rate
        anime3.clearTransforms()
        anime3.scale((200,200))
        anime3.set_colorkey((0,0,0))
        anime3.rotate(spining)
        
        
        #the animation was having different width and height in the each frame
        curSpinSurf = anime3.getCurrentFrame() # gets the current frame
        w, h = curSpinSurf.get_size() #frame's width and height
        anime3.blit(screen, (550 - int(w/2), (350 - int(h/2))))

        for each_anime in range(len(animes)):
            if each_anime == 3:
                continue
            animes[each_anime].blit(screen, (100*each_anime*2, 50)) 


        #text and image and mouse cursing
        if instructionRect.collidepoint(pygame.mouse.get_pos()):
            #spinging or rotate
            spining -= 2 #spinng rate
            anime3.clearTransforms()
            anime3.scale((200,200))
            anime3.set_colorkey((0,0,0))
            anime3.rotate(spining)

            
        
        #image mouse cursing
##        print(hi_rect.collidepoint(pygame.mouse.get_pos()))
        
        if hi_rect.collidepoint(pygame.mouse.get_pos()):
            #spinging or rotate
            spining -= 2 #spinng rate
            anime3.clearTransforms()
            anime3.scale((200,200))
            anime3.set_colorkey((0,0,0))
            anime3.rotate(spining)
            
        screen.blit(hi, (hi_rect.x, hi_rect.y))
        
        screen.blit(instructionSurf, instructionRect)
        anime.blit(screen, (500,50))
        pygame.display.update()
        clock.tick(30) 

    
if __name__ == "__main__":
    WIDTH = 1000
    HEIGHT = 600
    main(WIDTH, HEIGHT)
    

