import pygame
from pygame.locals import *
from pgu import engine
from os import path
from random import randrange



from scripts.settings import *
from scripts.hud import *
from scripts.spriteSheetClass import *
from scripts.marioClass import *
from scripts.sonicClass import *
from scripts.gokuClass import *
from scripts.kirbyClass import *
from scripts.linkClass import *
from scripts.platformClass import *

from scripts.single_mode_sprites import *


class Game(engine.Game):
    def __init__(self):
        super().__init__()
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT),SWSURFACE)
        pygame.display.set_caption(TITLE)
        self.crono = pygame.time.Clock()
        self._init_state_machine()
        self.font_name = pygame.font.match_font(FONT)
        self.muted = False
        self.click_sound = pygame.mixer.Sound("sounds/selection_click.ogg")
        
    def _init_state_machine(self):
        # All states must be initialized and stored as attributes
        self.menu_state = Menu(self)
        self.credits_state = Credits(self)
        self.single_menu_state = SingleMenu(self)
        self.historia0_state = Historia0(self)
        self.single_controls_state = SingleControls(self)
        self.single_mode_state = SingleMode(self)
        self.mult_mode_state = MultMode(self)
        self.mult_menu_state = MultMenu(self)
        self.selec_char_state = Selec_Char(self)
        self.hero_info_state = HeroInfo(self)
        self.mult_controls_state = MultControls(self)
        self.rules_state = Rules(self)
        self.player1_wins_state = Player1Wins(self)
        self.player2_wins_state = Player2Wins(self)
        self.pantalla_mort_state =PantallaMort(self)
        self.pantalla_final_state = PantallaFinal(self)
        self.quit_state = engine.Quit(self)

        #diapositives historia
        self.historia1_state = Historia1(self)
        self.historia2_state = Historia2(self)
        self.historia3_state = Historia3(self)
        

    def run(self): 
        super().run(self.menu_state, self.screen)
    
    def change_state(self, transition=None):
        if self.state is self.menu_state:
            if transition == 'MULT MENU':
                new_state = self.mult_menu_state
            elif transition == 'CREDITS':
                new_state = self.credits_state
            elif transition == 'SINGLE MENU':
                new_state = self.single_menu_state
            elif transition == 'QUIT':
                new_state = self.quit_state
                
        if self.state is self.single_menu_state:
            if transition == 'MENU':
                new_state = self.menu_state
            elif transition == 'HISTORIA 0':
                new_state = self.historia0_state
                new_state.init()
            elif transition == 'SINGLE MODE':
                new_state = self.single_mode_state
                new_state.init()
            elif transition == 'SINGLE CONTROLS':
                new_state = self.single_controls_state
                
        if self.state is self.historia0_state:
            if transition == 'SINGLE MENU':
                new_state = self.single_menu_state
            elif transition == 'HISTORIA 1':
                new_state = self.historia1_state
        if self.state is self.historia1_state:
            if transition == 'HISTORIA 0':
                new_state = self.historia0_state
            elif transition == 'HISTORIA 2':
                new_state = self.historia2_state
        if self.state is self.historia2_state:
            if transition == 'HISTORIA 1':
                new_state = self.historia1_state
            elif transition == 'HISTORIA 3':
                new_state = self.historia3_state
        if self.state is self.historia3_state:
            if transition == 'HISTORIA 2':
                new_state = self.historia2_state
            elif transition == 'MENU':
                new_state = self.menu_state
                new_state.init()
                
        if self.state is self.single_mode_state:
            if transition == 'MENU':
                new_state = self.menu_state
                new_state.init()
            elif transition == 'FIN':
                new_state = self.pantalla_final_state
            elif transition == 'MORT':
                new_state = self.pantalla_mort_state
                
        if self.state is self.pantalla_final_state:
            if transition == 'MENU':
                new_state = self.menu_state
                new_state.init()
        if self.state is self.pantalla_mort_state:
            if transition == 'MENU':
                new_state = self.menu_state
                new_state.init()               
                
                
        if self.state is self.single_controls_state:
            if transition == 'SINGLE MENU':
                new_state = self.single_menu_state
                

        if self.state is self.credits_state:
            if transition == 'MENU':
                new_state = self.menu_state
            
        if self.state is self.mult_menu_state:
            if transition == 'SELECT CHAR MENU':
                new_state = self.selec_char_state
                new_state.init()
            elif transition == 'RULES':
                new_state = self.rules_state
            elif transition == 'MULT CONTROLS':
                new_state = self.mult_controls_state
            elif transition == 'MENU':
                new_state = self.menu_state
                        

        if self.state is self.mult_controls_state:
            if transition == 'MULT MENU':
                new_state = self.mult_menu_state

        if self.state is self.rules_state:
            if transition == 'MULT MENU':
                new_state = self.mult_menu_state
                       
        if self.state is self.selec_char_state:
            if transition == 'PLAY':
                pygame.mixer.music.fadeout(500)
                new_state = self.mult_mode_state
                new_state.init()
            elif transition == 'HERO INFO':
                new_state =  self.hero_info_state
                new_state.init()
            elif transition == 'MULT MENU':
                new_state = self.mult_menu_state
                
        if self.state is self.hero_info_state:
            if transition == 'SELECT CHAR MENU':
                new_state = self.selec_char_state
                
        if self.state is self.mult_mode_state:
            if transition == 'MENU':
                new_state = self.menu_state
                new_state.init()
            elif transition == 'PLAYER 1 WINS':
                new_state = self.player1_wins_state
            elif transition == 'PLAYER 2 WINS':
                new_state = self.player2_wins_state
                        
        if self.state is self.player1_wins_state:
            if transition == 'MENU':
                new_state = self.menu_state
                new_state.init()
            elif transition == 'SELECT CHAR MENU':
                
                new_state = self.selec_char_state
        if self.state is self.player2_wins_state:
            if transition == 'MENU':
                new_state = self.menu_state
                new_state.init()
            elif transition == 'SELECT CHAR MENU':
                new_state = self.selec_char_state
        return new_state
   
    def tick(self):
        self.crono.tick(60)   # Limits the maximum FPS

