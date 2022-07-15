import pygame
import random
from scripts.spriteSheetClass import *
from scripts.settings import *
from scripts.hud import *
vec = pygame.math.Vector2
 
#Mario Stats:
increment = 5
friccio = -0.5
gravetat = 0.8
jump = -14
 
class Single_Mario(pygame.sprite.Sprite):
    def __init__(self,game,pos, proj, all_sprites_group,muted):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.all_sprites_group = all_sprites_group
        self.current_frame = 0
        self.proj = proj
        self.last_update = 0 #permet editar el frame rate de la animacio
        self.spritesheet = Spritesheet('img/heroes/mario_sprite.png')
        self.load_images()
        self.image = self.standing_frames_r[0]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(pos[0], pos[1])
        self.vel = vec(0, 0)
        self.acc = vec(0,0)
        self.jump_counter = 0
        self.jump_max_counter = 2
        self.faceright = True
        self.airborne = False
        self.walking_state = False
        self.go_left = False
        self.go_right = False
        self.jumping_state = False
        self.basic1_state = False
        self.basic2_state = False
        self.try_especial_state = False
        self.especial_state = False
        self.idle_state = True
        self.down_state = False
         
        self.basic1_damage = 0
        self.basic2_damage = 7
        self.especial_damage = 10

        self.basic1_push_x = 4
        self.basic1_push_y = 3
        self.basic2_push_x = 5
        self.basic2_push_y = 4
        self.especial_push_x = 7
        self.especial_push_y = 10
         
        self.max_health = 120
        self.max_cooldown_time = 15000

        self.egg_counter = 0
        self.max_eggs = 3
        self.eggs_collected = False

        self.end_game = False
        self.death_sound = pygame.mixer.Sound("sounds/death_sound.ogg")
        self.life_sound = pygame.mixer.Sound("sounds/mushroom_sound.ogg")
        self.coin_sound = pygame.mixer.Sound("sounds/coin_sound.ogg")
        self.coin_sound.set_volume(0.5)
        self.flame_sound = pygame.mixer.Sound("sounds/fireball_sound.ogg")
        self.especial_sound = pygame.mixer.Sound("sounds/big_mario_sound.ogg")
        self.especial_sound.set_volume(0.05)

        self.jump_sound = pygame.mixer.Sound('sounds/jump1_sound.ogg')
        self.jump_sound.set_volume(0.15)
        
        if muted:
            self.death_sound.set_volume(0)
            self.life_sound.set_volume(0)
            self.coin_sound.set_volume(0)
            self.jump_sound.set_volume(0)
            self.flame_sound.set_volume(0)
            self.especial_sound.set_volume(0)
            
        self.time = pygame.time.get_ticks()
         
    def jump(self):
        self.vel.y = jump
        self.jump_counter += 1
        self.jump_sound.play()
        self.jumping_state = False
 
    def move_left(self):
        self.vel.x = -increment
        self.faceright = False
 
    def move_right(self):
        self.vel.x = increment
        self.faceright = True
         
    def take_damage(self,damage):
            if self.health - damage > 0:
                self.health -= damage
            else:
                self.life -= 1
                self.death_sound.play()
                if self.life != 0: self.health = self.max_health
                
                 
     
    def collide(self):
        if self.vel.y > 0:
            hits = pygame.sprite.collide_rect(self, self.game.ground)
            if hits:
                self.pos.y = self.game.ground.rect.top
                self.airborne = False
                self.vel.y = 0
                self.acc.y = 0
                self.jump_counter = 0
            
            for plat in self.game.platforms:
                if pygame.sprite.collide_rect(self,plat) and not self.down_state:
                    hits2 = pygame.sprite.spritecollide(self, self.game.platforms, False)
                    nearest = hits2[0]
                    if self.rect.centery < plat.rect.top:
                        self.vel.y = 0
                        self.acc.y = 0
                        self.jump_counter = 0
                        self.airborne = False
                        self.pos.y = plat.rect.top + 10
     
            hits3 = pygame.sprite.spritecollide(self, self.game.platmobils, False)
            if hits3:
                nearest = hits3[0]
                if self.pos.y < nearest.rect.bottom:#s'aterra a la plat si el player.rect.bottom supera el plat.rect.top
                    if nearest.vel < 0:
                        self.pos.y = nearest.rect.centery-5
                    else:
                        self.pos.y = nearest.rect.centery+5
                    self.vel.y = 0
                    self.acc.y = 0
                    self.airborne = False
                    self.jump_counter = 0
        hitcoin = pygame.sprite.spritecollide(self,self.game.coins,True)
        if hitcoin:
            self.coin_sound.play()
            if self.coolbar.full:
                pass
            else:
                self.time -= int(self.max_cooldown_time/3)
 
        hitslife = pygame.sprite.spritecollide(self, self.game.powers, True)
        if hitslife:
            self.life_sound.play()
            if self.life == 3:
                self.health += 30
                if self.health > self.max_health:
                    self.health = self.max_health
            else:
                self.health += 30
                if self.health > self.max_health:
                    self.life += 1
                    self.health = 30 - (self.max_health - self.health)
        hitseggs = pygame.sprite.spritecollide(self,self.game.eggs, False)
        
        if hitseggs:
            for egg in self.game.eggs:
                if pygame.sprite.collide_rect(self,egg):
                    #if egg.rect.left > 50:
                    self.egg_counter += 1
                    egg.kill()
                    self.afegir_miniegg()
        if self.eggs_collected:
            if pygame.sprite.spritecollide(self,self.game.vortex, False):
                if self.faceright:
                    self.end_game = True
                
        if pygame.sprite.spritecollide(self,self.game.enemics1, False):
            for e in self.game.enemics1:
                if pygame.sprite.collide_rect(self,e):
                    if e.pos.x > 100:
                        if not self.basic2_state:
                            if self.rect.left < e.rect.left:
                                self.vel.x = -e.push
                            else:
                                self.vel.x = e.push
                            self.take_damage(e.damage)
        if pygame.sprite.spritecollide(self,self.game.enemics2, False):
            for e in self.game.enemics2:
                if e.basic1_state:
                    if pygame.sprite.collide_rect(self,e):
                        if self.rect.left < e.rect.left:
                            self.vel.x = -e.basic1_push_x
                        else:
                            self.vel.x = e.basic1_push_x
                        self.take_damage(e.basic1_damage)
                        
        if pygame.sprite.collide_rect(self,self.game.limit_esquerre):
            if self.vel.x != 0:
                self.vel.x = 5
        if pygame.sprite.collide_rect(self,self.game.limit_dret):
            self.vel.x = -5
            
            
               
                 
    def afegir_miniegg(self):
        num = self.egg_counter
        if num == 1:
            ou = GoldenEggMini(30,160)
            self.game.all_sprites.add(ou)
            self.game.minieggs.add(ou)
        elif num == 2:
            ou = GoldenEggMini(30,200)
            self.game.all_sprites.add(ou)
            self.game.minieggs.add(ou)
        elif num == 3:
            ou = GoldenEggMini(30,240)
            self.game.all_sprites.add(ou)
            self.game.minieggs.add(ou)
            
            

        
    def update(self):
        if self.egg_counter == self.max_eggs:
            self.eggs_collected = True
        self.lifebar.update(self.health, self.life)
        self.coolbar.update(pygame.time.get_ticks(),self.time, self.max_cooldown_time)
        if self.walking_state:
            self.walk_select_image()
            if self.go_left:
                self.move_left()
            if self.go_right:
                self.move_right()
        if self.jumping_state:
            self.jump()
        if self.idle_state:
            self.game.ground.vel = 0
            self.idle_select_image()
        if self.basic1_state:
            self.basic1_select_image()
             
        if self.basic2_state:
            self.basic2_select_image()
 
        if self.try_especial_state:
            if self.coolbar.full:
                self.especial_sound.play()
                self.especial_state = True
                self.time = pygame.time.get_ticks()
             
        if self.especial_state:
            self.especial_select_image()   
                     
        #airborne
        if self.vel.y != 0:
            self.acc.y = gravetat
            self.airborne = True
        else:
            self.airborne = False
        self.collide()        
        if self.airborne:
            if self.vel.y < 0:
                self.jump_select_image()
             
        #equation of motion
        self.pos.x = self.pos.x + self.vel.x
        self.pos.y += self.vel.y + 0.5*self.acc.y
         
        self.acc.y = gravetat
 
        #screen range
        if self.pos.x >= WIDTH*2/3:
            if self.vel.x > 0:
                self.pos.x -= abs(self.vel.x)
                
                     
                for plat in self.game.platforms:
                    plat.rect.x -= abs(self.vel.x)
                for plat in self.game.platmobils:
                    plat.rect.x -= abs(self.vel.x)
                for nuvol in self.game.nuvols:
                    nuvol.rect.x -= abs(self.vel.x)
                for vor in self.game.vortex:
                    vor.rect.x -= abs(self.vel.x)
                for c in self.game.coins:
                    c.rect.x -= abs(self.vel.x)
                for vida in self.game.powers:
                    vida.rect.x -= abs(self.vel.x)
                for egg in self.game.eggs:
                    egg.rect.x -= abs(self.vel.x)
                for e1 in self.game.enemics1:
                    e1.pos.x -= abs(self.vel.x)
                for e2 in self.game.enemics2:
                    e2.pos.x -= abs(self.vel.x)
                for l in self.game.limits:
                    l.rect.x -=abs(self.vel.x)
                 
                 
                         
        if self.pos.x <= WIDTH/3:
            if self.vel.x < 0:
                self.pos.x += abs(self.vel.x)
                
                         
                for plat in self.game.platforms:
                    plat.rect.x += abs(self.vel.x)
                for plat in self.game.platmobils:
                    plat.rect.x += abs(self.vel.x)
                for nuvol in self.game.nuvols:
                    nuvol.rect.x += abs(self.vel.x)
                for vor in self.game.vortex:
                    vor.rect.x += abs(self.vel.x)
                for c in self.game.coins:
                    c.rect.x += abs(self.vel.x)
                for vida in self.game.powers:
                    vida.rect.x += abs(self.vel.x)
                for egg in self.game.eggs:
                    egg.rect.x += abs(self.vel.x)
                for e1 in self.game.enemics1:
                    e1.pos.x += abs(self.vel.x)
                for e2 in self.game.enemics2:
                    e2.pos.x += abs(self.vel.x)
                for l in self.game.limits:
                    l.rect.x +=abs(self.vel.x)
 
        #aplicar friccio 
        self.vel.x += self.vel.x*friccio
        self.vel.y = self.vel.y + self.acc.y
         
        if abs(self.vel.x) < 1:
            self.vel.x = 0
      
         
        if self.pos.y > HEIGHT + 200:
            self.pos.y = 0
            self.pos.x = WIDTH/2
            self.life -=1
            self.health = self.max_health
 
       
 
        self.rect.midbottom = self.pos
     
         
         
    def walk_select_image(self):             
        if pygame.time.get_ticks() - self.last_update > 100:
            self.last_update = pygame.time.get_ticks()
            self.current_frame = (self.current_frame +1) % len(self.walking_frames_r)
            bottom = self.rect.bottom
            if self.vel.x > 0:
                self.image = self.walking_frames_r[self.current_frame]
            else:
                self.image = self.walking_frames_l[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
                 
    def jump_select_image(self):
        if pygame.time.get_ticks() - self.last_update > 80:
            self.last_update = pygame.time.get_ticks()
            self.current_frame = (self.current_frame +1) % len(self.jumping_frames_r)
            bottom = self.rect.bottom
            if self.faceright:
                self.image = self.jumping_frames_r[self.current_frame]
            else:
                self.image = self.jumping_frames_l[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
 
    def idle_select_image(self):
        if pygame.time.get_ticks() - self.last_update > 150:
            self.last_update = pygame.time.get_ticks()
            self.current_frame = (self.current_frame +1) % len(self.standing_frames_r)
            bottom = self.rect.bottom
            if self.faceright:
                self.image = self.standing_frames_r[self.current_frame]
            else:
                self.image = self.standing_frames_l[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
  
    def basic1_select_image(self):
        if pygame.time.get_ticks() - self.last_update > 90:
            self.last_update = pygame.time.get_ticks()
            self.current_frame = (self.current_frame +1) % len(self.basic1_frames_r)
            if self.current_frame == 0:
                self.basic1_state = False
                if len(self.proj) < 1:
                    a = FireBall(self.pos.x, self.pos.y - 15, self)
                    self.flame_sound.play()
                    self.proj.add(a)
                    self.all_sprites_group.add(a)
                bottom = self.rect.bottom
            if self.faceright:
                self.image = self.basic1_frames_r[self.current_frame]
            else:
                self.image = self.basic1_frames_l[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
             
    def basic2_select_image(self):
        if pygame.time.get_ticks() - self.last_update > 100:
            self.last_update = pygame.time.get_ticks()
            self.current_frame = (self.current_frame +1) % len(self.basic2_frames_r)
            if self.current_frame == 0:
                self.basic2_state = False
            bottom = self.rect.bottom
            if self.faceright:
                self.image = self.basic2_frames_r[self.current_frame]
            else:
                self.image = self.basic2_frames_l[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
 
    def especial_select_image(self):
        if pygame.time.get_ticks() - self.last_update > 80:
            self.last_update = pygame.time.get_ticks()
            self.current_frame = (self.current_frame +1) % len(self.especial_frames_r)
            if self.current_frame == 0:
                self.especial_state = False
            bottom = self.rect.bottom
            if self.faceright:
                self.image = pygame.transform.smoothscale(self.especial_frames_r[self.current_frame],(180,152)) #(113,95)
            else:
                self.image = pygame.transform.smoothscale(self.especial_frames_l[self.current_frame],(180,152))
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
     
                         
    def load_images(self):
        #STANDING
        self.standing_frames_r = [self.spritesheet.get_image(296,10,24,38),
                                self.spritesheet.get_image(388,11,26,37),
                                self.spritesheet.get_image(359,10,25,38)]
        self.standing_frames_l = []
 
        for frame in self.standing_frames_r:
            self.standing_frames_l.append(pygame.transform.flip(frame,True,False))
 
        #WALKING
        self.walking_frames_r = [self.spritesheet.get_image(124,65,27,37),
                                self.spritesheet.get_image(153,66,31,36),
                                self.spritesheet.get_image(186,67,32,35),
                                 self.spritesheet.get_image(220,65,25,37),
                                 self.spritesheet.get_image(246,66,32,36),
                                 self.spritesheet.get_image(280,67,35,35)]
        self.walking_frames_l = []
 
        for frame in self.walking_frames_r:
            self.walking_frames_l.append(pygame.transform.flip(frame,True,False))
 
        #JUMPING
        self.jumping_frames_r = [self.spritesheet.get_image(312,255,342-312,296-255)]
        self.jumping_frames_l = []
 
        for frame in self.jumping_frames_r:
            self.jumping_frames_l.append(pygame.transform.flip(frame,True,False))
 
        #BASIC1
            #altres (267,574,51,47)
        self.basic1_frames_r = [self.spritesheet.get_image(314,209,36,36)]
                                   
        self.basic1_frames_l = []
 
        for frame in self.basic1_frames_r:
            self.basic1_frames_l.append(pygame.transform.flip(frame,True,False))
             
        #BASIC2
        self.basic2_frames_r = [self.spritesheet.get_image(41,158,77-41,196-158),
                                self.spritesheet.get_image(79,152,116-79,198-152)]
                                   
        self.basic2_frames_l = []
 
        for frame in self.basic2_frames_r:
            self.basic2_frames_l.append(pygame.transform.flip(frame,True,False))
 
        #ESPECIAL
        self.especial_frames_r = [self.spritesheet.get_image(178,317,223-178,355-317),
                                self.spritesheet.get_image(225,318,270-225,355-318),
                                self.spritesheet.get_image(272,312,295-272,355-312),
                                self.spritesheet.get_image(297,312,342-297,355-312),
                                self.spritesheet.get_image(345,312,367-345,355-312),
                                  self.spritesheet.get_image(178,317,223-178,355-317),
                                self.spritesheet.get_image(225,318,270-225,355-318),
                                self.spritesheet.get_image(272,312,295-272,355-312),
                                self.spritesheet.get_image(297,312,342-297,355-312),
                                self.spritesheet.get_image(345,312,367-345,355-312)]
                                   
        self.especial_frames_l = []
 
        for frame in self.especial_frames_r:
            self.especial_frames_l.append(pygame.transform.flip(frame,True,False))
 
class FireBall(pygame.sprite.Sprite):
    def __init__(self, x, y, owner):
        pygame.sprite.Sprite.__init__(self)
        self.spritesheet = Spritesheet('img/heroes/mario_sprite.png')
        self.load_images()
        self.x = x
        self.damage = 3
        self.max_distance = 100
        self.owner = owner
        if self.owner.faceright:
            self.image = self.fire_ball_frames_r
            self.vel = 2
        else:
            self.image = self.fire_ball_frames_l
            self.vel = -2
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.low_tier = True
             
             
    def update(self):
        self.rect.x += self.vel
        if abs(self.rect.x - self.x) > self.max_distance:
            self.kill()
             
    def load_images(self):
        #tail
        self.fire_ball_frames_r = self.spritesheet.get_image(221,222,239-221,239-222)#82,612,96-82,624-612 / 244,218,269-244,241-218
        self.fire_ball_frames_l = pygame.transform.flip(self.spritesheet.get_image(221,222,239-221,239-222),True,False)
 
class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.Surface((2000,100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
 
    def update(self):
        self.image.fill((0,255,0))
 
      
 
class Single_Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, num):
        pygame.sprite.Sprite.__init__(self)
        self.arena_spritesheet = Spritesheet('img/assets/arena.png')
        images = [self.arena_spritesheet.get_image(97,16,596,23),
                  self.arena_spritesheet.get_image(97,55,263,23),
                  self.arena_spritesheet.get_image(97,91,459,23),
                  self.arena_spritesheet.get_image(97,143,373,23),
                  self.arena_spritesheet.get_image(538,154,115,23)]
        self.image = images[num]
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
         
    def update(self):
        pass
 
class Moving_Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, num, ymin, ymax, vel):
        pygame.sprite.Sprite.__init__(self)
        self.arena_spritesheet = Spritesheet('img/assets/arena.png')
        images = [self.arena_spritesheet.get_image(97,16,596,23),
                  self.arena_spritesheet.get_image(97,55,263,23),
                  self.arena_spritesheet.get_image(97,91,459,23),
                  self.arena_spritesheet.get_image(97,143,373,23),
                  self.arena_spritesheet.get_image(538,154,115,23)]
        self.image = images[num]
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel = vel
        self.ymin= ymin
        self.ymax = ymax
         
    def update(self):
        if self.rect.y < self.ymin:
                self.vel = abs(self.vel)
        if self.rect.y > self.ymax:
            self.vel = -abs(self.vel)
        self.rect.y += self.vel
 
class xMoving_Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, num, xmin, xmax, vel):
        pygame.sprite.Sprite.__init__(self)
        self.arena_spritesheet = Spritesheet('img/assets/arena.png')
        images = [self.arena_spritesheet.get_image(97,16,596,23),
                  self.arena_spritesheet.get_image(97,55,263,23),
                  self.arena_spritesheet.get_image(97,91,459,23),
                  self.arena_spritesheet.get_image(97,143,373,23),
                  self.arena_spritesheet.get_image(538,154,115,23)]
        self.image = images[num]
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel = vel
        self.xmin= xmin
        self.xmax = xmax
         
    def update(self):
        if self.rect.x > self.xmax:
                self.vel = -abs(self.vel)
        if self.rect.x < self.xmin:
            self.vel = abs(self.vel)
        self.rect.x += self.vel
         
 
class Cloud2(pygame.sprite.Sprite):
    def __init__(self, x, y, num):
        pygame.sprite.Sprite.__init__(self)
        self.arena_spritesheet = Spritesheet('img/assets/cloud_sprite.png')
        images = [self.arena_spritesheet.get_image(72,61,268-72,146-61),
                  self.arena_spritesheet.get_image(59,177,280-59,276-177),
                  self.arena_spritesheet.get_image(65,326,244-65,437-326),
                  self.arena_spritesheet.get_image(345,116,529-345,206-116),
                  self.arena_spritesheet.get_image(318,236,520-318,337-236),
                  self.arena_spritesheet.get_image(318,373,507-318,467-373)]
        self.image = images[num]
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
         
    def update(self):
        pass
 
class Vortex2(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        #self.game = game
         
        self.spritesheet = Spritesheet('img/assets/vortex.png')
        self.load_images()
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.pos = vec(x,y)
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
 
 
class Coin2(pygame.sprite.Sprite):
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
 
class PowerUp2(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = Spritesheet('img/assets/power_up_sprite.png').get_image(178,97,209-178,130-97)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y
         
    def update(self):
        pass
 
class GoldenEgg(pygame.sprite.Sprite):
    def __init__ (self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = Spritesheet('img/assets/golden_egg.png').get_image(0, 0, 64, 67)
        self.rect = self.image.get_rect()
        self.image.set_colorkey((0,0,0))
        self.image = pygame.transform.scale(self.image,(43,45))
        self.rect.x = x
        self.rect.bottom = y

class GoldenEggMini(pygame.sprite.Sprite):
    def __init__ (self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = Spritesheet('img/assets/golden_egg.png').get_image(0, 0, 64, 67)
        self.rect = self.image.get_rect()
        self.image.set_colorkey((0,0,0))
        self.image = pygame.transform.scale(self.image,(22,23))
        self.rect.x = x
        self.rect.bottom = y

class Enemic1(pygame.sprite.Sprite):
    def __init__(self,game, x, y,plat,oponent):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.oponent = oponent
        self.image = Spritesheet('img/assets/power_up_sprite.png').get_image(178,134,209-178,167-134)
        self.rect = self.image.get_rect()
        self.plat = plat
        self.pos = vec(x,y)
        self.vel = 1
        self.damage = 10
        self.push = 30
        self.gravetat = 1
        self.health = 1
        
    def update(self):
        if pygame.sprite.spritecollide(self, self.oponent.proj, True):
            self.kill()
        if pygame.sprite.collide_rect(self,self.plat):
            self.pos.y = self.plat.rect.top
            
        if pygame.sprite.collide_rect(self, self.oponent):
            if self.oponent.basic1_state:
                self.kill()
            elif self.oponent.basic2_state:
                self.kill()
            elif self.oponent.especial_state:
                self.kill()         
            
        if self.rect.right == self.plat.rect.right:
            self.vel = -1
        if self.rect.left == self.plat.rect.left:
            self.vel = 1
        self.pos.x += self.vel
        self.pos.y +=self.gravetat
        if pygame.sprite.collide_rect(self,self.game.ground):
            self.kill()
        
        self.rect.midbottom = self.pos

class Enemic2(pygame.sprite.Sprite):
    def __init__(self,game,pos, proj, oponent):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.current_frame = 0
        self.proj = proj
        self.oponent = oponent
        self.last_update = 0 #permet editar el frame rate de la animacio
        self.spritesheet = Spritesheet('img/heroes/sonic.png')
        self.load_images()
        self.image = self.standing_frames_r[0]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(pos[0], pos[1])
        self.vel = vec(0, 0)
        self.acc = vec(0,0)
        self.faceright = False
        self.walking_state = False
        self.go_left = False
        self.go_right = False
        self.basic1_state = False
        self.idle_state = True
            
        self.basic1_push_x = 20
        self.basic1_push_y = 10
                
        self.basic1_damage = 12
        self.attack_speed = 70 
        self.increment = 3
        self.gravetat = 1
        self.friccio = -0.5
        self.gravetat = 1
        self.max_health = 70

        self.health = self.max_health
        self.life = 1
    
        self.healthbar = MiniHealthBar(self.max_health, self.rect.centerx, self.rect.top)
        
        self.agressive_state = False
   
      

    def move_left(self):
        self.vel.x = -self.increment
        self.faceright = False

    def move_right(self):
        self.vel.x = self.increment
        self.faceright = True
        
    def take_damage(self,damage):
            if self.health - damage > 0:
                self.health -= damage
            else:
                self.life -= 1
                if self.life != 0: self.health = self.max_health
                self.pos.y = 0
                self.pos.x = WIDTH/2
                
    
    def collide(self):
        if pygame.sprite.spritecollide(self, self.game.platforms, False):
            for p in self.game.platforms:
                if pygame.sprite.collide_rect(self,p):
                    self.pos.y = p.rect.top+10
                    
                    if pygame.sprite.collide_rect(self.oponent, p):
                        
                        self.agressive_state = True
                        self.walking_state = True
                    else:
                        self.agressive_state = False
                        self.walking_state = False
        if pygame.sprite.collide_rect(self,self.game.ground):
            self.kill()
                    
        hits3 = pygame.sprite.spritecollide(self, self.oponent.proj, False)
        for projectil in hits3:
            self.take_damage(projectil.damage)
            
            if self.rect.centerx - hits3[0].rect.centerx < 0: 
                self.pos.x -= 50 
            else:
                self.pos.x += 50
            if projectil.low_tier:
                projectil.kill()
   
        if pygame.sprite.collide_rect(self, self.oponent):
            if self.oponent.basic1_state:
                self.get_hit_by_basic1()
                self.take_damage(self.oponent.basic1_damage)                
            if self.oponent.basic2_state:
                self.get_hit_by_basic2()
                self.take_damage(self.oponent.basic2_damage)
            if self.oponent.especial_state:
                self.get_hit_by_especial()
                self.take_damage(self.oponent.especial_damage)
                
                        
    def attack(self):
        n = random.randint(1,40)
        if n == 1:
            self.basic1_state = True
                   
    def think(self):                
        if self.agressive_state:        
            if abs(self.pos.x - self.oponent.pos.x) < 35:
                self.walking_state = False
                self.go_left = False
                self.go_right = False
                self.attack()
            else:
                if self.pos.x < self.oponent.pos.x:
                    self.go_right = True
                    self.go_left = False
                else:
                    self.go_left = True
                    self.go_right = False
                self.walking_state = True
            
        if self.pos.x - self.oponent.pos.x > 0:
            self.faceright = False
        else:
            self.faceright = True
                                      
          
    def update(self):
        self.think()
        self.healthbar.update(self.health, self.rect.centerx, self.rect.top)
        if self.walking_state:
            self.walk_select_image()
            if self.go_left:
                self.move_left()
            if self.go_right:
                self.move_right()
        if self.idle_state:
            self.idle_select_image()
        if self.basic1_state:
            self.basic1_select_image()
        self.collide()

        if self.life != 1:
        
            self.kill()
        
        
            
        #equation of motion
        self.pos.x = self.pos.x + self.vel.x
        self.pos.y += self.gravetat
        

        #aplicar friccio 
        self.vel.x += self.vel.x*self.friccio
        
        
        if abs(self.vel.x) < 1:
            self.vel.x = 0
     
        self.rect.midbottom = self.pos
        

    def get_hit_by_basic1(self):
        
        if self.oponent.faceright:
            self.vel.x = self.oponent.basic1_push_x
                       
        else:
            self.vel.x = -self.oponent.basic1_push_x
                        
    def get_hit_by_basic2(self):
        if self.oponent.faceright:
            self.vel.x = self.oponent.basic2_push_x
            
        else:
            self.vel.x = -self.oponent.basic2_push_x
        
            
    def get_hit_by_especial(self):
        self.kill()
        
    def walk_select_image(self):             
        if pygame.time.get_ticks() - self.last_update > 100:
            self.last_update = pygame.time.get_ticks()
            self.current_frame = (self.current_frame +1) % len(self.walking_frames_r)
            bottom = self.rect.bottom
            if self.vel.x > 0:
                self.image = self.walking_frames_r[self.current_frame]
            else:
                self.image = self.walking_frames_l[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
                

    def idle_select_image(self):
        if pygame.time.get_ticks() - self.last_update > 150:
            self.last_update = pygame.time.get_ticks()
            self.current_frame = (self.current_frame +1) % len(self.standing_frames_r)
            bottom = self.rect.bottom
            if self.faceright:
                self.image = self.standing_frames_r[self.current_frame]
            else:
                self.image = self.standing_frames_l[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
 
    def basic1_select_image(self):
        if pygame.time.get_ticks() - self.last_update > self.attack_speed:
            self.last_update = pygame.time.get_ticks()
            self.current_frame = (self.current_frame +1) % len(self.basic1_frames_r)
            if self.current_frame == 0:
                self.basic1_state = False
            bottom = self.rect.bottom
            if self.faceright:
                self.image = self.basic1_frames_r[self.current_frame]
            else:
                self.image = self.basic1_frames_l[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
                
                        
    def load_images(self):
        #STANDING
        self.standing_frames = [self.spritesheet.get_image(31,36,23,33),
                                self.spritesheet.get_image(58,34,23,34),
                                self.spritesheet.get_image(86,33,25,35),
                                self.spritesheet.get_image(115,33,25,35),
                                self.spritesheet.get_image(145,36,27,32)]
        self.standing_frames_l = []
        self.standing_frames_r = []

        for frame in self.standing_frames:
            frame = pygame.transform.scale(frame,(int(frame.get_width()*1.3),int(frame.get_height()*1.3)))
            self.standing_frames_r.append(frame)
            self.standing_frames_l.append(pygame.transform.flip(frame,True,False))

        #WALKING
        self.walking_frames = [self.spritesheet.get_image(32,82,33,34),
                                self.spritesheet.get_image(67,81,34,34),
                                self.spritesheet.get_image(105,83,34,33),
                                 self.spritesheet.get_image(146,83,35,33)]
        self.walking_frames_l = []
        self.walking_frames_r = []

        for frame in self.walking_frames:
            frame = pygame.transform.scale(frame,(int(frame.get_width()*1.3),int(frame.get_height()*1.3)))
            self.walking_frames_r.append(frame)
            self.walking_frames_l.append(pygame.transform.flip(frame,True,False))
        

        #BASIC1
        self.basic1_frames = [self.spritesheet.get_image(24,277,51-24,309-277),
                              self.spritesheet.get_image(55,276,81-55,309-276),
                              self.spritesheet.get_image(89,274,33,34),
                              self.spritesheet.get_image(126,274,32,34),
                              self.spritesheet.get_image(166,275,199-166,308-275),
                              self.spritesheet.get_image(203,274,40,34),
                              self.spritesheet.get_image(249,274,287-249,307-274),
                              self.spritesheet.get_image(294,274,323-294,308-274)]
                                  
        self.basic1_frames_l = []
        self.basic1_frames_r = []

        for frame in self.basic1_frames:
            frame = pygame.transform.scale(frame,(int(frame.get_width()*1.3),int(frame.get_height()*1.3)))
            self.basic1_frames_r.append(frame)
            self.basic1_frames_l.append(pygame.transform.flip(frame,True,False))
            
class MiniHealthBar(pygame.sprite.Sprite):
    def __init__(self, max_health,centerx, top):
        pygame.sprite.Sprite.__init__(self)
        self.color = (0,204,0)
        self.width = 50
        self.height = 10
        self.max_health = max_health
        self.image = pygame.Surface((self.width,self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.bottom = top
        
    def update(self,health,center,top):
        self.rect.centerx = center
        self.rect.bottom = top - 10
        self.color = (0,204,0)
        
        self.image = pygame.Surface((health*self.width/self.max_health, self.height))
        self.image.fill(self.color)

class Arbust1(pygame.sprite.Sprite):
    def __init__ (self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = Spritesheet('img/assets/bg.png').get_image(0, 128, 217, 235-128)
        self.rect = self.image.get_rect()
        self.image.set_colorkey((0,0,0))
        self.rect.x = x
        self.rect.bottom = y
        
class Bloc1(pygame.sprite.Sprite):
    def __init__ (self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = Spritesheet('img/assets/bg.png').get_image(249, 249, 558-249, 409-249)
        self.rect = self.image.get_rect()
        self.image.set_colorkey((0,0,0))
        self.rect.x = x
        self.rect.bottom = y

class Limit(pygame.sprite.Sprite):
    def __init__ (self, x, y,tipus):
        pygame.sprite.Sprite.__init__(self)
        if tipus == 'ESQUERRE':
            self.image = Spritesheet('img/assets/bg.png').get_image(1320, 0, 1582-1320, 491-0)
        if tipus == 'DRET':
            self.image = Spritesheet('img/assets/bg.png').get_image(1031, 392, 1294-1031, 881-392)
        self.rect = self.image.get_rect()
        self.image.set_colorkey((0,0,0))
        self.rect.x = x
        self.rect.bottom = y

