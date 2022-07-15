import pygame
from scripts.spriteSheetClass import *
from scripts.settings import *
from scripts.hud import *
vec = pygame.math.Vector2

#Goku Stats:
increment = 5
friccio = -0.5
gravetat = 1
jump = -16

class Goku(pygame.sprite.Sprite):
    def __init__(self,game,pos, proj, all_sprites_group,muted):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.all_sprites_group = all_sprites_group
        self.current_frame = 0
        self.proj = proj
        self.last_update = 0 #permet editar el frame rate de la animacio
        self.spritesheet = Spritesheet('img/heroes/kid_goku.png')
        self.load_images()
        self.image = self.standing_frames_r[0]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(pos[0], pos[1])
        self.vel = vec(0, 0)
        self.acc = vec(0,0)
        self.jump_counter = 0
        self.jump_max_counter = 2
        self.atacant = False
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
    
        self.basic1_push_x = 20
        self.basic1_push_y = 10
        self.basic2_push_x = 30
        self.basic2_push_y = 8
        self.especial_push_x = 0
        self.especial_push_y = 0
        
        
        self.basic1_damage = 5
        self.basic2_damage = 9
        self.especial_damage = 50
        
        self.max_health = 100
        self.max_cooldown_time = 15000
        
        
        self.time = pygame.time.get_ticks()

        self.death_sound = pygame.mixer.Sound("sounds/death_sound.ogg")
        self.life_sound = pygame.mixer.Sound("sounds/mushroom_sound.ogg")
        self.coin_sound = pygame.mixer.Sound("sounds/coin_sound.ogg")
        self.coin_sound.set_volume(0.25)
        self.kamehame_sound = pygame.mixer.Sound("sounds/kamehame_sound.ogg")

        self.jump_sound = pygame.mixer.Sound('sounds/jump1_sound.ogg')
        self.jump_sound.set_volume(0.25)
        
        if muted:
            self.death_sound.set_volume(0)
            self.life_sound.set_volume(0)
            self.coin_sound.set_volume(0)
            self.jump_sound.set_volume(0)
            self.kamehame_sound.set_volume(0)
            
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
                else:
                    pass
                
            hits2 = pygame.sprite.spritecollide(self, self.game.platforms, False)
            if not self.down_state:
                if hits2 and not hits:
                    nearest = hits2[0]
                    for hit in hits2: #busquem quina es la plat més propera al jugador per a fer la colisio
                        if hit.rect.bottom > nearest.rect.bottom:
                            nearest = hit
                    if self.pos.y < nearest.rect.bottom:#s'aterra a la plat si el player.rect.bottom supera el plat.rect.top
                        self.pos.y = nearest.rect.centery
                        self.vel.y = 0
                        self.airborne = False
                        self.jump_counter = 0
                if hits2 and self.rect.bottom>self.game.stadium.rect.top +60:
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
            #EXCEPCIO PELS QUE TENEN ESPECIAL COS A COS (MARIO KIRBY SONIC)
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
            self.especial_state = False
            self.walk_select_image()
            if self.go_left:
                self.move_left()
            if self.go_right:
                self.move_right()
        if self.jumping_state:
            self.especial_state = False
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
                            
        if self.pos.x < 0:
            self.pos.y = 0
            self.pos.x = WIDTH/2
            self.death_sound.play()
            self.life -=1
            self.health = self.max_health

        if self.rect.top > HEIGHT:
            self.vel.y = 0
            self.pos.y = 0
            self.pos.x = WIDTH/2
            self.death_sound.play()
            self.life -=1
            self.health = self.max_health

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
                self.atacant = False
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
                self.atacant = False
            bottom = self.rect.bottom
            if self.faceright:
                self.image = self.basic2_frames_r[self.current_frame]
            else:
                self.image = self.basic2_frames_l[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom

    def especial_select_image(self):
        if pygame.time.get_ticks() - self.last_update > 100:
            self.last_update = pygame.time.get_ticks()
            self.current_frame = (self.current_frame +1) % len(self.especial_frames_r)
            if self.current_frame == 0:
                self.especial_state = False
            if self.especial_state:
                if len(self.proj)<1:
                    self.kamehame_sound.play()
                    a = Kamehame(self.pos.x, self.pos.y - 15,self,self.game.platforms, self.game.stadium)
                    if self.faceright:
                        a.vel = 4
                    else:
                        a.vel = -4
                    self.proj.add(a)
                    self.all_sprites_group.add(a)
                
            bottom = self.rect.bottom
            if self.faceright:
                self.image = self.especial_frames_r[self.current_frame]
            else:
                self.image = self.especial_frames_l[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
    
                        
    def load_images(self):
        #STANDING
        self.standing_frames_r = [self.spritesheet.get_image(11,150,26,41),
                                self.spritesheet.get_image(42,148,25,44),
                                self.spritesheet.get_image(73,150,26,41)]
        self.standing_frames_l = []

        for frame in self.standing_frames_r:
            self.standing_frames_l.append(pygame.transform.flip(frame,True,False))

        #WALKING
        self.walking_frames_r = [self.spritesheet.get_image(9,195,27,39),
                                self.spritesheet.get_image(46,195,28,38),
                                self.spritesheet.get_image(78,196,29,37),
                                 self.spritesheet.get_image(113,195,27,38),
                                 self.spritesheet.get_image(142,193,29,38),
                                 self.spritesheet.get_image(174,195,28,39),
                                 self.spritesheet.get_image(206,196,28,38),
                                 self.spritesheet.get_image(243,197,27,38)]
        self.walking_frames_l = []

        for frame in self.walking_frames_r:
            self.walking_frames_l.append(pygame.transform.flip(frame,True,False))

        #JUMPING
        self.jumping_frames_r = [self.spritesheet.get_image(52,289,82-52,328-289),
                                 self.spritesheet.get_image(89,290,118-89,321-290)]
        self.jumping_frames_l = []

        for frame in self.jumping_frames_r:
            self.jumping_frames_l.append(pygame.transform.flip(frame,True,False))

        #BASIC1
        self.basic1_frames_r = [self.spritesheet.get_image(4,427,44,32),
                                  self.spritesheet.get_image(53,425,34,33),
                                  self.spritesheet.get_image(94,426,34,32),
                                  self.spritesheet.get_image(140,422,53,36),
                                  self.spritesheet.get_image(198,421,72,37),
                                  self.spritesheet.get_image(271,422,145,39)]
                                  
        self.basic1_frames_l = []

        for frame in self.basic1_frames_r:
            self.basic1_frames_l.append(pygame.transform.flip(frame,True,False))
            
        #BASIC2
        self.basic2_frames_r = [self.spritesheet.get_image(404,468,30,39)]
                                  
        self.basic2_frames_l = []

        for frame in self.basic2_frames_r:
            self.basic2_frames_l.append(pygame.transform.flip(frame,True,False))

        #ESPECIAL
        self.especial_frames_r = [self.spritesheet.get_image(135,562,32,35),
                                  self.spritesheet.get_image(172,564,33,33),
                                  self.spritesheet.get_image(135,562,32,35),
                                  self.spritesheet.get_image(172,564,33,33)]
                                  
                                  
        self.especial_frames_l = []

        for frame in self.especial_frames_r:
            self.especial_frames_l.append(pygame.transform.flip(frame,True,False))

class Kamehame(pygame.sprite.Sprite):
    def __init__(self, x, y, owner, plat, stadi):
        pygame.sprite.Sprite.__init__(self)
        self.spritesheet = Spritesheet('img/heroes/kid_goku.png')
        self.load_images()
        self.x = x
        self.damage = 40
        self.image = self.head_kame_frames_r[0]
        self.vel = 4
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.low_tier = True #False si no vull que desapareixi al contacte
        self.owner = owner
        self.plat = plat
        self.on_plat = pygame.sprite.spritecollide(self, self.plat, False)
        self.on_air = self.owner.airborne
        self.stadi = stadi
        self.on_stadi = pygame.sprite.collide_rect(self, self.stadi)
        
    def update(self):
        if self.vel > 0:
            self.image = self.head_kame_frames_l[0]
        else:
            self.image = self.head_kame_frames_r[0]
            
        self.rect.x += self.vel
        if self.on_air:
            self.rect.y+= 1
        if self.on_plat and not self.on_stadi:
            self.rect.y+= 1
            
        if self.rect.left > WIDTH:
            self.kill()
        if self.rect.left<60:
            self.kill()
            
    def load_images(self):
        #tail
        self.tail_kame_frames_r = [self.spritesheet.get_image(263,629,16,22)]
        self.tail_kame_frames_l = [pygame.transform.flip(self.spritesheet.get_image(263,629,16,22),True,False)]

        #head
        self.head_kame_frames_r = [self.spritesheet.get_image(222,620,26,40)]
        self.head_kame_frames_l = [pygame.transform.flip(self.spritesheet.get_image(222,620,26,40),True,False)]

       
        

        