class Menu(engine.State):
    def init(self):
        self.image = pygame.image.load("img/menus/main_menu.png")
        pygame.mixer.music.load('sounds/ow.ogg')
        
        if self.game.muted:
            pygame.mixer.music.set_volume(0)
            self.game.click_sound.set_volume(0)
        else:
            self.game.click_sound.set_volume(1)
            pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(loops=-1)
        self.micro = Micro(770, 800)
    
    def update(self, s):
        s.fill(WHITE)
        rect = self.image.get_rect()
        rect.center = s.get_rect().center
        s.blit(self.image, rect)
        s.blit(self.micro.image, self.micro.rect)
        pygame.display.flip()

    def event(self,e): 
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_x:
                if self.game.muted:
                    self.game.muted = False
                else:
                    self.game.muted = True
            if e.key == pygame.K_c:
                self.game.click_sound.play()
                return self.game.change_state('CREDITS')
            if e.key == pygame.K_s:
                self.game.click_sound.play()
                return self.game.change_state('SINGLE MENU')
            if e.key == pygame.K_m:
                self.game.click_sound.play()
                return self.game.change_state('MULT MENU')
            if e.key == pygame.K_ESCAPE:
                self.game.click_sound.play()
                return self.game.change_state('QUIT')
    def loop(self):
        self.micro.update(self.game.muted)
        if not self.game.muted:
            pygame.mixer.music.set_volume(0.5)
            self.game.click_sound.set_volume(1)
        else:
            pygame.mixer.music.set_volume(0)
            self.game.click_sound.set_volume(0)

class SingleMenu(engine.State):
    def init(self):
        self.image = pygame.image.load("img/menus/single_menu.png")
    
    def paint(self, s):
        s.fill(WHITE)
        rect = self.image.get_rect()
        rect.center = s.get_rect().center
        s.blit(self.image, rect)
        pygame.display.flip()
        
    def event(self,e): 
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_n:
                self.game.click_sound.play()
                pygame.mixer.music.fadeout(500)
                return self.game.change_state('SINGLE MODE')
            if e.key == K_h:
                self.game.click_sound.play()
                pygame.mixer.music.fadeout(500)
                return self.game.change_state('HISTORIA 0')
            if e.key == K_c:
                self.game.click_sound.play()
                return self.game.change_state('SINGLE CONTROLS')
            if e.key == K_ESCAPE:
                self.game.click_sound.play()
                return self.game.change_state('MENU')
            
class SingleControls(engine.State):
    def init(self):
        self.image = pygame.image.load("img/menus/single_controls.png")
    
    def paint(self, s):
        s.fill(WHITE)
        rect = self.image.get_rect()
        rect.center = s.get_rect().center
        s.blit(self.image, rect)
        pygame.display.flip()
        
    def event(self,e): 
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                self.game.click_sound.play()
                return self.game.change_state('SINGLE MENU')

class Historia0(engine.State):
    def init(self):
        pygame.mixer.music.load('sounds/halo.ogg')
        if self.game.muted:
            pygame.mixer.music.set_volume(0)
            self.game.click_sound.set_volume(0)
        else:
            self.game.click_sound.set_volume(1)
            #pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(loops=-1)
        self.image = pygame.image.load("img/menus/historia0.png")
    
    def paint(self, s):
        s.fill(WHITE)
        rect = self.image.get_rect()
        rect.center = s.get_rect().center
        s.blit(self.image, rect)
        pygame.display.flip()
        
    def event(self,e): 
        if e.type is KEYDOWN:
            if e.key == K_ESCAPE:
                self.game.click_sound.play()
                return self.game.change_state('SINGLE MENU')
            if e.key == K_RETURN:
                self.game.click_sound.play()
                return self.game.change_state('HISTORIA 1')
            
class Historia1(engine.State):
    def init(self):
        self.image = pygame.image.load("img/menus/historia1.png")
    
    def paint(self, s):
        s.fill(WHITE)
        rect = self.image.get_rect()
        rect.center = s.get_rect().center
        s.blit(self.image, rect)
        pygame.display.flip()
        
    def event(self,e): 
        if e.type is KEYDOWN:
            if e.key == K_ESCAPE:
                self.game.click_sound.play()
                return self.game.change_state('HISTORIA 0')
            if e.key == K_RETURN:
                self.game.click_sound.play()
                return self.game.change_state('HISTORIA 2')
            
class Historia2(engine.State):
    def init(self):
        self.image = pygame.image.load("img/menus/historia2.png")
    
    def paint(self, s):
        s.fill(WHITE)
        rect = self.image.get_rect()
        rect.center = s.get_rect().center
        s.blit(self.image, rect)
        pygame.display.flip()
        
    def event(self,e): 
        if e.type is KEYDOWN:
            if e.key == K_ESCAPE:
                self.game.click_sound.play()
                return self.game.change_state('HISTORIA 1')
            if e.key == K_RETURN:
                self.game.click_sound.play()
                return self.game.change_state('HISTORIA 3')
            
