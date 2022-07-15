import pygame
from scripts.spriteSheetClass import *
from scripts.settings import *
from scripts.hud import *
vec = pygame.math.Vector2

#Link Stats:
increment = 5
friccio = -0.5
gravetat = 1
jump = -19

class Link(pygame.sprite.Sprite):
    def __init__(self,game,pos, proj, all_sprites_group,muted):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.all_sprites_group = all_sprites_group
        self.current_frame = 0
        self.proj = proj
        self.last_update = 0 #permet editar el frame rate de la animacio
        self.spritesheet = Spritesheet('img/heroes/link_sprite.png')
        self.load_images()
        self.image = self.standing_frames_r[0]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(pos[0], pos[1])
        self.vel = vec(0, 0)
        self.acc = vec(0,0)
        self.jump_counter = 0
        self.jump_max_counter = 1
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
    
        self.basic1_push_x = 30
        self.basic1_push_y = 3
        self.basic2_push_x = 25
        self.basic2_push_y = 8
        self.especial_push_x = 0
        self.especial_push_y = 0
        
        
        self.basic1_damage = 4
        self.basic2_damage = 7
        self.especial_damage = 0 #si es cos a cos solament!
        
        self.max_health = 150
        self.max_cooldown_time = 7000 #15000
        
        
        self.time = pygame.time.get_ticks()

        self.death_sound = pygame.mixer.Sound("sounds/death_sound.ogg")
        self.life_sound = pygame.mixer.Sound("sounds/mushroom_sound.ogg")
        self.coin_sound = pygame.mixer.Sound("sounds/coin_sound.ogg")
        self.coin_sound.set_volume(0.5)

        self.jump_sound = pygame.mixer.Sound('sounds/jump2_sound.ogg')
        self.jump_sound.set_volume(0.25)
        
        if muted:
            self.death_sound.set_volume(0)
            self.life_sound.set_volume(0)
            self.coin_sound.set_volume(0)
            self.jump_sound.set_volume(0)
        
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
                if hits2 and hits:
                    self.airborne = False
                    
        hits3 = pygame.sprite.spritecollide(self, self.oponent.proj, False)
        for projectil in hits3:
            self.take_damage(projectil.damage)#POSAR DAMAGE AL PROJECTIL
            
            if self.rect.centerx - hits3[0].rect.centerx < 0: 
                self.pos.x -= 50
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
            #EXCEPCIO PELS QUE TENEN ESPECIAL COS A COS
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
        if pygame.time.get_ticks() - self.last_update > 80:#50
            self.last_update = pygame.time.get_ticks()
            self.current_frame = (self.current_frame +1) % len(self.basic1_frames_r)
            if self.current_frame == 0:
                self.basic1_state = False
                self.atacant = False
                if len(self.proj) < 1:
                    a = Arrow(self.pos.x, self.pos.y - 15, self, self.game.platforms, self.game.stadium)                   
                    self.proj.add(a)
                    self.all_sprites_group.add(a)
                
            if self.faceright:
                self.image = self.basic1_frames_r[self.current_frame]
            else:
                self.image = self.basic1_frames_l[self.current_frame]
            self.rect = self.image.get_rect()
            
            
    def basic2_select_image(self):
        if pygame.time.get_ticks() - self.last_update > 65:
            self.last_update = pygame.time.get_ticks()
            self.current_frame = (self.current_frame +1) % len(self.basic2_frames_r)
            if self.current_frame == 0:
                self.basic2_state = False
                self.atacant = False
            if self.faceright:
                self.image = self.basic2_frames_r[self.current_frame]
            else:
                self.image = self.basic2_frames_l[self.current_frame]
            self.rect = self.image.get_rect()
            

    def especial_select_image(self):
        if pygame.time.get_ticks() - self.last_update > 80:#50
            self.last_update = pygame.time.get_ticks()
            self.current_frame = (self.current_frame +1) % len(self.especial_frames_r)
            if self.current_frame == 0:
                
                for plat in self.game.platforms:
                    if abs(plat.rect.y - self.pos.y) > 100:
                        self.pos.y = plat.rect.top - 50
                        self.pos.x = plat.rect.centerx
                
                self.especial_state = False
                
            if self.faceright:
                self.image = self.especial_frames_r[self.current_frame]
            else:
                self.image = self.especial_frames_l[self.current_frame]
            self.rect = self.image.get_rect()
                        
    def load_images(self):
        #STANDING
        self.standing_frames_r = [self.spritesheet.get_image(273,134,316-273,185-134),
                                  self.spritesheet.get_image(273,134,316-273,185-134)]
        
        self.standing_frames_l = [self.spritesheet.get_image(35,130,80-35,187-130),
                                  self.spritesheet.get_image(35,130,80-35,187-130)]

        #WALKING
        self.walking_frames_r = [self.spritesheet.get_image(16,289,71-16,329-289),
                                self.spritesheet.get_image(76,288,127-76,334-288),
                                 self.spritesheet.get_image(136,290,179-136,334-290),
                                 self.spritesheet.get_image(190,290,233-190,334-290),
                                 self.spritesheet.get_image(238,292,293-238,333-292),
                                 self.spritesheet.get_image(299,292,350-299,338-292),
                                 self.spritesheet.get_image(358,294,403-358,338-294),
                                 self.spritesheet.get_image(413,294,456-413,338-294)]
        self.walking_frames_l = []

        for frame in self.walking_frames_r:
            self.walking_frames_l.append(pygame.transform.flip(frame,True,False))

        #JUMPING
        self.jumping_frames_r = [self.spritesheet.get_image(30,500,68-30,558-500)]
        self.jumping_frames_l = [self.spritesheet.get_image(35,593,90-35,651-593)]

       
        #BASIC1
        self.basic1_frames_r = [self.spritesheet.get_image(349,38,390-349,92-38),
                                self.spritesheet.get_image(38,38,84-38,92-38),
                                  self.spritesheet.get_image(90,38,141-90,92-38),
                                  self.spritesheet.get_image(147,36,206-147,92-36),
                                  self.spritesheet.get_image(211,32,271-211,92-32),
                                  self.spritesheet.get_image(349,38,390-349,92-38)
                                  ]
                                  
        self.basic1_frames_l = []

        for frame in self.basic1_frames_r:
            self.basic1_frames_l.append(pygame.transform.flip(frame,True,False))
            
        #BASIC2
        self.basic2_frames_r = [self.spritesheet.get_image(19,214,80-19,267-214),
                                self.spritesheet.get_image(84,215,138-84,266-215),
                                self.spritesheet.get_image(154,215,196-154,266-215),
                                self.spritesheet.get_image(201,215,259-201,266-215),
                                self.spritesheet.get_image(264,215,315-264,266-214),
                                self.spritesheet.get_image(324,215,383-324,266-215),
                                self.spritesheet.get_image(389,215,445-389,266-215),
                                self.spritesheet.get_image(450,215,513-450,266-215),
                                self.spritesheet.get_image(514,215,572-514,266-215),
                                self.spritesheet.get_image(579,215,639-579,266-215),
                                self.spritesheet.get_image(646,215,714-646,266-215)]
                                  
        self.basic2_frames_l = []

        for frame in self.basic2_frames_r:
            self.basic2_frames_l.append(pygame.transform.flip(frame,True,False))

        #ESPECIAL
        
        self.especial_frames_r = [self.spritesheet.get_image(377,392,416-377,424-392),
                                self.spritesheet.get_image(377,392,416-377,424-392),
                              self.spritesheet.get_image(421,380,465-421,434-380),
                              self.spritesheet.get_image(363,427,404-363,466-427),
                              self.spritesheet.get_image(407,442,438-349,467-442)]
        '''
self.spritesheet.get_image(65,383,106-65,446-383),
                                self.spritesheet.get_image(118,375,153-118,448-375),
                                self.spritesheet.get_image(166,396,198-166,448-396),
                                self.spritesheet.get_image(211,395,249-211,446-395),
                                self.spritesheet.get_image(274,422,299-274,454-422),
                              self.spritesheet.get_image(345,38,373-345,92-38),
                              '''
                                  
        self.especial_frames_l = []

        for frame in self.especial_frames_r:
            self.especial_frames_l.append(pygame.transform.flip(frame,True,False))

        
