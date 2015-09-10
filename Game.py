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
            self.original_health = 20
            self.current_health = 20
            self.damage = 2
            self.level = 0
            
            self.x = 300 # x and y are the player's position
            self.y = 200

            self.WALKRATE = 4
            self.RUNRATE = 12
            
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

            """____"""
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
        self.front_standing = pygame.transform.scale(self.front_standing, self.default_scale)
        
        self.back_standing = pygame.image.load("Pictures/hero1.png").convert()
        self.back_standing.set_colorkey((0,0,0))
        self.back_standing = pygame.transform.scale(self.back_standing, self.default_scale)
        
        self.left_standing = pygame.image.load("Pictures/hero1.png").convert()
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
            self.imagesAndDurations = [("Pictures/hero1.png", 100)] 
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

class Map():

    def __init__(self,x,y):

##        self.obstaticle_pos = []
##
##        # Check and see if we hit anything
##        block_hit_list = pygame.sprite.spritecollide(self, Ocean_obstacles, False)
##        
##        for block in block_hit_list:
## 
##            # Reset our position based on the top/bottom of the object.
##            if self.change_y > 0:
##                self.rect.bottom = block.rect.top
##            else:
##                self.rect.top = block.rect.bottom
                

        """plot obstacles, save the posotion, collide, find the hero's"""
        """facing direction and go back one step or the old position if possible"""


        
        self.x = x
        self.y = y
        self.sprite =  pygame.sprite.Sprite()
        self.sprite.image =  pygame.image.load('hero.gif')
        self.sprite.rect =  self.sprite.image.get_rect()
        self.sprite.rect.left = x
        self.sprite.rect.top = y
        self.group = pygame.sprite.GroupSingle(self.sprite)

    # Finds distance between player and obstacle
    def dist_player(self, me):
        disty = math.sqrt( (float(self.x)-float(me.x))**2 + (float(self.y)-float(me.y))**2)  
        return disty
    
    # checks if the player has hit a object
    def hit(self, me):
        dst = self.dist_player(me)
        if dst < 26:
            enmy.health = enmy.health-10
        print(enmy.health)
        
    # creates a copy of origional x and y   
    def cpy(self,me):
        me.current_x = copy.deepcopy(me.x)  
        me.current_y = copy.deepcopy(me.y) 

    # if player collides go back a step 
    def too_far(self,me):
        dst = self.dist_player(me) 

        if dst < 26:
            me.x = me.current_x
            me.y = me.current_y


# pet class
class Pet():
 
    def __init__(self,x,y):
        self.x = x
        self.y = y 
        self.health = 10
        self.alive = 1   
        #self.battle_x = 1
        self.sprite =  pygame.sprite.Sprite()
        self.sprite.image =  pygame.image.load('Pictures/tank1 new.png')
        self.sprite.image = pygame.transform.scale(self.sprite.image, (20,20))
        self.sprite.rect =  self.sprite.image.get_rect()
        self.sprite.rect.left = 4
        self.sprite.rect.top = 4
        self.group = pygame.sprite.GroupSingle(self.sprite)
 #finds the distance to player   
    def dist_to_player(self, me):
        disty = math.sqrt( (float(self.x)-float(me.x))**2 + (float(self.y)-float(me.y))**2)
        return disty
 #makes a copy of origional x and y    
    def cpy(self):
        self.current_x = copy.deepcopy(self.x)  
        self.current_y = copy.deepcopy(self.y) 
# works out the position of pet before move
    def old_move(self):
        x = copy.deepcopy(self.x)
        y = copy.deepcopy(self.y)
        x = self.current_x
        y = self.current_y
#set origional x
    def orig_positx(self):
        orig_x = self.current_x
        return orig_x
#set origional y
    def orig_posity(self):
        orig_y = self.current_y
        return orig_y
 # checks if the pet has gone too far from the player and if so sets position to players        
  
    
    def too_far(self,me):
        dst =  self.dist_to_player(me) 

        if dst > 200:
            self.x = me.x
            self.y = me.y    
  