class Historia3(engine.State):
    def init(self):
        self.image = pygame.image.load("img/menus/historia3.png")
    
    def paint(self, s):
        s.fill(WHITE)
        rect = self.image.get_rect()
        rect.center = s.get_rect().center
        s.blit(self.image, rect)
        pygame.display.flip()
        
    def event(self,e): 
        if e.type is KEYDOWN:
            if e.key == K_ESCAPE:
                self.game.click_sound.play()
                return self.game.change_state('HISTORIA 2')
            if e.key == K_RETURN:
                self.game.click_sound.play()
                pygame.mixer.music.fadeout(500)
                return self.game.change_state('MENU')

class PantallaFinal(engine.State):
    def init(self):
        self.image = pygame.image.load("img/menus/final_ind.png")
    
    def paint(self, s):
        s.fill(WHITE)
        rect = self.image.get_rect()
        rect.center = s.get_rect().center
        s.blit(self.image, rect)
        pygame.display.flip()
        
    def event(self,e): 
        if e.type is KEYDOWN:
            if e.key == K_RETURN:
                self.game.click_sound.play()
                
                return self.game.change_state('MENU')
class PantallaMort(engine.State):
    def init(self):
        self.image = pygame.image.load("img/menus/pantalla_de_mort_ind.png")
    
    def paint(self, s):
        s.fill(WHITE)
        rect = self.image.get_rect()
        rect.center = s.get_rect().center
        s.blit(self.image, rect)
        pygame.display.flip()
        
    def event(self,e): 
        if e.type is KEYDOWN:
            
            if e.key == K_RETURN:
                self.game.click_sound.play()
                
                return self.game.change_state('MENU')
       
            
            
  



