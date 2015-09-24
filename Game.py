import pygame
from pygame.locals import *
import sys
import time
import pyganim
import random

import random
import math
import copy
from random import randint
# change
class Player (pygame.sprite.Sprite):
    """implement the character"""

    def __init__(self,stance = "Player", default_scale = (25,25)):

        pygame.sprite.Sprite.__init__(self)



        
##        https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite
##        use the link to use pygame.sprite.Sprite for behaviours and death etc and use on pyganim
        
        default_scale = default_scale #all character's size


        # make children class and redefine all the varibles(it has priority)
        if stance == "enemy":
            #status for different characters
            self.original_health = 20
            self.current_health = 20
            self.damage = 2
            self.level = 0
            
            self.x = random.randint(0, 1000) # x and y are the player's position
            self.y = random.randint(0, 600)

            self.WALKRATE = 4
            self.RUNRATE = 12

            

            #part of making sprite get kill
            self.image =  pygame.image.load('Pictures/hero.gif')
            self.image = pygame.transform.scale(self.image, (20,20))
            self.rect =  self.image.get_rect()
            
            self.rect.left = self.x
            self.rect.top = self.y
           
            self.group = pygame.sprite.GroupSingle(self)
            #part of making sprite get kill

            

            
            
        else:
            self.original_health = 5
            self.current_health = 5
            
            self.damage = 1
            self.level = 0
            self.required_experience = self.level*10
            self.experience = 0
            
            self.x = 300 # x and y are the player's position
            self.y = 200

            self.WALKRATE = 4
            self.RUNRATE = 12

            
            """___look at below to check if required_"""
##            self.battle.x = 1
##            self.alive = 1
##            self.sprite.rect.left = 4
##            self.sprite.rect.top = 4
##            self.group = pygame.sprite.GroupSingle(self.sprite)
##            # finds distance between enemy and the character
##            def dist_to_enemy(self, enmy):
##                disty = math.sqrt( (float(self.x)-float(enmy.x))**2 + (float(self.y)-float(enmy.y))**2)
##                 return disty


            # load the "standing" sprites (these are single images, not animations)
            self.front_standing = pygame.image.load("Pictures/hero1.png").convert()
            self.front_standing.set_colorkey((0,0,0))
            self.front_standing = pygame.transform.scale(self.front_standing, default_scale)
            
            self.back_standing = pygame.image.load("Pictures/hero1.png").convert()
            self.back_standing.set_colorkey((0,0,0))
            self.back_standing = pygame.transform.scale(self.back_standing, default_scale)
            
            self.left_standing = pygame.image.load("Pictures/hero1.png").convert()
            self.left_standing.set_colorkey((0,0,0))
            self.left_standing = pygame.transform.scale(self.left_standing, default_scale)
            
            self.right_standing = pygame.transform.flip(self.left_standing, True, False) #.flip(image, x, y)
            self.right_standing = pygame.transform.scale(self.right_standing, default_scale)

            #get the size of the image for moving purpose
            self.playerWidth, self.playerHeight = self.front_standing.get_size()

            # creating the PygAnimation objects for walking/running in all directions
            self.animTypes = 'back_run back_walk front_run front_walk left_run left_walk'.split()
            self.animObjs = {}
            
            rect_axis = []
            for animType in self.animTypes:
                self.imagesAndDurations = [("Pictures/hero1.png", 100)] 
                self.animObjs[animType] = pyganim.PygAnimation(self.imagesAndDurations)
               
                rect_axis.append(self.animObjs[animType].getRect())
                
                self.animObjs[animType].scale(default_scale)
            

        
        
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

            elif event.key == K_w:
                self.moveUp = True
                self.moveDown = False
                if not self.moveLeft and not self.moveRight:
                    # only change the facing to up if the player wasn't moving left/right
                    self.facing = self.UP
            elif event.key == K_s:
                self.moveDown = True
                self.moveUp = False
                if not self.moveLeft and not self.moveRight:
                    self.facing = self.DOWN
            elif event.key == K_a:
                self.moveLeft = True
                self.moveRight = False
                if not self.moveUp and not self.moveDown:
                    self.facing = self.LEFT
            elif event.key == K_d:
                self.moveRight = True
                self.moveLeft = False
                if not self.moveUp and not self.moveDown:
                    self.facing = self.RIGHT

        elif event.type == KEYUP:
            if event.key in (K_LSHIFT, K_RSHIFT):
                # player has stopped running
                self.running = False

            if event.key == K_w:
                self.moveUp = False
                # if the player was moving in a sideways facing before, change the direction the player is facing.
                if self.moveLeft:
                    self.facing = self.LEFT
                if self.moveRight:
                    self.facing = self.RIGHT
            elif event.key == K_s:
                self.moveDown = False
                if self.moveLeft:
                    self.facing = self.LEFT
                if self.moveRight:
                    self.facing = self.RIGHT
            elif event.key == K_a:
                self.moveLeft = False
                if self.moveUp:
                    self.facing = self.UP
                if self.moveDown:
                    self.facing = self.DOWN
            elif event.key == K_d:
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


    def collision (self, list_of_objects):

        collisions = pygame.sprite.spritecollide(self, list_of_objects, False)
        
        for coliision in collisions:

            if self.facing == "down":
                self.y -= 1
            else:
                self.y += 1

            if self.facing == "left":
                self.x -= 1
            else:
                self.y += 1
                