# does a random move 
  
    def random_move(self):
         r = random.randint(0,4)
         if r == 0:
             if self.sprite.rect.top > 0:
                self.x = self.x + 10
                self.x,self.y=self.sprite.rect.center
         elif r == 1:
             if self.sprite.rect.top < HEIGHT:
                self.sprite.rect.top += TILE_SIZE/20
                self.x,self.y=self.sprite.rect.center
         elif r == 2:
             if self.sprite.rect.right < WIDTH:
                self.sprite.rect.right += TILE_SIZE/20
                self.x,self.y=self.sprite.rect.center
               
         elif r == 3:
             if self.sprite.rect.right >0:
                self.sprite.rect.right -= TILE_SIZE/20
                self.x,self.y=self.sprite.rect.center
                  

    def random_move(self):
         r = random.randint(0,4)
         if r == 0:
             if self.sprite.rect.top > 0:
                self.sprite.rect.top -= TILE_SIZE/20
                self.x,self.y=self.sprite.rect.center
         elif r == 1:
             if self.sprite.rect.top < HEIGHT:
                self.sprite.rect.top += TILE_SIZE/20
                self.x,self.y=self.sprite.rect.center
         elif r == 2:
             if self.sprite.rect.right < WIDTH:
                self.sprite.rect.right += TILE_SIZE/20
                self.x,self.y=self.sprite.rect.center
               
         elif r == 3:
             if self.sprite.rect.right >0:
                self.sprite.rect.right -= TILE_SIZE/20
                self.x,self.y=self.sprite.rect.center

# enemy tank class


class Enemy():
 
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.health = z
        self.orig = z
        self.alive = 1
        self.battle_x=1
        self.mode = NORMAL
        self.sprite =  pygame.sprite.Sprite()
        self.sprite.image =  pygame.image.load('Pictures/tank2 new.png')
        self.sprite.rect =  self.sprite.image.get_rect()
        self.sprite.rect.left = x
        self.sprite.rect.top = y
        self.group = pygame.sprite.GroupSingle(self.sprite)
# does a rnadom move
    def random_move(self):
        r = random.randint(0,4)
      
        if r == 0:
            if self.sprite.rect.top > 0:
                self.sprite.rect.top -= TILE_SIZE/10
                self.x,self.y=self.sprite.rect.center
        elif r == 1:
            if self.sprite.rect.top < HEIGHT:
                self.sprite.rect.top += TILE_SIZE/10
                self.x,self.y=self.sprite.rect.center
        elif r == 2:
            if self.sprite.rect.right < WIDTH:
                self.sprite.rect.right += TILE_SIZE/10
                self.x,self.y=self.sprite.rect.center
               
                 
        elif r == 3:
            if self.sprite.rect.right >0:
                self.sprite.rect.right -= TILE_SIZE/10
                self.x,self.y=self.sprite.rect.center
              
 
 
# if health reaches helth percentage change image    

    def shrink(self):
        if self.health == self.orig/2:
            self.sprite.image =  pygame.image.load('Pictures/tank1 new.png')        

 
# the projectile class
 
class Shot():

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.speed = 60
        self.mse = pygame.mouse.get_pos()
        self.Vx = self.getVx()
        self.Vy = self.getVy()
        self.sprite =  pygame.sprite.Sprite()
        self.sprite.image =  pygame.image.load('Pictures/Ball_sprite.png')
        self.sprite.image = pygame.transform.scale(self.sprite.image, (20,20))
        self.sprite.rect =  self.sprite.image.get_rect()
        self.sprite.rect =  self.sprite.image.get_rect()
        self.sprite.rect.left = x
        self.sprite.rect.top = y
        self.group = pygame.sprite.GroupSingle(self.sprite)
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
    def hit(self, enmy):
        dst = self.dist_enmy(enmy)
        if dst < 26:
            enmy.health = enmy.health-10
        print(enmy.health)
 