##############################################################################################################
########################################################################
###################################




            
    
                      
class SingleMode(engine.State):
    def init(self):
        pygame.mixer.music.load('sounds/forward.ogg')
        
        if self.game.muted:
            pygame.mixer.music.set_volume(0)
            self.game.click_sound.set_volume(0)
        else:
            self.game.click_sound.set_volume(1)
            pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(loops=-1)
        
        # start a new game
        self.all_sprites = pygame.sprite.Group()
        self.projectils_player1_group = pygame.sprite.Group()
        self.ground = Ground(self,0,HEIGHT-50)
        self.all_sprites.add(self.ground)
        self.player = Single_Mario(self,(self.ground.rect.left + 100, self.ground.rect.top),self.projectils_player1_group,self.all_sprites,self.game.muted)
        self.player.cooldown = pygame.time.get_ticks()
        self.player.health = self.player.max_health
        self.player.life = 1
        self.player.lifebar = LifeBar(self,30,40, 150, 20, self.player.health)
        self.player.coolbar = CoolBar(self,30,70, 100, 10, self.player.max_cooldown_time)
        self.all_sprites.add(self.player)     
 
        #set course
        egg1 = GoldenEgg(2600,300)
        egg2 = GoldenEgg(5800,300)
        egg3 = GoldenEgg(7400,200)
        self.eggs = pygame.sprite.Group()
        self.eggs.add(egg1, egg2, egg3)
        self.max_eggs = 3 #ous maxims per acabar la partida
        self.minieggs = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.platmobils = pygame.sprite.Group()
        self.nuvols = pygame.sprite.Group()
        self.vortex = pygame.sprite.Group()
        vor = Vortex2 (9700,650)
        self.vortex.add(vor)
        self.all_sprites.add(vor)
        self.coins = pygame.sprite.Group()
        self.powers = pygame.sprite.Group()
         
 
        platform_list = [(500,700,0), #escala 1
                 (1000, 500, 3),
                 (1700, 200, 2),
                 (2300, 300, 2),
                 (3400, 600, 2),
                 (3400, 200, 0),
                 (4000, 500, 0),
                 (4500, 300, 3),
                 (5500, 300, 0),
                 (5500, 600, 0),
                 (6100, 500, 3),
                 (7000, 200, 2),
                 (7900,400,2),
                 (8400, 600, 2),
                 ]
 
        movplatform_list = [(1500, 400, 4, 300, 600,3),
                            (2900, 400, 3, 300, 600, 2),
                            (5000, 400, 4,200,600,3),
                            (5250,200,4, 200, 500, 2),
                            (6500, 200, 3, 200, 500, 3),
                            (7600, 200, 4, 200, 700, 3)
                            
                            ]
        nuvols_list = [(400, 200, 0), (100, 100, 2), (700, 250, 4),
                       (1400, 200, 5), (1700, 300, 2), (2100, 50, 0),
                       (2500, 100, 2), (3000, 100, 4),
                       (3400, 200, 5), (3700, 100, 2), (4100, 50, 0),
                       (4400, 200, 0), (5100, 100, 2),
                       (6100, 200, 5), (6700, 100, 2), (7100, 50, 0),
                       (7400, 200, 0), (8100, 100, 2), (8700, 250, 4),
                       (9400, 200, 5), (9700, 100, 2), (10100, 50, 0),
                       (11400, 200, 0), (12100, 100, 2), (15700, 250, 4)]
 
        coins_list = [(800,700), (5800,600), (8100, 400)]
 
        power_list = [(1550, 400), (3600, 180), (4550, 400)]
 
        for plat in platform_list:
            p = Single_Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        for plat in movplatform_list:
            p = Moving_Platform(*plat)
            self.all_sprites.add(p)
            self.platmobils.add(p)
        for nuvol in nuvols_list:
            n = Cloud2(*nuvol)
            self.all_sprites.add(n)
            self.nuvols.add(n)
        for coin in coins_list:
            c = Coin2(*coin)
            self.all_sprites.add(c)
            self.coins.add(c)
 
        for power in power_list:
            p = PowerUp2(*power)
            self.all_sprites.add(p)
            self.powers.add(p)
 
        
        self.enemics2 = pygame.sprite.Group()         
        self.s1 = Enemic2(self, (600,700),self.projectils_player1_group,self.player)
        self.enemics2.add(self.s1)
        self.all_sprites.add(self.s1)

        self.s2 = Enemic2(self, (3500,600),self.projectils_player1_group,self.player)
        self.enemics2.add(self.s2)
        self.all_sprites.add(self.s2)

        self.s3 = Enemic2(self, (7200,150),self.projectils_player1_group,self.player)
        self.enemics2.add(self.s3)
        self.all_sprites.add(self.s3)

        self.s4 = Enemic2(self, (5700,250),self.projectils_player1_group,self.player)
        self.enemics2.add(self.s4)
        self.all_sprites.add(self.s4)

        self.s5 = Enemic2(self, (8700,550),self.projectils_player1_group,self.player)
        self.enemics2.add(self.s5)
        self.all_sprites.add(self.s5)

        self.enemics1 = pygame.sprite.Group()
        e = Enemic1(self,list(self.platforms)[1].rect.left,list(self.platforms)[1].rect.top,list(self.platforms)[1],self.player)
        e1 = Enemic1(self,list(self.platforms)[1].rect.right,list(self.platforms)[1].rect.top,list(self.platforms)[1],self.player)
        e1.vel = -1
        
        e3 = Enemic1(self,list(self.platforms)[3].rect.left,list(self.platforms)[3].rect.top,list(self.platforms)[3],self.player)
        
        self.enemics1.add(e,e1,e3)
        self.all_sprites.add(e,e1,e3)

        arbustos = [(300,850),(400,850),(500,850),
                    (900,self.ground.rect.top),(1000,self.ground.rect.top),(1300,self.ground.rect.top),
                    (2400,self.ground.rect.top),(2700,self.ground.rect.top),(2800,self.ground.rect.top),
                    (4300,self.ground.rect.top),(4600,self.ground.rect.top),(4700,self.ground.rect.top),
                    (6200,self.ground.rect.top),(6700,self.ground.rect.top),(7400,self.ground.rect.top),
                    (8300,self.ground.rect.top),(8600,self.ground.rect.top),(9100,self.ground.rect.top)]
        blocs_1 = [(0,850),(2000,850),(3900,self.ground.rect.top),
                    (5400,self.ground.rect.top),(7700,self.ground.rect.top),(10000,self.ground.rect.top)]
        for ar in arbustos:
            a = Arbust1(*ar)
            self.nuvols.add(a)
            self.all_sprites.add(a)
        for bl in blocs_1:
            b = Bloc1(*bl)
            self.nuvols.add(b)
            self.all_sprites.add(b)

        self.limits = pygame.sprite.Group()
        self.limit_esquerre = Limit(-600,850,'ESQUERRE')
        self.limit_dret = Limit(10300,850,'DRET')
        self.limits.add(self.limit_esquerre,self.limit_dret)
        self.all_sprites.add(self.limit_esquerre,self.limit_dret)
        
         
         
 
    def event(self,e):
        if e.type == pygame.KEYDOWN:
            #atacs
            if e.key == pygame.K_f:
                self.player.basic1_state = True
                if not self.player.airborne:
                    self.player.walking_state = False
            if e.key == pygame.K_g:
                self.player.basic2_state = True
                if not self.player.airborne:
                    self.player.walking_state = False
            if e.key == pygame.K_h:
                self.player.try_especial_state = True
             
            #salt   
            if e.key == pygame.K_w:
                if self.player.jump_counter < self.player.jump_max_counter:
                    self.player.jumping_state = True
                    self.player.airborne = True
                     
            #moviment:
            if e.key == pygame.K_a:
                self.player.walking_state = True
                if self.player.basic1_state:
                    self.player.basic1_state = False
                if self.player.basic2_state:
                    self.player.basic2_state = False
                self.player.go_left=True
 
            if e.key == pygame.K_d:
                self.player.walking_state = True
                if self.player.basic1_state:
                    self.player.basic1_state = False
                if self.player.basic2_state:
                    self.player.basic2_state = False
                self.player.go_right=True
 
            if e.key == pygame.K_s:
                self.player.down_state = True
            
            #transició pgu
            if e.key == pygame.K_ESCAPE:
                return self.game.change_state('MENU')
             
        if e.type == pygame.KEYUP:
            #atacs
            if e.key == pygame.K_f:
                self.player.basic1_state = False
                                    
            if e.key == pygame.K_g:
                self.player.basic2_state = False
 
            if e.key == pygame.K_h:
                self.player.try_especial_state = False
             
 
            #moviment              
            if e.key ==pygame.K_a:
                self.player.walking_state = False
                self.player.go_left=False
 
            if e.key == pygame.K_d:
                self.player.walking_state = False
                self.player.go_right=False
            
            if e.key == pygame.K_s:
                self.player.down_state = False
 
            #salt   
            if e.key == pygame.K_w:
                self.player.jumping_state = False

            
    def loop(self):        
        self.all_sprites.update()
        self.update(self.game.screen)
        if self.player.end_game:
            pygame.mixer.music.fadeout(500)
            return self.game.change_state('FIN')
            
                         
        #end match
        if self.player.life <= 0:
            pygame.mixer.music.fadeout(500)
            return self.game.change_state('MORT')
                     
    def update(self,screen):
        pygame.display.set_caption("{:0.2f}".format(self.game.crono.get_fps()))#per veure si hi ha lagg
        screen.fill((153, 204, 255))
        self.all_sprites.draw(screen)
        screen.blit(self.ground.image, self.ground.rect)
        self.projectils_player1_group.draw(screen)
        self.eggs.draw(screen)
        if self.s1 in self.enemics2:
            screen.blit(self.s1.healthbar.image,self.s1.healthbar.rect)
        if self.s2 in self.enemics2:
            screen.blit(self.s2.healthbar.image,self.s2.healthbar.rect)
        if self.s3 in self.enemics2:
            screen.blit(self.s3.healthbar.image,self.s3.healthbar.rect)
        if self.s4 in self.enemics2:
            screen.blit(self.s4.healthbar.image,self.s4.healthbar.rect)
        if self.s5 in self.enemics2:
            screen.blit(self.s5.healthbar.image,self.s5.healthbar.rect)
        
        screen.blit(self.player.lifebar.image, self.player.lifebar.rect)
        screen.blit(self.player.coolbar.image, self.player.coolbar.rect)
        screen.blit(self.player.image, self.player.rect)
        screen.blit(self.player.lifebar.image, self.player.lifebar.rect)
        
        pygame.display.flip()
 

