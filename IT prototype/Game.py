import pygame
from pygame.locals import *
import sys
import time
import pyganim
import random

class Player ():
    """implement the character"""
    
    def __init__(self, stance = "Player"):

        self.default_scale = (100,100) #character's size
        
        if stance == "enemy":
            #status for different characters
            self.health = 20
            self.attack = 2
            self.level = 0
            
            self.x = 300 # x and y are the player's position
            self.y = 200

            self.WALKRATE = 4
            self.RUNRATE = 12
            
        else:
            self.health = 5
            self.attack = 1
            self.level = 0
            self.required_experience = self.level*10
            self.experience = 0
            
            self.x = 300 # x and y are the player's position
            self.y = 200

            self.WALKRATE = 4
            self.RUNRATE = 12

        # load the "standing" sprites (these are single images, not animations)
        self.front_standing = pygame.image.load("hero1.png").convert()
        self.front_standing.set_colorkey((0,0,0))
        self.front_standing = pygame.transform.scale(self.front_standing, self.default_scale)
        
        self.back_standing = pygame.image.load("hero1.png").convert()
        self.back_standing.set_colorkey((0,0,0))
        self.back_standing = pygame.transform.scale(self.back_standing, self.default_scale)
        
        self.left_standing = pygame.image.load("hero1.png").convert()
        self.left_standing.set_colorkey((0,0,0))
        self.left_standing = pygame.transform.scale(self.left_standing, self.default_scale)
        
        self.right_standing = pygame.transform.flip(self.left_standing, True, False) #.flip(image, x, y)
        self.right_standing = pygame.transform.scale(self.right_standing, self.default_scale)

        #get the size of the image for moving purpose
        self.playerWidth, self.playerHeight = self.front_standing.get_size()

        # creating the PygAnimation objects for walking/running in all directions
        self.animTypes = 'back_run back_walk front_run front_walk left_run left_walk'.split()
        self.animObjs = {}
        
        rect_axis = []
        for animType in self.animTypes:
            self.imagesAndDurations = [("hero1.png", 100)] 
            self.animObjs[animType] = pyganim.PygAnimation(self.imagesAndDurations)
           
            rect_axis.append(self.animObjs[animType].getRect())
            
            self.animObjs[animType].scale(self.default_scale)
        
        # create the right-facing sprites by copying and flipping the left-facing sprites
        self.animObjs['right_walk'] = self.animObjs['left_walk'].getCopy()
        self.animObjs['right_walk'].flip(True, False)
        self.animObjs['right_walk'].makeTransformsPermanent()
        
        self.animObjs['right_run'] = self.animObjs['left_run'].getCopy()
        self.animObjs['right_run'].flip(True, False)
        self.animObjs['right_run'].makeTransformsPermanent()

        self.running = self.moveUp = self.moveDown = self.moveLeft = self.moveRight = False

    
        # define some constants
        self.UP = 'up'
        self.DOWN = 'down'
        self.LEFT = 'left'
        self.RIGHT = 'right'
    
        self.facing = self.DOWN # player starts off facing down (front)
        
        self.multiAnime = pyganim.PygConductor(self.animObjs) #conductor allows multiple animations act at the same time
        
    def direction (self, event):
        """get the direction of character depend on the arrow keys"""
        if event.type == pygame.KEYDOWN:
            
            if event.key in (K_LSHIFT, K_RSHIFT):
                # player has started running
                self.running = True

            elif event.key == K_UP:
                self.moveUp = True
                self.moveDown = False
                if not self.moveLeft and not self.moveRight:
                    # only change the facing to up if the player wasn't moving left/right
                    self.facing = self.UP
            elif event.key == K_DOWN:
                self.moveDown = True
                self.moveUp = False
                if not self.moveLeft and not self.moveRight:
                    self.facing = self.DOWN
            elif event.key == K_LEFT:
                self.moveLeft = True
                self.moveRight = False
                if not self.moveUp and not self.moveDown:
                    self.facing = self.LEFT
            elif event.key == K_RIGHT:
                self.moveRight = True
                self.moveLeft = False
                if not self.moveUp and not self.moveDown:
                    self.facing = self.RIGHT

        elif event.type == KEYUP:
            if event.key in (K_LSHIFT, K_RSHIFT):
                # player has stopped running
                self.running = False

            if event.key == K_UP:
                self.moveUp = False
                # if the player was moving in a sideways facing before, change the direction the player is facing.
                if self.moveLeft:
                    self.facing = self.LEFT
                if self.moveRight:
                    self.facing = self.RIGHT
            elif event.key == K_DOWN:
                self.moveDown = False
                if self.moveLeft:
                    self.facing = self.LEFT
                if self.moveRight:
                    self.facing = self.RIGHT
            elif event.key == K_LEFT:
                self.moveLeft = False
                if self.moveUp:
                    self.facing = self.UP
                if self.moveDown:
                    self.facing = self.DOWN
            elif event.key == K_RIGHT:
                self.moveRight = False
                if self.moveUp:
                    self.facing = self.UP
                if self.moveDown:
                    self.facing = self.DOWN
       
    
    def movement (self, WIDTH = 1000, HEIGHT = 600, screen = pygame.display.set_mode((1000, 600))):
        """bliting image on the screen as character make a move"""
        
        if self.moveUp or self.moveDown or self.moveLeft or self.moveRight:
            # draw the correct walking/running sprite from the animation object
            self.multiAnime.play() # calling play() when buttons are pressing
            if self.running:
                if self.facing == self.UP:
                    self.animObjs['back_run'].blit(screen, (self.x, self.y))
                elif self.facing == self.DOWN:
                    self.animObjs['front_run'].blit(screen, (self.x, self.y))
                elif self.facing == self.LEFT:
                    self.animObjs['left_run'].blit(screen, (self.x, self.y))
                elif self.facing == self.RIGHT:
                    self.animObjs['right_run'].blit(screen, (self.x, self.y))
            else:
                # walking
                if self.facing == self.UP:
                    self.animObjs['back_walk'].blit(screen, (self.x, self.y))
                elif self.facing == self.DOWN:
                    self.animObjs['front_walk'].blit(screen, (self.x, self.y))
                elif self.facing == self.LEFT:
                    self.animObjs['left_walk'].blit(screen, (self.x, self.y))
                elif self.facing == self.RIGHT:
                    self.animObjs['right_walk'].blit(screen, (self.x, self.y))


            # actually move the position of the player
            if self.running:
                rate = self.RUNRATE
            else:
                rate = self.WALKRATE

            if self.moveUp:
                self.y -= rate
            if self.moveDown:
                self.y += rate
            if self.moveLeft:
                self.x -= rate
            if self.moveRight:
                self.x += rate

        else:
            # standing still
            self.multiAnime.stop() # calling stop() while the animation objects are already stopped is okay; in that case stop() is a no-op
            
            if self.facing == self.UP:
                screen.blit(self.back_standing, (self.x, self.y))
            elif self.facing == self.DOWN:
                screen.blit(self.front_standing, (self.x, self.y))
            elif self.facing == self.LEFT:
                screen.blit(self.left_standing, (self.x, self.y))
            elif self.facing == self.RIGHT:
                screen.blit(self.right_standing, (self.x, self.y))

        # make sure the player does move off the screen
        if self.x < 0:
            self.x = 0
        if self.x > WIDTH - self.playerWidth:
            self.x = WIDTH - self.playerWidth
        if self.y < 0:
            self.y = 0
        if self.y > HEIGHT - self.playerHeight:
            self.y = HEIGHT - self.playerHeight
    