##    def random_move(self, screen = pygame.display.set_mode((1000, 600)) ):
##        rand_x = random.randint(-20,20)
##        rand_y = random.randint(-20,20)
##        
##        self.rect.top += rand_y
##        self.rect.left += rand_x
##        
##        screen.blit(self.image, (self.rect.left, self.rect.top))
        

        







class Obstacle(pygame.sprite.Sprite):

    def __init__(self, default_scale = (25,25)):

        pygame.sprite.Sprite.__init__(self)
        
        self.obstaticle_pos = []
        
        self.obstacle = pygame.image.load('Pictures/crab.png').convert_alpha()
        self.obstacle = pygame.transform.scale(self.obstacle, default_scale)
        
    def obstacles_placing (self, nums = random.randint(3, 10), WIDTH = 1000, HEIGHT = 600):

        for num in range(nums):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            
            while (x, y) in self.obstaticle_pos:
                x = random.randint(0, WIDTH)
                y = random.randint(0, HEIGHT)
                
            self.obstaticle_pos.append((x, y))
            pygame.display.set_mode((WIDTH, HEIGHT)).blit(self.obstacle, (x, y))


class Pet(pygame.sprite.Sprite):
 
    def __init__(self, player):

        pygame.sprite.Sprite.__init__(self)
        
        self.level = 0
        self.expereience = 0
        self.full_experience = 0
        player.health += self.level*10
        
        #place the pet behind the player 
        self.x = player.x
        self.y = player.y + 2
    
        self.image =  pygame.image.load('Pictures/tank1 new.png')
        self.image = pygame.transform.scale(self.image, (5,5))

        #have facing later!!!
                     
##        self.group = pygame.sprite.GroupSingle(self.sprite)  #group single replace the sprite when new one add
  
# does a random move arond the player
  
    def follow(self, screen = pygame.display.set_mode((1000, 600))):
        
        big_follow = random.randint(-5,5)
        small_follow = random.randint(-2,2)

        self.x = (player.x + big_follow)
        self.y = (player.y + small_follow)
        
        while self.x >= (player.x + 10) or self.y >= (player.y + 5):
            self.x = (player.x + big_follow)
            self.y = (player.y + small_follow)
            
        if player.facing == "down":
            screen.blit(self.image, (player.x + big_follow, player.y + abs(small_follow)))
        else:
            screen.blit(self.image, (player.x + big_follow, player.y + abs(small_follow)))

        if player.facing == "left":
            screen.blit(self.image, (player.x + abs(small_follow), player.y + big_follow))
        else:
            screen.blit(self.image, (player.x + abs(small_follow), player.y + big_follow))
                  

class Shot(pygame.sprite.Sprite):

    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        
        self.x = player.x
        self.y = player.y
        self.mse = pygame.mouse.get_pos()
        self.sprite =  pygame.sprite.Sprite()
        self.sprite.image =  pygame.image.load('Pictures/Ball_sprite.png')
        self.sprite.image = pygame.transform.scale(self.sprite.image, (20,20))
        self.sprite.rect =  self.sprite.image.get_rect()
        self.sprite.rect =  self.sprite.image.get_rect()
        self.sprite.rect.left = player.x
        self.sprite.rect.top = player.y
        self.group = pygame.sprite.GroupSingle(self.sprite)

        self.Vx = self.getVx()
        self.Vy = self.getVy()
        self.speed = 10

        self.delta_x = 0
        self.delat_y = 0
        #need to find the change of distance from inital !!
        
# works out velocity in x direction
    def getVx(self):
        L = ( (self.mse[0] - self.x)*(self.mse[0] - self.x) + (self.mse[1] - self.y)*(self.mse[1] - self.y))**(0.5) 
        return (self.mse[0] - self.x)/L
# works out velocity in y direction
    def getVy(self):
        L = ( (self.mse[0] - self.x)*(self.mse[0] - self.x) + (self.mse[1] - self.y)*(self.mse[1] - self.y))**(0.5) 
        return (self.mse[1] - self.y)/L
# works out distance to enemy from the projectile

    def dist_enmy(self, enmy):
        disty = math.sqrt( (float(self.x)-float(enmy.x))**2 + (float(self.y)-float(enmy.y))**2)
  
        return disty
#checks if the projectile has hit the enemy    
    def hit(self, player):
        dst = self.dist_enmy(enmy)
        if dst < 26:
            enmy.health = enmy.health-10
        print(enmy.health)

        
##        collisions = pygame.sprite.spritecollide(self.sprite.image, player, True)
##        
##        for coliision in collisions:
##            player.kill()
##            Shot().kill()
 
#moves projectile
    def move(self):
        if self.sprite.rect.right < 1000:
            self.sprite.rect.right  += self.Vx*self.speed
            self.sprite.rect.top    += self.Vy*self.speed
            self.x,self.y=self.sprite.rect.center