############################################################
#############################################################################################
################################################################################################################################







        
            
class Credits(engine.State):
    def init(self):
        self.image = pygame.image.load("img/menus/credits.png")
    
    def paint(self, s):
        s.fill(WHITE)
        rect = self.image.get_rect()
        rect.center = s.get_rect().center
        s.blit(self.image, rect)
        pygame.display.flip()
        
    def event(self,e): 
        if e.type is KEYDOWN:
            if e.key == K_ESCAPE:
                self.game.click_sound.play()
                return self.game.change_state('MENU')

class MultMenu(engine.State):
    def init(self):
        self.image = pygame.image.load("img/menus/mult_menu.png")
    
    def paint(self, s):
        s.fill(WHITE)
        rect = self.image.get_rect()
        rect.center = s.get_rect().center
        s.blit(self.image, rect)
        pygame.display.flip()
        
    def event(self,e): 
        if e.type is KEYDOWN:
            if e.key == K_n:
                self.game.click_sound.play()
                return self.game.change_state('SELECT CHAR MENU')
            if e.key == K_r:
                self.game.click_sound.play()
                return self.game.change_state('RULES')
            if e.key == K_c:
                self.game.click_sound.play()
                return self.game.change_state('MULT CONTROLS')
            if e.key == K_ESCAPE:
                self.game.click_sound.play()
                return self.game.change_state('MENU')
            if e.key == K_s:
                self.game.click_sound.play()
                return self.game.change_state('SINGLE')

class MultControls(engine.State):
    def init(self):
        self.image = pygame.image.load("img/menus/mult_controls.png")
    
    def paint(self, s):
        s.fill(WHITE)
        rect = self.image.get_rect()
        rect.center = s.get_rect().center
        s.blit(self.image, rect)
        pygame.display.flip()
        
    def event(self,e): 
        if e.type is KEYDOWN:
            if e.key == K_ESCAPE:
                self.game.click_sound.play()
                return self.game.change_state('MULT MENU')

class Rules(engine.State):
    def init(self):
        self.image = pygame.image.load("img/menus/rules.png")
    
    def paint(self, s):
        s.fill(WHITE)
        rect = self.image.get_rect()
        rect.center = s.get_rect().center
        s.blit(self.image, rect)
        pygame.display.flip()
        
    def event(self,e): 
        if e.type is KEYDOWN:
            if e.key == K_ESCAPE:
                self.game.click_sound.play()
                return self.game.change_state('MULT MENU')

class Selec_Char(engine.State):
    def init(self):
        self.image = pygame.image.load("img/menus/select_char_menu.png")
        self.game.player1_selec = ''
        self.game.player2_selec = ''
        self.game.hero_info = ''
        self.rodona_player = Rodona_1()
        self.rodona_enemy = Rodona_2()
        
            
    def update(self, s):
        s.fill(WHITE)
        rect = self.image.get_rect()
        rect.center = s.get_rect().center
        s.blit(self.image, rect)
        s.blit(self.rodona_player.image, self.rodona_player.rect)
        s.blit(self.rodona_enemy.image, self.rodona_enemy.rect)
        pygame.display.flip()

    def loop(self):
        self.rodona_player.update(self.game.player1_selec)
        self.rodona_enemy.update(self.game.player2_selec)

    def event(self,e): 
        if e.type is KEYDOWN:
            if e.key == K_1:
                self.game.player1_selec = 'Mario'
            if e.key == K_2:
                self.game.player1_selec = 'Sonic'
            if e.key == K_3:
                self.game.player1_selec = 'Goku'
            if e.key == K_4:
                self.game.player1_selec = 'Kirby'
            if e.key == K_6:
                self.game.player1_selec = 'Link'            
            if e.key == K_7:
                self.game.player1_selec = 'Random'
            
            if e.key == K_q:
                self.game.player2_selec ='Mario'
            if e.key == K_w:
                self.game.player2_selec = 'Sonic'
            if e.key == K_e:
                self.game.player2_selec = 'Goku'
            if e.key == K_r:
                self.game.player2_selec = 'Kirby'
            if e.key == K_y:
                self.game.player2_selec = 'Link'
            if e.key == K_u:
                self.game.player2_selec = 'Random'
            
            
            if e.key == K_RETURN:
                if self.game.player1_selec != '' and self.game.player2_selec != '':
                    return self.game.change_state('PLAY')
            if e.key == K_ESCAPE:
                self.game.click_sound.play()
                return self.game.change_state('MULT MENU')
            
        if e.type == MOUSEBUTTONDOWN:
            self.mousex,self.mousey = pygame.mouse.get_pos()
            if 46 < self.mousex < 75 and 122 < self.mousey < 153:
                self.game.hero_info = 'Mario Info'
                return self.game.change_state('HERO INFO')
            if 248 < self.mousex < 277 and 127 < self.mousey < 157:
                self.game.hero_info = 'Sonic Info'
                return self.game.change_state('HERO INFO')
            if 463 < self.mousex < 491 and 121 < self.mousey < 151:
                self.game.hero_info = 'Goku Info'
                return self.game.change_state('HERO INFO')
            if 675 < self.mousex < 704 and 128 < self.mousey < 158:
                self.game.hero_info = 'Kirby Info'
                return self.game.change_state('HERO INFO')
            if 249 < self.mousex < 277 and 436 < self.mousey < 465:
                self.game.hero_info = 'Link Info'
                return self.game.change_state('HERO INFO')
            

