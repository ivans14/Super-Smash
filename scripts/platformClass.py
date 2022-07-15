import pygame
from scripts.settings import *
from random import *
from scripts.spriteSheetClass import *   

class Stadium(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = Spritesheet('img/assets/arena.png').get_image(23,198,556,201)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rellotge = pygame.time.get_ticks()
        
        self.puja = True
        self.baixa = False
        self.dead = False
        
    def update(self):
        self.actua()
        if pygame.time.get_ticks() - self.rellotge > 20000:
            self.baixa = True
            self.clock = pygame.time.get_ticks()
        if self.puja:
            if self.rect.top != HEIGHT -201:
                self.rect.y -= 1
        if self.rect.top == HEIGHT -201:
            self.puja = False
            
            
    def actua(self):
        if self.baixa:            
            self.rect.y += 1
        if self.rect.top > HEIGHT + 450:
            self.kill()

class Pipe(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = Spritesheet('img/assets/pipe.png').get_image(0,0,96,148)
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
    def update(self):
        pass

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.arena_spritesheet = Spritesheet('img/assets/arena.png')
        images = [self.arena_spritesheet.get_image(97,16,596,23),
                  self.arena_spritesheet.get_image(97,16,596,23),
                  self.arena_spritesheet.get_image(97,55,263,23),
                  self.arena_spritesheet.get_image(97,91,459,23),
                  self.arena_spritesheet.get_image(97,143,373,23),
                  self.arena_spritesheet.get_image(538,154,115,23)]
        self.image = choice(images)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel = 1
        
    def update(self):
        #moviment plataformes
        #plat.rect.y += randrange(1,3) <-- dona efecte curios
        self.rect.y += 1
        if self.rect.top >= HEIGHT:
            self.kill()
          
class Sequenciador(pygame.sprite.OrderedUpdates):
    def __init__(self):
        super().__init__()
        self.t_ultima_plat = pygame.time.get_ticks()
        
    def update(self):
        super().update()
        #generacio de noves plataformes
        if pygame.time.get_ticks() - self.t_ultima_plat > 3000:
            width = randrange(WIDTH*(0.15), WIDTH*(0.45))
            p = Platform(randrange(0,WIDTH-width),randrange(-75,-35))
            if p.rect.right > WIDTH:
                p.rect.right = WIDTH
            self.add(p)
            n = randint(0,10)
            if n == 1:
                l = PowerUp(p.rect.centerx, p.rect.top, p.rect.left, p.rect.right)
                self.life_gr.add(l)
            if n == 2 or n == 3:
                c = Coin(p.rect.centerx, p.rect.top)
                self.coins.add(c)
            self.t_ultima_plat = pygame.time.get_ticks()
            
    def kill(self):
        for plat in self.group:
            plat.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, max_left, max_right):
        pygame.sprite.Sprite.__init__(self)
        self.image = Spritesheet('img/assets/power_up_sprite.png').get_image(178,97,209-178,130-97)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y
        self.vel = 1
        self.max_left = max_left
        self.max_right = max_right
        
    def update(self):
        self.rect.y += 1
        if self.vel > 0:
            if self.rect.right == self.max_right:
                self.vel = -1
            else:
                self.rect.x += 1
        else:
            if self.rect.x == self.max_left:
                self.vel = 1
            else:
                self.rect.x -= 1
        
        if self.rect.top >= HEIGHT:
            self.kill()
            
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.spritesheet = Spritesheet('img/assets/power_up_sprite.png')
        self.load_images()
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y
        self.last_update = pygame.time.get_ticks()
        self.current_frame = 0
              
    def update(self):
        self.select_image()
        self.rect.y += 1        
        if self.rect.top >= HEIGHT:
            self.kill()

    def select_image(self):
        if pygame.time.get_ticks() - self.last_update > 90:
            self.last_update = pygame.time.get_ticks()
            self.current_frame = (self.current_frame +1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            
            

    def load_images(self):
        self.frames = [self.spritesheet.get_image(226,107,240-226,124-107),
                       self.spritesheet.get_image(249,107,262-249,124-107),
                       self.spritesheet.get_image(270,107,282-270,124-107),
                       self.spritesheet.get_image(294,107,300-294,124-107),
                       self.spritesheet.get_image(317,107,320-317,124-107),
                       self.spritesheet.get_image(337,107,343-337,124-107),
                       self.spritesheet.get_image(355,107,367-355,124-107),
                       self.spritesheet.get_image(377,107,389-377,124-107)]


class CloudGenerator(pygame.sprite.OrderedUpdates):
    def __init__(self):
        super().__init__()
        self.t_ultima_plat = pygame.time.get_ticks()
        
    def update(self):
        super().update()
        #generacio de noves plataformes
        if len(self.group) < 5:
            if pygame.time.get_ticks() - self.t_ultima_plat > 2000:
                width = randrange(WIDTH*(0.15), WIDTH*(0.45))
                c1 = Cloud(randrange(0,WIDTH-width),-100)
                if c1.rect.right > WIDTH:
                    c1.rect.right = WIDTH
                self.add(c1)
                self.t_ultima_plat = pygame.time.get_ticks()
            
    def kill(self):
        for plat in self.group:
            plat.kill()


class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.arena_spritesheet = Spritesheet('img/assets/cloud_sprite.png')
        images = [self.arena_spritesheet.get_image(72,61,268-72,146-61),
                  self.arena_spritesheet.get_image(59,177,280-59,276-177),
                  self.arena_spritesheet.get_image(65,326,244-65,437-326),
                  self.arena_spritesheet.get_image(345,116,529-345,206-116),
                  self.arena_spritesheet.get_image(318,236,520-318,337-236),
                  self.arena_spritesheet.get_image(318,373,507-318,467-373)]
        self.image = choice(images)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel = randint(1,2)
        
    def update(self):
        self.rect.y += self.vel
        if self.rect.top >= HEIGHT:
            self.kill()

class Vortex(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        
        self.spritesheet = Spritesheet('img/assets/vortex.png')
        self.load_images()
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.last_update = pygame.time.get_ticks()
        self.current_frame = 0
        
        
    def update(self):
        self.select_image()
        
    def select_image(self):
        if pygame.time.get_ticks() - self.last_update > 80:#50
            self.last_update = pygame.time.get_ticks()
            self.current_frame = (self.current_frame +1) % len(self.frames)
            self.image = self.frames[self.current_frame]
    
    def load_images(self):
        self.frames = [self.spritesheet.get_image(0,0,124-0,123-0),
                       self.spritesheet.get_image(125,0,252-125,123-0),
                       self.spritesheet.get_image(254,0,380-254,123-0),
                       self.spritesheet.get_image(382,0,506-382,123-0),
                       self.spritesheet.get_image(507,0,636-507,123-0)]


    

  
    
    
        


