import pygame

class Spritesheet:
    def __init__(self,filename):
        self.spritesheet = pygame.image.load(filename).convert()
        if filename in ['img/heroes/kid_goku.png', 'img/assets/arena.png', 'img/heroes/kirby_sprite.png',
                        'img/heroes/mario_sprite.png', 'img/heroes/sonic.png','img/assets/cloud_sprite.png',
                        'img/heroes/link_sprite.png', 'img/assets/power_up_sprite.png','img/assets/pipe.png',
                        'img/assets/vortex.png', 'img/assets/golden_egg.png','img/assets/bg.png']:
            self.spritesheet.set_colorkey((255,255,255))

    def get_image(self,x,y,width, height):
        image = pygame.Surface((width,height),pygame.SRCALPHA)
        image.blit(self.spritesheet, (0,0),(x,y,width,height))
        return image