class HeroInfo(engine.State):
    def init(self):
        if self.game.hero_info == 'Mario Info':
            self.image = pygame.image.load("img/menus/mario_info.png")
        if self.game.hero_info == 'Sonic Info':
            self.image = pygame.image.load("img/menus/sonic_info.png")
        if self.game.hero_info == 'Goku Info':
            self.image = pygame.image.load("img/menus/goku_info.png")
        if self.game.hero_info == 'Kirby Info':
            self.image = pygame.image.load("img/menus/kirby_info.png")
        if self.game.hero_info == 'Link Info':
            self.image = pygame.image.load("img/menus/link_info.png")
        
    
    def paint(self, s):
        s.fill(WHITE)
        rect = self.image.get_rect()
        rect.center = s.get_rect().center
        s.blit(self.image, rect)
        pygame.display.flip()
        
    def event(self,e): 
        if e.type is KEYDOWN:
            if e.key == K_ESCAPE:
                return self.game.change_state('SELECT CHAR MENU')
class MultMode(engine.State):  
    def init(self):
        # start a new game
        self.all_sprites = pygame.sprite.Group()
        self.platforms = Sequenciador()
        self.clouds = CloudGenerator()
        self.clouds.group = self.clouds
        self.power_up = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.platforms.coins = self.coins
        self.platforms.life_gr = self.power_up
        self.projectils_player1_group = pygame.sprite.Group()
        self.projectils_enemy_group = pygame.sprite.Group()
        self.tags_group = pygame.sprite.Group()
        #self.arena_spritesheet = Spritesheet('img/assets/arena.png')
        self.pipe = Pipe(self,WIDTH/2, 0)
        #self.pipe = Vortex(self,WIDTH/2,80)
        self.stadium = Stadium(self,WIDTH*0.5-278, HEIGHT-201)
        self.stadiums = pygame.sprite.Group()
        self.stadiums.add(self.stadium)
        self.all_sprites.add(self.stadium,self.pipe)
        if self.game.player1_selec == 'Mario':
            self.player = Mario(self,(self.stadium.rect.left + 100, self.stadium.rect.top),self.projectils_player1_group,self.all_sprites,self.game.muted)
        if self.game.player1_selec == 'Sonic':
            self.player = Sonic(self,(self.stadium.rect.left + 100, self.stadium.rect.top),self.projectils_player1_group,self.all_sprites,self.game.muted)
        if self.game.player1_selec == 'Goku':
            self.player = Goku(self,(self.stadium.rect.left + 100, self.stadium.rect.top),self.projectils_player1_group,self.all_sprites,self.game.muted)
        if self.game.player1_selec == 'Kirby':
            self.player = Kirby(self,(self.stadium.rect.left + 100, self.stadium.rect.top),self.projectils_player1_group,self.all_sprites,self.game.muted)
        if self.game.player1_selec == 'Link':
            self.player = Link(self,(self.stadium.rect.left + 100, self.stadium.rect.top),self.projectils_player1_group,self.all_sprites,self.game.muted)
        if self.game.player1_selec == 'Random':
            n = randint(0,4)
            if n == 0: self.player = Mario(self,(self.stadium.rect.left + 100, self.stadium.rect.top),self.projectils_player1_group,self.all_sprites,self.game.muted)
            if n == 1: self.player = Sonic(self,(self.stadium.rect.left + 100, self.stadium.rect.top),self.projectils_player1_group,self.all_sprites,self.game.muted)
            if n == 2: self.player = Goku(self,(self.stadium.rect.left + 100, self.stadium.rect.top),self.projectils_player1_group,self.all_sprites,self.game.muted)
            if n == 3: self.player = Kirby(self,(self.stadium.rect.left + 100, self.stadium.rect.top),self.projectils_player1_group,self.all_sprites,self.game.muted)
            if n == 4: self.player = Link(self,(self.stadium.rect.left + 100, self.stadium.rect.top),self.projectils_player1_group,self.all_sprites,self.game.muted)
                
        
        if self.game.player2_selec == 'Mario':
            self.enemy = Mario(self,(self.stadium.rect.right -100,self.stadium.rect.top+30),self.projectils_enemy_group,self.all_sprites, self.game.muted)
        if self.game.player2_selec == 'Sonic':
            self.enemy = Sonic(self,(self.stadium.rect.right -100,self.stadium.rect.top+30),self.projectils_enemy_group,self.all_sprites,self.game.muted)
        if self.game.player2_selec == 'Goku':
            self.enemy = Goku(self,(self.stadium.rect.right -100,self.stadium.rect.top+30),self.projectils_enemy_group,self.all_sprites,self.game.muted)
        if self.game.player2_selec == 'Kirby':
            self.enemy = Kirby(self,(self.stadium.rect.right -100,self.stadium.rect.top+30),self.projectils_enemy_group,self.all_sprites,self.game.muted)
        if self.game.player2_selec == 'Link':
            self.enemy = Link(self,(self.stadium.rect.right -100,self.stadium.rect.top+30),self.projectils_enemy_group,self.all_sprites,self.game.muted)
        if self.game.player2_selec == 'Random':
            n = randint(0,4)
            if n == 0: self.enemy = Mario(self,(self.stadium.rect.right -100,self.stadium.rect.top+30),self.projectils_enemy_group,self.all_sprites, self.game.muted)
            if n == 1: self.enemy = Sonic(self,(self.stadium.rect.right -100,self.stadium.rect.top+30),self.projectils_enemy_group,self.all_sprites, self.game.muted)
            if n == 2: self.enemy = Goku(self,(self.stadium.rect.right -100,self.stadium.rect.top+30),self.projectils_enemy_group,self.all_sprites, self.game.muted)
            if n == 3: self.enemy = Kirby(self,(self.stadium.rect.right -100,self.stadium.rect.top+30),self.projectils_enemy_group,self.all_sprites, self.game.muted)
            if n == 4: self.enemy = Link(self,(self.stadium.rect.right -100,self.stadium.rect.top+30),self.projectils_enemy_group,self.all_sprites, self.game.muted)
        
            
        self.player.oponent = self.enemy
        self.enemy.oponent = self.player
        self.player.tag = Tag('blue')
        self.enemy.tag = Tag('orange')
        self.tags_group.add(self.player.tag, self.enemy.tag)
        self.all_sprites.add(self.player, self.enemy)

        self.player.life_gr = self.power_up
        self.player.coins = self.coins
        self.enemy.coins = self.coins
        self.enemy.life_gr = self.power_up

        self.enemy.faceright = False

        if not self.game.muted:
            pygame.mixer.music.load('sounds/SSB.ogg')
            pygame.mixer.music.set_volume(0.05)
            pygame.mixer.music.play(loops=-1)
       
        self.t_ultima_pedra = pygame.time.get_ticks()
        self.enemy.cooldown = pygame.time.get_ticks()
        self.player.cooldown = pygame.time.get_ticks()

        self.player.health = self.player.max_health
        self.player.life = 3 
        self.enemy.health = self.enemy.max_health
        self.enemy.life = 3

        self.player.lifebar = LifeBar(self,30,HEIGHT - 30, 150, 20, self.player.health)
        self.enemy.lifebar = LifeBar(self,WIDTH-180,HEIGHT - 30, 150, 20, self.enemy.health)
    
        self.player.coolbar = CoolBar(self,30,HEIGHT - 5, 100, 10, self.player.max_cooldown_time)
        self.enemy.coolbar = CoolBar(self,WIDTH-180,HEIGHT - 5, 100, 10, self.enemy.max_cooldown_time)

    def event(self,e):
        if e.type is KEYDOWN:
            #atacs dels jugadors
            if e.key == K_f:
                if not self.player.atacant:
                    self.player.atacant = True
                    self.player.basic1_state = True
                    self.player.current_frame = 0
                    if not self.player.airborne:#si vull poder atacar i mourem a la vegada enlairat
                        self.player.walking_state = False #si no vull atacar i mourem a la vegada
            if e.key == K_g:
                if not self.player.atacant:
                    self.player.atacant = True
                    self.player.basic2_state = True
                    self.player.current_frame = 0
                    if not self.player.airborne:
                        self.player.walking_state = False
            if e.key == K_h:
                self.player.try_especial_state = True
            if e.key == K_i:
                if not self.enemy.atacant:
                    self.enemy.atacant = True
                    self.enemy.basic1_state = True
                    self.enemy.current_frame = 0
                    if not self.enemy.airborne:
                        self.enemy.walking_state = False
            if e.key == K_o:
                if not self.enemy.atacant:
                    self.enemy.atacant = True
                    self.enemy.basic2_state = True
                    self.enemy.current_frame = 0
                    if not self.enemy.airborne:
                        self.enemy.walking_state = False
            if e.key == K_p:
                self.enemy.try_especial_state = True
            
            
            #salts del jugadors    
            if e.key == K_w:
                if not self.player.atacant:
                    if self.player.jump_counter < self.player.jump_max_counter:
                        self.player.jumping_state = True
                        self.player.airborne = True
            if e.key == K_UP:
                if not self.enemy.atacant:
                    if self.enemy.jump_counter < self.enemy.jump_max_counter:
                        self.enemy.jumping_state = True
                        self.airborne = True
                    
            #moviment dels jugadors:
            if e.key == K_a:
                if not self.player.atacant:
                    self.player.walking_state = True
                    if self.player.basic1_state:
                        self.player.basic1_state = False
                    if self.player.basic2_state:
                        self.player.basic2_state = False
                    self.player.go_left=True

            if e.key == K_d:
                if not self.player.atacant:
                    self.player.walking_state = True
                    if self.player.basic1_state:
                        self.player.basic1_state = False
                    if self.player.basic2_state:
                        self.player.basic2_state = False
                    self.player.go_right=True

            if e.key == K_s:
                if not self.player.atacant:
                    self.player.down_state = True

            if e.key == K_DOWN:
                if not self.enemy.atacant:
                    self.enemy.down_state = True

            if e.key == K_LEFT:
                if not self.enemy.atacant:
                    self.enemy.walking_state = True
                    if self.enemy.basic1_state:
                        self.enemy.basic1_state = False
                    if self.enemy.basic2_state:
                        self.enemy.basic2_state = False
                    self.enemy.go_left=True

            if e.key == K_RIGHT:
                if not self.enemy.atacant:
                    self.enemy.walking_state = True
                    if self.enemy.basic1_state:
                        self.enemy.basic1_state = False
                    if self.enemy.basic2_state:
                        self.enemy.basic2_state = False
                    self.enemy.go_right=True
                
            #transició pgu
            if e.key == K_ESCAPE:
                pygame.mixer.music.fadeout(500)
                return self.game.change_state('MENU')
            
        if not self.player.atacant:
            self.player.basic1_state = False
            self.player.basic2_state = False
        if not self.enemy.atacant:
            self.enemy.basic1_state = False
            self.enemy.basic2_state = False
            
        if e.type is KEYUP:
            #atacs dels jugadors
            

            if e.key == K_h:
                self.player.try_especial_state = False
           
                
            if e.key == K_p:
                self.enemy.try_especial_state = False

            #moviment dels jugaors               
            if e.key == K_a:
                self.player.walking_state = False
                self.player.go_left=False

            if e.key == K_d:
                self.player.walking_state = False
                self.player.go_right=False

            if e.key == K_s:
                self.player.down_state = False

            if e.key == K_DOWN:
                self.enemy.down_state = False

            if e.key == K_LEFT:
                self.enemy.walking_state = False
                self.enemy.go_left=False

            if e.key == K_RIGHT:
                self.enemy.walking_state = False
                self.enemy.go_right=False
            
            #salts del jugadors    
            if e.key == K_w:
                self.player.jumping_state = False 
            if e.key == K_UP:
                self.enemy.jumping_state = False
            
    def loop(self):
        if len(self.stadiums) == 0:
            self.stadium = Stadium(self,WIDTH*0.5-278, HEIGHT)
            self.stadiums.add(self.stadium)
            self.all_sprites.add(self.stadium)
        self.all_sprites.update()
        self.platforms.update()
        self.clouds.update()
        self.power_up.update()
        self.coins.update()
        self.update(self.game.screen)
                        
        #end match
        if self.enemy.life <= 0:
            pygame.mixer.music.fadeout(500)
            return self.game.change_state('PLAYER 1 WINS')
        if self.player.life <= 0:
            pygame.mixer.music.fadeout(500)
            return self.game.change_state('PLAYER 2 WINS')
                    
    def update(self,screen):
        pygame.display.set_caption("{:0.2f}".format(self.game.crono.get_fps()))#per veure si hi ha lagg
        screen.fill((153, 204, 255)) #(204, 230, 255)
        self.clouds.draw(screen)
        self.all_sprites.draw(screen)
        self.platforms.draw(screen)
        self.power_up.draw(screen)
        self.coins.draw(screen)
        screen.blit(self.stadium.image, self.stadium.rect)
        self.projectils_player1_group.draw(screen)
        self.projectils_enemy_group.draw(screen)
        screen.blit(self.enemy.image, self.enemy.rect)
        screen.blit(self.enemy.tag.image, self.enemy.tag.rect)
        screen.blit(self.player.image, self.player.rect)
        screen.blit(self.player.tag.image, self.player.tag.rect)
        screen.blit(self.player.lifebar.image, self.player.lifebar.rect)
        screen.blit(self.enemy.lifebar.image, self.enemy.lifebar.rect)
        screen.blit(self.player.coolbar.image, self.player.coolbar.rect)
        screen.blit(self.enemy.coolbar.image, self.enemy.coolbar.rect)
        screen.blit(self.pipe.image, self.pipe.rect)
        pygame.display.flip()


