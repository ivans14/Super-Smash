import pygame
from scripts.spriteSheetClass import *
from scripts.settings import *
from scripts.hud import *
vec = pygame.math.Vector2

#Kirby Stats:
increment = 3.5
friccio = -0.5
gravetat = 0.65
jump = -13

class Kirby(pygame.sprite.Sprite):
    def __init__(self,game,pos, proj, all_sprites_group, muted):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.all_sprites_group = all_sprites_group
        self.current_frame = 0
        self.proj = proj
        self.last_update = 0 #permet editar el frame rate de la animacio
        self.spritesheet = Spritesheet('img/heroes/kirby_sprite.png')
        self.load_images()
        self.image = self.standing_frames_r[0]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(pos[0], pos[1])
        self.vel = vec(0, 0)
        self.acc = vec(0,0)
        self.jump_counter = 0
        self.jump_max_counter = 3
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
        self.atacant = False
    
        self.basic1_push_x = 20
        self.basic1_push_y = 10
        self.basic2_push_x = 0
        self.basic2_push_y = 0
        self.especial_push_x = 40
        self.especial_push_y = 8
        
        
        self.basic1_damage = 8
        self.basic2_damage = 4
        self.especial_damage = 60
        
        self.max_health = 200
        self.max_cooldown_time = 12000
        
        self.time = pygame.time.get_ticks()

        self.death_sound = pygame.mixer.Sound("sounds/death_sound.ogg")
        self.life_sound = pygame.mixer.Sound("sounds/mushroom_sound.ogg")
        self.coin_sound = pygame.mixer.Sound("sounds/coin_sound.ogg")
        self.coin_sound.set_volume(0.25)
        self.especial_sound = pygame.mixer.Sound("sounds/kirby_especial_sound.ogg")

        self.jump_sound = pygame.mixer.Sound('sounds/jump3_sound.ogg')
        self.jump_sound.set_volume(0.25)
        
        if muted:
            self.death_sound.set_volume(0)
            self.life_sound.set_volume(0)
            self.coin_sound.set_volume(0)
            self.jump_sound.set_volume(0)
            self.especial_sound.set_volume(0)
        
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
                self.death_sound.play()
                self.life -= 1
                if self.life != 0: self.health = self.max_health
                self.pos.y = 0
                self.pos.x = WIDTH/2
                
    
    def collide(self):
        if self.vel.y > 0:
            hits = pygame.sprite.collide_rect(self, self.game.stadium)
            if hits:
                if self.rect.bottom < self.game.stadium.rect.top + 50:
                    self.pos.y = self.game.stadium.rect.top + 30
                    self.airborne = False
                    self.vel.y = 0
                    self.jump_counter = 0
                if self.especial_state:
                    self.especial_state = False
                    
                
            hits2 = pygame.sprite.spritecollide(self, self.game.platforms, False)
            if not self.down_state:
                if hits2 and not hits and not self.especial_state:
                    nearest = hits2[0]
                    for hit in hits2: #busquem quina es la plat més propera al jugador per a fer la colisio
                        if hit.rect.bottom > nearest.rect.bottom:
                            nearest = hit
                    if self.pos.y < nearest.rect.bottom:#s'aterra a la plat si el player.rect.bottom supera el plat.rect.top
                        self.pos.y = nearest.rect.centery
                        self.vel.y = 0
                        self.airborne = False
                        self.jump_counter = 0
                if hits2 and self.rect.bottom>self.game.stadium.rect.top +60 and not self.especial_state:
                        nearest = hits2[0]
                        for hit in hits2: #busquem quina es la plat més propera al jugador per a fer la colisio
                            if hit.rect.bottom > nearest.rect.bottom:
                                nearest = hit
                        if self.pos.y < nearest.rect.bottom:#s'aterra a la plat si el player.rect.bottom supera el plat.rect.top
                            self.pos.y = nearest.rect.centery
                            self.vel.y = 0
                            self.airborne = False
                            self.jump_counter = 0
                    
        hits3 = pygame.sprite.spritecollide(self, self.oponent.proj, False)
        for projectil in hits3:
            self.take_damage(projectil.damage)#POSAR DAMAGE AL PROJECTIL
            
            if self.rect.centerx - hits3[0].rect.centerx < 0: 
                self.pos.x -= 50 #POSAR PUSH PROJECTIL.PUSH
            else:
                self.pos.x += 50
            if projectil.low_tier:
                projectil.kill()
        hits4 = pygame.sprite.collide_rect(self, self.oponent)
        if hits4:
            if self.oponent.basic1_state:
                self.get_hit_by_basic1()
                self.take_damage(self.oponent.basic1_damage)                
            if self.oponent.basic2_state:
                self.get_hit_by_basic2()
                self.take_damage(self.oponent.basic2_damage)
            #EXCEPCIO PELS QUE TENEN ESPECIAL COS A COS (MARIO KIRBY)
            if self.oponent.especial_state:
                self.get_hit_by_especial()
                self.take_damage(self.oponent.especial_damage)
        hits5 = pygame.sprite.spritecollide(self, self.life_gr, True)
        if hits5:
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
        hits6 = pygame.sprite.spritecollide(self, self.coins, True)
        if hits6:
            self.coin_sound.play()
            if self.coolbar.full:
                pass
            else:
                self.time -= int(self.max_cooldown_time/3)

         
                
          
    def update(self):
        self.lifebar.update(self.health, self.life)
        self.tag.update(self.rect.centerx, self.rect.top)
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
            self.idle_select_image()
        if self.basic1_state:
            self.basic1_select_image()
            
        if self.basic2_state:
            self.basic2_select_image()

        if self.try_especial_state:
            if self.coolbar.full:
                self.especial_state = True
                self.time = pygame.time.get_ticks()
            
        if self.especial_state:
            self.jump_counter = self.jump_max_counter
            self.especial_select_image()   
                    
        #airborne
        if self.vel.y != 0:
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

        #aplicar friccio 
        self.vel.x += self.vel.x*friccio
        self.vel.y = self.vel.y + self.acc.y
        
        if abs(self.vel.x) < 1:
            self.vel.x = 0
     
        #screen range
        if self.pos.x > WIDTH:
            self.pos.y = 0
            self.pos.x = WIDTH/2
            self.death_sound.play()
            self.life -=1
            self.health = self.max_health
            if self.especial_state:
                self.especial_state = False
                            
        if self.pos.x < 0:
            self.pos.y = 0
            self.pos.x = WIDTH/2
            self.death_sound.play()
            self.life -=1
            self.health = self.max_health
            if self.especial_state:
                self.especial_state = False

        if self.rect.top > HEIGHT:
            self.vel.y = 0
            self.pos.y = 0
            self.pos.x = WIDTH/2
            self.death_sound.play()
            self.life -=1
            self.health = self.max_health
            if self.especial_state:
                self.especial_state = False

        self.rect.midbottom = self.pos

    def get_hit_by_basic1(self):
        if self.oponent.faceright:
            self.vel.x = self.oponent.basic1_push_x
            self.vel.y = -self.oponent.basic1_push_y
            
        else:
            self.vel.x = -self.oponent.basic1_push_x
            self.vel.y = -self.oponent.basic1_push_y
            
    def get_hit_by_basic2(self):
        if self.oponent.faceright:
            self.vel.x = self.oponent.basic2_push_x
            self.vel.y = -self.oponent.basic2_push_y
        else:
            self.vel.x = -self.oponent.basic2_push_x
            self.vel.y = -self.oponent.basic2_push_y
            
    def get_hit_by_especial(self):
        if self.oponent.faceright:
            self.vel.x = self.oponent.especial_push_x
            self.vel.y = -self.oponent.especial_push_y
        else:
            self.vel.x = -self.oponent.especial_push_x
            self.vel.y = -self.oponent.especial_push_y
        
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
        if pygame.time.get_ticks() - self.last_update > 70:
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
                self.atacant = False
            bottom = self.rect.bottom
            if self.faceright:
                self.image = self.basic1_frames_r[self.current_frame]
            else:
                self.image = self.basic1_frames_l[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
            
    def basic2_select_image(self):
        if pygame.time.get_ticks() - self.last_update > 90:
            self.last_update = pygame.time.get_ticks()
            self.current_frame = (self.current_frame +1) % len(self.basic2_frames_r)
            if self.current_frame == 4:
                if len(self.proj) < 1:
                    a = Swing(self.pos.x, self.pos.y - 15, self, self.game.platforms, self.game.stadium)
                    #self.flame_sound.play()
                    self.proj.add(a)
                    self.all_sprites_group.add(a)
            if self.current_frame == 0:
                self.basic2_state = False
                self.atacant = False
            bottom = self.rect.bottom
            if self.faceright:
                self.image = self.basic2_frames_r[self.current_frame]
            else:
                self.image = self.basic2_frames_l[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom

    def especial_select_image(self):
        if pygame.time.get_ticks() - self.last_update > 60:
            self.last_update = pygame.time.get_ticks()
            self.image = self.especial_frame
            self.rect = self.image.get_rect()
    
                        
    def load_images(self):
        #STANDING
        self.standing_frames = [self.spritesheet.get_image(208,33,28,22),
                                self.spritesheet.get_image(242,34,28,21)]
                                
        self.standing_frames_l = []
        self.standing_frames_r = []

        for frame in self.standing_frames:
            frame = pygame.transform.scale(frame,(int(frame.get_width()*1.3),int(frame.get_height()*1.3)))
            self.standing_frames_r.append(frame)
            self.standing_frames_l.append(pygame.transform.flip(frame,True,False))

        #WALKING
        self.walking_frames = [self.spritesheet.get_image(66,93,28,23),
                                self.spritesheet.get_image(100,92,25,24),
                                self.spritesheet.get_image(131,92,22,24),
                                 self.spritesheet.get_image(159,92,22,24),
                                 self.spritesheet.get_image(188,93,24,23),
                                 self.spritesheet.get_image(218,92,22,24),
                                 self.spritesheet.get_image(246,92,22,24),
                                 self.spritesheet.get_image(274,92,25,24)]
        self.walking_frames_l = []
        self.walking_frames_r = []

        for frame in self.walking_frames:
            frame = pygame.transform.scale(frame,(int(frame.get_width()*1.3),int(frame.get_height()*1.3)))
            self.walking_frames_r.append(frame)
            self.walking_frames_l.append(pygame.transform.flip(frame,True,False))

        #JUMPING
        self.jumping_frames = [self.spritesheet.get_image(65,162,90-65,190-162),
                               self.spritesheet.get_image(96,164,121-96,190-164)]
                               
        self.jumping_frames_l = []
        self.jumping_frames_r = []

        for frame in self.jumping_frames:
            frame = pygame.transform.scale(frame,(int(frame.get_width()*1.3),int(frame.get_height()*1.3)))
            self.jumping_frames_r.append(frame)
            self.jumping_frames_l.append(pygame.transform.flip(frame,True,False))


        #BASIC1
        self.basic1_frames = [self.spritesheet.get_image(173,196,34,22)]
                                  
        self.basic1_frames_l = []
        self.basic1_frames_r = []

        for frame in self.basic1_frames:
            frame = pygame.transform.scale(frame,(int(frame.get_width()*1.3),int(frame.get_height()*1.3)))
            self.basic1_frames_r.append(frame)
            self.basic1_frames_l.append(pygame.transform.flip(frame,True,False))
            
        #BASIC2
        self.basic2_frames = [self.spritesheet.get_image(599,877,639-599,922-877),
                              self.spritesheet.get_image(461,879,503-461,923-879),
                              self.spritesheet.get_image(509,865,543-509,922-865),
                              self.spritesheet.get_image(549,888,593-549,923-888),
                              self.spritesheet.get_image(599,877,639-599,922-877)]
        '''
                              self.spritesheet.get_image(469,745,506-469,768-745),
                              self.spritesheet.get_image(512,744,534-512,768-744),
                              self.spritesheet.get_image(233,745,289-233,770-745),
                              self.spritesheet.get_image(294,744,333-294,771-744),
                              self.spritesheet.get_image(339,744,362-339,774-744),
                              self.spritesheet.get_image(368,744,405-368,772-744),
                              self.spritesheet.get_image(411,745,463-411,768-745)
        '''
                              
                                  
        self.basic2_frames_l = []
        self.basic2_frames_r = []

        for frame in self.basic2_frames:
            frame = pygame.transform.scale(frame,(int(frame.get_width()*1.3),int(frame.get_height()*1.3)))
            self.basic2_frames_r.append(frame)
            self.basic2_frames_l.append(pygame.transform.flip(frame,True,False))

        #ESPECIAL
        self.especial_frame = pygame.transform.smoothscale(self.spritesheet.get_image(258,954,284-258,973-954),(100,100))
                                  
class Swing(pygame.sprite.Sprite):
    def __init__(self, x, y, owner, plat,stadi):
        pygame.sprite.Sprite.__init__(self)
        self.plat = plat
        self.spritesheet = Spritesheet('img/heroes/kirby_sprite.png')
        self.load_images()
        self.x = x
        self.damage = 5
        self.max_distance = 200
        self.owner = owner
        if self.owner.faceright:
            self.image = self.swing_frames_r
            self.vel = 3
        else:
            self.image = self.swing_frames_l
            self.vel = -3
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.low_tier = True
        self.on_plat = pygame.sprite.spritecollide(self, self.plat, False)
        self.on_air = self.owner.airborne
        self.stadi = stadi
        self.on_stadi = pygame.sprite.collide_rect(self, self.stadi)
            
            
    def update(self):
        self.rect.x += self.vel
        if self.on_air:
            self.rect.y+= 1
        if self.on_plat and not self.on_stadi:
            self.rect.y+= 1
        if self.rect.left < 40:
            self.kill()            
        
        if abs(self.rect.x - self.x) > self.max_distance:
            self.kill()
            
    def load_images(self):
        self.swing_frames_r = pygame.transform.scale(self.spritesheet.get_image(646,888,688-646,922-888),(int(self.spritesheet.get_image(646,888,688-646,922-888).get_width()*1.3),int(self.spritesheet.get_image(646,888,688-646,922-888).get_height()*1.3))) 
        self.swing_frames_l = pygame.transform.flip(self.swing_frames_r,True,False)

