import pygame

class Player(pygame.sprite.Sprite):
    change_x = 0
    change_y = 0
    
    def __init__(self, x, y, name):

        pygame.sprite.Sprite.__init__(self)
       
        
        self.images = ["luffy stand.png","luffy stand.png","luffy stand.png","luffy stand.png"]
        
        
        self.image = pygame.image.load(self.images[0]).convert_alpha()
        
        # Set height, width
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


class Character (Player): 
    
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

class Enemy(pygame.sprite.Sprite):

    change_x = 0
    change_y = 0
    
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        # Set height, width
        
        self.image = pygame.image.load("enemy stand.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(33, 43))
        
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
        
def TypeOfEnemy (Enemy):

    def __init__(self, x, y, name):
        Enemy.__init__(self, x, y, name)
        
        self.max_health = 10
        self.max_mana = 50
        self.attack = 5 
        self.defense = 10 
        self.health = self.max_health
        self.mana = self.max_mana
