import data
import pygame as pg
from pygame.locals import *
import sys
import math

HEIGHT = 600
WIDTH = 800

MOVESPEED = 0.3
ANGSPEED = 6

class Player(pg.sprite.Sprite):
    def __init__(self):
        self.img = load_image(data.filepath('nave.png'), True)
        self.rect = self.img.get_rect()
        self.rect.centerx = 50
        self.rect.centery = WIDTH/2

    def update(self, movex, movey, delta=1):
        '''update ship.s movement '''
        self.rect.centerx += movex*MOVESPEED*delta
        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= WIDTH:
            self.rect.right = WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
        self.rect.centery += movey*MOVESPEED*delta

class Pala(pg.sprite.Sprite):
    def __init__(self, player):
        self.player = player
        #self.img = load_image(data.filepath('palashadow_placeholder.png'), True)
        self.img = load_image(data.filepath('pala2.png'), True)
        self.img_original = self.img.copy()
        self.rect = self.img.get_rect()
        self.angle = 0
        self.angle2 = 0
        self.distance = 400
        self.rect.centerx = self.player.rect.centerx + self.distance
        self.rect.centery = self.player.rect.centery

    def update2(self, angle, delta=1):
        self.angle = (self.angle + angle)%360
        re = self.rect.copy()
        img = pg.transform.rotate(self.img_original, self.angle)
        re.center = img.get_rect().center
        self.img = img.subsurface(re).copy()
        
        self.rect.centerx = self.player.rect.centerx + math.cos(math.radians(self.angle)) * self.distance
        self.rect.centery = self.player.rect.centery - math.sin(math.radians(self.angle)) * self.distance
        if (angle):
            print('%d,%d - %f/%f: %f-%f\n' % (self.rect.centerx, self.rect.centery, self.angle, 
                math.radians(self.angle), math.cos(math.radians(self.angle)) * self.distance, 
                math.sin(math.radians(self.angle)) * self.distance))

def angulo(x1,y1, x2, y2):
    return math.atan2(y2-y1, x1-x2)

def load_image(filename, transparent=False):
        try:
            image = pg.image.load(filename)
        except pg.error, message:
                raise SystemExit(message)
        image = image.convert()
        if transparent:
                color = image.get_at((0, 0))
                image.set_colorkey(color, RLEACCEL)
        #print "cargada"
        return image

def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def escribe(texto, posx, posy, color=(255, 255, 255)):
    fuente = pg.font.Font(data.filepath('DroidSans.ttf'), 25)
    salida = pg.font.Font.render(fuente, texto, 1, color)
    salida_rect = salida.get_rect()
    salida_rect.centerx = posx
    salida_rect.centery = posy
    return salida, salida_rect

def juego(screen):
    run = 1  # better than true for whiles
    clock = pg.time.Clock()
    movey = 0         # movimiento de la pala1
    movex = 0
    angulo = 0
    points = 0  # puntuacion de las palas
    player = Player()
    pala = Pala(player)
    bg = load_image(data.filepath('bg_placeholder.jpg'))
    while run:
        delta = clock.tick(30)

        for evs in pg.event.get():
            if evs.type == QUIT:
                sys.exit()
            if evs.type == KEYDOWN:
                if evs.key in (K_UP, K_w):
                    movey = -1
                if evs.key in (K_DOWN, K_s):
                    movey = 1
                if evs.key in (K_LEFT, K_a):
                    movex = -1
                if evs.key in (K_RIGHT, K_d):
                    movex = 1
                if evs.key in (K_z, K_q):
                    angulo = ANGSPEED
                if evs.key in (K_x, K_e):
                    angulo = -ANGSPEED
                if evs.key == K_ESCAPE:
                    run = 0
            if evs.type == KEYUP:
                if evs.key in (K_UP, K_w, K_DOWN, K_s):
                    movey = 0
                if evs.key in (K_LEFT, K_a, K_RIGHT, K_d):
                    movex = 0
                if evs.key in (K_z, K_q, K_x, K_e):
                    angulo = 0
        targetx, targety = pg.mouse.get_pos()
        

        player.update(movex, movey, delta)
        pala.update2(angulo, delta)
        screen.blit(bg, (0,0))
        screen.blit(player.img, player.rect)
        screen.blit(pala.img, pala.rect)
        pg.display.flip()

def main():
    """ your app starts here
    """
    
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Bot uprise")
    
    juego(screen)
    return 0