#moves projectile
    def move(self):
        if self.sprite.rect.right < WIDTH:
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
        if disty > 1000:
            return True
        else:
            return False


#######################################################################################
###########  FUNCTIONS 
#######################################################################################
# updates position of enemies and projectiles
              
def UpdatePosition(Shots):
      enemy.random_move()
      enemy.shrink() 
      enemy2.random_move()
      enemy2.shrink() 
      enemy3.random_move()
      enemy3.shrink() 
      N = len(Shots)
      for i in range(N):
         Shots[i].move()
# finds distance to mouse
def disty():
     p = pygame.mouse.get_pos()
     print(p)
     time.sleep(0.1)
#general find distance function         
def Distance(ObjOne,ObjTwo):
    disty = math.sqrt( (float(ObjOne.x)-float(ObjTwo.x))**2 + (float(ObjOne.y)-float(ObjTwo.y))**2)  
    return disty

# checks if player has collided with the obstacle
def check_collision_obj(me,obj):
    print("collision routine")
    for i in obj:
        print("Distance = ",Distance(me,i))
        if Distance(me,i) < 15:
           print("collision") 
           return True
       
    return False




#--------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------
#------------------------ MAINLINE ----------------------------------------------------------
#--------------------------------------------------------------------------------------------
#creates all the objects
#object loop
obj = []
me  = Hero()
#creates obstacles
for i in range (15):
    x = random.randint(0,800)
    print(x)
    y = random.randint(0,800)
    print(y)
    obj.append(Map(x,y))

pet     = Pet(500,500)
enemy   = Enemy(6,6,20)
enemy2  = Enemy(7,7,20)
enemy3  = Enemy(15,15,20)

#sets tile size, the height, and width of screen

TILE_SIZE = me.sprite.rect.width
NUM_TILES_WIDTH = WIDTH / TILE_SIZE
NUM_TILES_HEIGHT = HEIGHT / TILE_SIZE


# variable to check if player has won

win = False



#---------------------------------------------------------------------------------------- MENU 
#Starts up the difficulty screen and asks if you want to play hard or easy

strn = "Difficulty Easy!!"
difficulty = 1
print_screen(strn) 
menu_flag = True

me.set_health()
while menu_flag : 
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                screen.fill((134, 145, 21))
                strn = "Difficulty Easy"
                difficulty = 1
                print_screen(strn)
                pygame.display.update()
            if event.key == pygame.K_DOWN:
                screen.fill((134, 145, 21))
                strn = "Difficulty Hard"
                difficulty = 2
                print_screen(strn)       
                pygame.display.update()  
            if event.key == pygame.K_SPACE:
                print( "You have hit the space bar")                 
                menu_flag=False
             


#--------------------------------------------------------MAIN MAP LOOP ----------------------------------------
#checks if either you have won the game or lost the game 
finish = False
now = False
Shots = []

winner = 0
while finish != True:
    disty()


     # STEP 1 - Check on Health
    if me.health <= 0:
        screen.fill((34, 145, 21))
        print_screen("Youre Lose!")
        time.sleep(1.0)
        pygame.quit()    
     

    
     # STEP 2 - Update all the positions and look for collisions 
    UpdatePosition(Shots)

    for i in Shots:
        i.dist_enmy(enemy)
        i.hit(enemy)
        i.dist_enmy(enemy2)
        i.hit(enemy2)
        i.dist_enmy(enemy3)
        i.hit(enemy3)
    if me.dist_to_enemy(enemy) < 50.0 and enemy.alive: 
        me.damage()
                   


     # Random move the pet
    fail = True
    while fail == True:
        pet.cpy()     
        pet.random_move()
        pet.dist_to_player(me)
        if pet.dist_to_player(me) > 26:
             pet.old_move()
        else:
            fail = False	 
    time.sleep(0.2)	




     # HANDLE EVENTS
     	  