class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y, owner, plat, stadi):
        pygame.sprite.Sprite.__init__(self)
        self.spritesheet = Spritesheet('img/heroes/link_sprite.png')
        self.load_images()
        self.x = x
        self.damage = 3
        self.max_distance = 200
        self.owner = owner
        if self.owner.faceright:
            self.image = self.arrow_frames_r[0]
            self.vel = 4
        else:
            self.image = self.arrow_frames_l[0]
            self.vel = -4
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y - 20
        self.low_tier = True
        self.last_update = pygame.time.get_ticks()
        self.current_frame = 0
        self.plat = plat
        self.on_plat = pygame.sprite.spritecollide(self, self.plat, False)
        self.on_air = self.owner.airborne
        self.right = self.owner.faceright
        self.stadi = stadi
        self.on_stadi = pygame.sprite.collide_rect(self, self.stadi)
        
    def update(self):
        self.select_image()
        self.rect.x += self.vel
        if self.on_air:
            self.rect.y+= 1
        if self.on_plat and not self.on_stadi:
            self.rect.y+= 1
        if abs(self.rect.x - self.x) > self.max_distance:
            self.kill()
        if self.rect.left < 40:
            self.kill()

    def select_image(self):
        if pygame.time.get_ticks() - self.last_update > 80:#50
            self.last_update = pygame.time.get_ticks()
            self.current_frame = (self.current_frame +1) % len(self.arrow_frames_r)
            if self.right:
                self.image = self.arrow_frames_r[self.current_frame]
            else:
                self.image = self.arrow_frames_l[self.current_frame]
        
                
            
    def load_images(self):
        self.arrow_frames_r = [self.spritesheet.get_image(397,63,443-397,89-63),
                               self.spritesheet.get_image(445,62,504-445,90-62),
                               self.spritesheet.get_image(508,66,549-508,87-66),
                               self.spritesheet.get_image(552,62,611-552,89-62),
                               self.spritesheet.get_image(617,65,662-617,88-65),
                               self.spritesheet.get_image(665,63,722-665,90-63),
                               self.spritesheet.get_image(728,66,766-728,86-66)]
        self.arrow_frames_l = []

        for frame in self.arrow_frames_r:
            self.arrow_frames_l.append(pygame.transform.flip(frame,True,False))

        '''
        self.impact_frames = [self.spritesheet.get_image(478,364,508-478,375-364),
                               self.spritesheet.get_image(515,310,607-515,415-310),
                               self.spritesheet.get_image(612,297,730-612,435-297)]
        '''