# finds distance between projectile and player
    def dist_player(self,Hero):
        disty = math.sqrt( (float(self.x)-float(Hero.x))**2 + (float(self.y)-float(Hero.y))**2)      
        return disty

# checks if distance is too far from the player so that if this is true the object will be removed
    def too_far(self, Hero):
        disty = self.dist_player(Hero)
        if self.x > 990 or self.y > 590:#disty > 1000:
            return True
        else:
            return False


def UpdatePosition(shots, enemies):
    N = len(shots)
    
    for i in range(len(enemies)):
        
        
        for e in range(N):


            if enemies[i].image.get_rect().collidepoint((shots[e].x, shots[e].y)):
                shots[e].kill()
                enemies[i].kill()

                screen.blit(enemies[i].image, (enemies[i].x, enemies[i].y))
            
            shots[e].move()
        
            if shots[e].x > 980 or shots[e].y > 580:
                shots[e].kill()
        

    
    

            
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
    enemy = Player("enemy")
    enemy1 = Player("enemy")
    shots = []

    num = 6

    list_of_enemies = {}
    for enemy in range(num):
        list_of_enemies[enemy] = Player("enemy")
    
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
                elif event.key == pygame.K_c:
                    shots.append(Shot(player))
                    
                #part of making sprite get kill
                if event.key == pygame.K_g:
                    enemy1.kill()
                #get the sprite appear 
                if event.key == pygame.K_k:
                    enemy1.add(enemy1.group)
                    
            player.direction(event)
        
        player.movement(Width, Height)


##        #care about the small range of player and look at the answer to the test code of the ball physics 
##        for i in range(num):
##            
##            if list_of_enemies[i].x > player.x:
##                list_of_enemies[i].x -= 2
##                list_of_enemies[i].image = pygame.image.load('Pictures/hero.gif').convert_alpha()
##                list_of_enemies[i].image = pygame.transform.scale(list_of_enemies[i].image,(25,25))
##                
##            elif list_of_enemies[i].x > player.x:
##                list_of_enemies[i].x += random.choice([2, -2, 3, -3])
##                list_of_enemies[i].image = pygame.image.load('Pictures/hero.gif').convert_alpha()
##                list_of_enemies[i].image = pygame.transform.scale(list_of_enemies[i].image,(25,25))
##                
##            if list_of_enemies[i].x < player.x:
##                list_of_enemies[i].x += 2
##                list_of_enemies[i].image = pygame.image.load('Pictures/hero.gif').convert_alpha()
##                list_of_enemies[i].image = pygame.transform.scale(list_of_enemies[i].image,(25,25))
##                
##            elif list_of_enemies[i].x < player.x:
##                list_of_enemies[i].x -= random.choice([2, -2, 3, -3])
##                list_of_enemies[i].image = pygame.image.load('Pictures/hero.gif').convert_alpha()
##                list_of_enemies[i].image = pygame.transform.scale(list_of_enemies[i].image,(25,25))
##                
##            if list_of_enemies[i].y > player.y:
##                list_of_enemies[i].y -= 2
##                list_of_enemies[i].image = pygame.image.load('Pictures/hero.gif').convert_alpha()
##                list_of_enemies[i].image = pygame.transform.scale(list_of_enemies[i].image,(25,25))
##                
##            elif list_of_enemies[i].y > player.y:
##                list_of_enemies[i].y += random.choice([2, -2, 3, -3])
##                list_of_enemies[i].image = pygame.image.load(list_of_enemies[i].image).convert_alpha()
##                list_of_enemies[i].image = pygame.transform.scale(list_of_enemies[i].image,(25,25))
##                
##            if list_of_enemies[i].y < player.y:
##                list_of_enemies[i].y += 2
##                list_of_enemies[i].image = pygame.image.load('Pictures/hero.gif').convert_alpha()
##                list_of_enemies[i].image = pygame.transform.scale(list_of_enemies[i].image,(25,25))
##            elif list_of_enemies[i].y < player.y:
##                list_of_enemies[i].y -= random.choice([2, -2, 3, -3])
##                list_of_enemies[i].image = pygame.image.load('Pictures/hero.gif').convert_alpha()
##                list_of_enemies[i].image = pygame.transform.scale(list_of_enemies[i].image,(25,25))
##                  
##
##            screen.blit(list_of_enemies[i].image, (list_of_enemies[i].x, list_of_enemies[i].y))
        
        pygame.time.delay(50)



        
        
        for sht in shots:
            if sht.too_far(player) == False:
                sht.group.draw(screen)
                sht.dist_player(player)
                sht.too_far(player)
                
        for enemy in range(num):
            list_of_enemies[enemy].group.draw(screen)
            
        #improve this
        
        UpdatePosition(shots, list_of_enemies)
                
        #part of making sprite get kill
        enemy1.group.draw(screen)

        

            
        pygame.display.update()
        pygame.time.Clock().tick(80)

        
if __name__ == "__main__":
    
    main()
        