#checks is game is finished or not		 	
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            finish = True
        if event.type == pygame.KEYDOWN:

         # Move the player around the screen

            time.sleep(0.1)
            if event.key == pygame.K_UP:
                if me.sprite.rect.top > 0:
                   me.sprite.image =  pygame.image.load('Actor5back.png')                
                   me.sprite.rect.top -= TILE_SIZE/10
                   me.x,me.y=me.sprite.rect.center 
                if check_collision_obj(me,obj) == True:
                   me.sprite.rect.top += TILE_SIZE/10
                   me.x,me.y=me.sprite.rect.center  

                      
            elif event.key == pygame.K_DOWN:
                if me.sprite.rect.top < HEIGHT:
                   me.sprite.image =  pygame.image.load('Actor5frnt.png') 
                   me.sprite.rect.top += TILE_SIZE/10
                   me.x,me.y=me.sprite.rect.center  
                if check_collision_obj(me,obj) == True:
                   me.sprite.rect.top -= TILE_SIZE/10
                   me.x,me.y=me.sprite.rect.center  

           
            elif event.key == pygame.K_RIGHT:
                if me.sprite.rect.right < WIDTH:
                   me.sprite.image =  pygame.image.load('Actor5right.png')
                   me.sprite.rect.right += TILE_SIZE/10                   
                   me.x,me.y=me.sprite.rect.center  
 
                   if not IsValidPosition(me.x,me.y):
                      print( "Not valid position ")
                      me.sprite.rect.right += TILE_SIZE/10                   
                      me.x,me.y=me.sprite.rect.center 
                if check_collision_obj(me,obj) == True:
                   me.sprite.rect.right -= TILE_SIZE/10           
                   me.x,me.y=me.sprite.rect.center  
            elif event.key == pygame.K_LEFT:
                if me.sprite.rect.right >0:
                    me.sprite.image =  pygame.image.load('Actor5lft.png')
                    me.sprite.rect.right -= TILE_SIZE/10                   
                    me.x,me.y=me.sprite.rect.center       
                    if not IsValidPosition(me.x,me.y):
                       print( "Not valid position ")
                       me.sprite.rect.right += TILE_SIZE     
                       me.x,me.y=me.sprite.rect.center   
                if check_collision_obj(me,obj) == True:
                    me.sprite.rect.right += TILE_SIZE/10           
                    me.x,me.y=me.sprite.rect.center  
            elif event.key == pygame.K_c:      
                Shots.append(Shot(me.x,me.y))
                print("Hello")

       
            time.sleep(0.1)

             #-------------------------------------------------------------B A T T L E  L O O P  H E R E
             #This is the Battle loop
            
                      
#checks whether the enemies are alive or not 
#draws players and enemies
    screen.fill((0, 0, 0))
    if me.health > 0:
         me.group.draw(screen)
         for i in obj:
             i.group.draw(screen)
         #shop.group.draw(screen)
         pet.group.draw(screen)   
         for shts in Shots:
           if shts.too_far(me) == False:
             shts.group.draw(screen)
             shts.dist_player(me)
             shts.too_far(me)
           
    if enemy.health > 0:
        enemy.group.draw(screen)
    else:
        winner = winner + 1
    if enemy2.health > 0:    
        enemy2.group.draw(screen)
    else:
        winner = winner + 1
    if enemy3.health > 0:
        enemy3.group.draw(screen)
    else:
        winner = winner + 1
     
    print(winner)
    if winner == 3:
        screen.fill((34, 145, 21))
        print_screen("Youre Winner!")
        time.sleep(1.0)
        pygame.quit()   

    pygame.draw.line(screen, (0,0,255), (400,0), (400,436), 4) 
    pygame.display.update()













    
            
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
        