class Player1Wins(engine.State):
    def init(self):
        self.image = pygame.image.load("img/menus/player1_victory.png")     
    
    def paint(self, s):
        s.fill(WHITE)
        rect = self.image.get_rect()
        rect.center = s.get_rect().center
        s.blit(self.image, rect)
        pygame.display.flip()
        
    def event(self,e): 
        if e.type is KEYDOWN:
            if e.key == K_RETURN:
                return self.game.change_state('MENU')
            if e.key == K_s:
                if not self.game.muted:
                    pygame.mixer.music.fadeout(500)
                    pygame.mixer.music.load('sounds/ow.ogg')
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(loops=-1)
                return self.game.change_state('SELECT CHAR MENU')
            
class Player2Wins(engine.State):
    def init(self):
        self.image = pygame.image.load("img/menus/player2_victory.png")     
    
    def paint(self, s):
        s.fill(WHITE)
        rect = self.image.get_rect()
        rect.center = s.get_rect().center
        s.blit(self.image, rect)
        pygame.display.flip()
        
    def event(self,e): 
        if e.type is KEYDOWN:
            if e.key == K_RETURN:
                return self.game.change_state('MENU')
            if e.key == K_s:
                pygame.mixer.music.fadeout(500)
                if not self.game.muted:
                    pygame.mixer.music.load('sounds/ow.ogg')
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(loops=-1)
                return self.game.change_state('SELECT CHAR MENU')
     
def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
