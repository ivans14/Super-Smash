import pygame
from scripts.settings import *
from scripts.spriteSheetClass import *

class LifeBar(pygame.sprite.Sprite):
    def __init__(self,game, x, y, width, height, max_health, color = (0,204,0)):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.color = color
        self.width = width
        self.height = height
        self.max_health = max_health
        self.image = pygame.Surface((self.width,self.height))
        self.image.fill((0,204,0))
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.bottom = y
       
    def update(self,health,life):
        if life == 3:
            self.color = (0,204,0)
        if life == 2:
            self.color = (204, 204, 0)
        if life == 1:
            self.color = (204,0,0)
        self.image = pygame.Surface((health*self.width/self.max_health, self.height))
        self.image.fill(self.color)

class CoolBar(pygame.sprite.Sprite):
    def __init__(self,game,x, y, width, height, max_cooldown, color = (0,0,204)):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.color = color
        self.width = width
        self.height = height
        self.max_cooldown = max_cooldown
        self.image = pygame.Surface((self.width,self.height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.bottom = y
        self.full = False
        
    def update(self,now,last_time,max_col):
        if now - last_time > max_col:
            self.color = (255,255,255)
            self.full = True
        else:
            self.color = (0,0,204)
            self.full = False

        if ((now - last_time)*self.width / self.max_cooldown) < self.width:
            self.image = pygame.Surface(((now - last_time)*self.width/self.max_cooldown, self.height))
        self.image.fill(self.color)

        if self.full:
            self.image = pygame.Surface((self.width,self.height))
            self.image.fill(self.color)
        

class Tag(pygame.sprite.Sprite):
    def __init__(self, color):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        if self.color == 'blue':
             self.image = Spritesheet('img/assets/arena.png').get_image(684,134,705-684,152-134)
        if self.color == 'orange':
             self.image = Spritesheet('img/assets/arena.png').get_image(684,153,705-684,171-153)
             
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()

    def update(self, centerx, top):
        self.rect.centerx = centerx
        self.rect.bottom = top - 10       

class Micro(pygame.sprite.Sprite):
    def __init__(self,x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = Spritesheet('img/assets/micro_sprite.png').get_image(0,10,214-0,182-10)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        
    def update(self, muted):
        if not muted:
            self.image = pygame.transform.smoothscale(Spritesheet('img/assets/micro_sprite.png').get_image(0,10,214-0,182-10),(100,80))
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y
        else:
            self.image = pygame.transform.smoothscale(Spritesheet('img/assets/micro_sprite.png').get_image(0,198,214-0,369-198),(100,80))
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

class Rodona_1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = Spritesheet('img/assets/arena.png').get_image(684,178,736-684,228-178)
        self.rect = self.image.get_rect()
        self.rect.left = -200
        self.rect.top = -200
            
    def update(self, owner):
        if owner == 'Mario':            
            self.rect.left = 68
            self.rect.top = 374
        if owner == 'Sonic':            
            self.rect.left = 272
            self.rect.top = 374
        if owner == 'Goku':            
            self.rect.left = 489
            self.rect.top = 374
        if owner == 'Kirby':            
            self.rect.left = 693
            self.rect.top = 374
        if owner == 'Link':            
            self.rect.left = 272
            self.rect.top = 684
        if owner == 'Random':            
            self.rect.left = 484
            self.rect.top = 684
        
class Rodona_2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = Spritesheet('img/assets/arena.png').get_image(684,234,736-684,283-234)
        self.rect = self.image.get_rect()
        self.rect.left = -200
        self.rect.top = -200
        
    def update(self, owner):
        if owner == 'Mario':            
            self.rect.left = 165
            self.rect.top = 374
        if owner == 'Sonic':            
            self.rect.left = 372
            self.rect.top = 375
        if owner == 'Goku':            
            self.rect.left = 590
            self.rect.top = 375
        if owner == 'Kirby':            
            self.rect.left = 793
            self.rect.top = 375
        if owner == 'Link':            
            self.rect.left = 372
            self.rect.top = 684
        if owner == 'Random':            
            self.rect.left = 590
            self.rect.top = 684
        
        
    

    
        
        

        
       
        