def text (string, x, y, size = 16, font='Arial', color=(255, 255, 255)):
    """blit text on the screen"""
    arial_16font = pygame.font.SysFont(font, size)#(font type, size)
    
    instructionSurf = arial_16font.render(string, True, color)
    instructionRect = instructionSurf.get_rect()
    instructionRect.bottomleft = (x, y)
    
def angle(anime, angle):
    """set the angle of the character"""

    anime.rotate(angle)

def spining(anime, angle, screen, x, y, size_x = None, size_y = None):
    """make character spin"""
    
    anime.clearTransforms()
    
    if size_x != None or size_y != None:
        anime.scale((size_x, size_y))
        
    anime.rotate(angle)
    curSpinSurf = anime.getCurrentFrame() # gets the current frame
    w, h = curSpinSurf.get_size() #frame's width and height
    anime.set_colorkey((0,0,0))
    anime.blit(screen, (x - int(w/2), (y - int(h/2))))
        
def transparency (anime, value):
    """make charcter image color more fading"""
    
    anime.set_alpha(value) #range value is 0 to 255

def scale (anime, x, y):
    """change the size"""
    anime.scale((x, y))

def disappear (anime):
    
    anime.visibility = not anime.visibility

        
def main():

    finish = False
    
    BGCOLOR = (100, 50, 50)
    
    Width = 1000
    Height = 600
    pygame.init()
    screen = pygame.display.set_mode((Width, Height))
    pygame.display.set_caption("Unimaginable Powers!!!")
    player = Player()

    while not finish:
        
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

            player.direction(event)
        
        player.movement(Width, Height)


        pygame.display.update()
        pygame.time.Clock().tick(80)

        
if __name__ == "__main__":
    
    main()
        
