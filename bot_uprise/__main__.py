import data
import pygame as pg
from pygame.locals import *
import sys
import math
import random

HEIGHT = 600
WIDTH = 800

GLOBALSPEED = 1 

MOVESPEED = 0.3 * GLOBALSPEED
ANGSPEED = 12 * GLOBALSPEED
BGSPEED = 0.3 * GLOBALSPEED
BULLETSPEED = 0.5 * GLOBALSPEED
RECARGA = 200 * GLOBALSPEED
SPAWNRND = 5 * GLOBALSPEED # 1 in SPAWNRND posibilities of spawning a baddie
SPAWNTIME = 400 * GLOBALSPEED
NUMLIFES = 5

EVT_FIRE = 24
EVT_REMOVE_BULLET = 25
EVT_ENEMY_KILLED = 26
EVT_PLAYER_KILLED = 27

class Player(pg.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.img = load_image(data.filepath('nave.png'), True)
        self.rect = self.img.get_rect()
        self.rect.centerx = 50
        self.rect.centery = WIDTH/2
        self.collider = pg.rect.Rect(
            self.rect.centerx - 30, #left
            self.rect.centery - 10, #top
            60,
            40)

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
        self.collider.centerx = self.rect.centerx
        self.collider.bottom = self.rect.bottom -10

class Pala(pg.sprite.Sprite):
    def __init__(self, player):
        super(Pala, self).__init__()
        self.player = player
        #self.img = load_image(data.filepath('palashadow_placeholder.png'), True)
        self.img = load_image(data.filepath('pala2.png'), True)
        self.img_original = self.img.copy()
        self.rect = self.img.get_rect()
        self.angle = 0
        self.angle2 = 0
        self.distance = 0
        self.rect.centerx = self.player.rect.centerx + self.distance
        self.rect.centery = self.player.rect.centery
        self.collider = pg.rect.Rect(-14,-36,40,72) #bullets have to be displaced to check against

    def update2(self, angle, delta=1):
        self.angle = (self.angle + angle)%360
        re = self.rect.copy()
        img = pg.transform.rotate(self.img_original, self.angle)
        re.center = img.get_rect().center
        self.img = img.subsurface(re).copy()
        
        self.rect.centerx = self.player.rect.centerx + math.cos(math.radians(self.angle)) * self.distance
        self.rect.centery = self.player.rect.centery - math.sin(math.radians(self.angle)) * self.distance
        #if (angle):
        #    print('%d,%d - %f/%f: %f-%f\n' % (self.rect.centerx, self.rect.centery, self.angle, 
        #        math.radians(self.angle), math.cos(math.radians(self.angle)) * self.distance, 
        #        math.sin(math.radians(self.angle)) * self.distance))

    def displace(self, x, y):
        '''puts the center in the same space as the crane'''
        an = math.radians(-self.angle)
        x1 = x - (self.player.rect.centerx + 64*math.cos(an))
        y1 = y - (self.player.rect.centerx + 64*math.sin(an)) 
        return (x1*math.cos(an) - y1*math.sin(an), (x1*math.sin(an) + y1*math.cos(an)))
        #are signs right? :S

    def collide_bullet(self, bullet):
        (x, y) = self.displace(bullet.rect.centerx, bullet.rect.centery)
        if self.collider.collidepoint(x,y):
            print "colision en %s,%s (originalmente %s, %s) player %s, %s/%s" % (x, y, bullet.rect.centerx, 
                bullet.rect.centery, self.player.rect.centerx, self.player.rect.centery, self.angle)
        return self.collider.colliderect(pg.rect.Rect(x-8, y - 8, 16,16))


class Bullet(pg.sprite.Sprite):
    def __init__(self, angle, posx, posy, origin):
        super(Bullet, self).__init__()
        self.image = load_image(data.filepath('bala.png'), True)
        self.rect = self.image.get_rect()
        self.angle = angle
        self.rect.centerx = posx
        self.rect.centery = posy
        self.collider = self.rect
        self.active = False #we don't want enemies selfdestructing the moment they fire
        self.origin = origin

    def update(self, delta, lista, player, pala):
        #check for collisions
        self.rect.centerx += math.cos(math.radians(self.angle))*BULLETSPEED*delta
        self.rect.centery += math.sin(math.radians(self.angle))*BULLETSPEED*delta
        if (self.rect.centerx < 0 or self.rect.centerx > WIDTH or 
            self.rect.centery < 0 or self.rect.centery > HEIGHT):
            pg.event.post(pg.event.Event(EVT_REMOVE_BULLET, elto=self))
        if not self.active:
            if not self.collider.colliderect(self.origin.collider):
                self.active = True # lock and loaded
                self.origin = None #we don't want the bullet holding a reference
        else:
            if pala.collide_bullet(self):
                self.deflect(pala.angle)
                print "boink!"
            elif self.check_collisions(player, lista):
                pg.event.post(pg.event.Event(EVT_REMOVE_BULLET, elto=self))

    def deflect(self, angle):
        '''
        If the bullet hits the mechanical arm, it should be deflected. 
        angle is the angle orthogonal to the surface of the arm.
        angle + (angle - self.angle)
        '''
        self.angle = (angle * 2 - self.angle) % 360

    def check_collisions(self, player, lista):
        col = self.collider.colliderect(player.collider)
        if not col:
            for e in lista.sprites():
                if self.collider.colliderect(e.collider):
                    col = True
                    pg.event.post(pg.event.Event(EVT_ENEMY_KILLED, baddie = e))
                    break
        else:
            pg.event.post(pg.event.Event(EVT_PLAYER_KILLED))
            return False
        return col

class Enemy(pg.sprite.Sprite):
    """docstring for Enemy"""
    def __init__(self, y):
        super(Enemy, self).__init__()
        self.image = load_image(data.filepath('protoenemy.png'), True)
        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.rect.centerx = WIDTH + 10
        self.carga = RECARGA
        self.collider = self.rect

    def update(self, delta):
        self.rect.centerx -= MOVESPEED * delta
        self.carga -= delta
        if self.carga <= 0 and self.rect.centerx <= WIDTH:
            pg.event.post(pg.event.Event(EVT_FIRE, x=self.rect.centerx, y=self.rect.centery, baddie= self))
            self.carga = RECARGA


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
    clock = pg.time.Clock()
    movey = 0         # movimiento de la pala1
    movex = 0
    angulo = 0
    points = 0  # puntuacion de las palas
    xpos = 0
    player = Player()
    pala = Pala(player)
    bullet_list = pg.sprite.Group()
    enemy_list = pg.sprite.Group()
    bg = load_image(data.filepath('bg.png'))
    background = pg.Surface(screen.get_size())
    #background.fill((0,0,0))
    background.blit(bg, (xpos,0))
    spawn_timer = SPAWNTIME
    lifes = NUMLIFES
    score = 0

    while lifes:
        delta = clock.tick(30)
        xpos = (xpos + BGSPEED*delta) % WIDTH

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
                    lifes = 0
                #if evs.key == K_PLUS:
                #    GLOBALSPEED += 0.1
                #if evs.key == K_MINUS:
                #    GLOBALSPEED -= 0.1

            if evs.type == KEYUP:
                if evs.key in (K_UP, K_w, K_DOWN, K_s):
                    movey = 0
                if evs.key in (K_LEFT, K_a, K_RIGHT, K_d):
                    movex = 0
                if evs.key in (K_z, K_q, K_x, K_e):
                    angulo = 0

            if evs.type == EVT_FIRE:
                angulo_tiro = math.degrees(math.atan2(player.rect.centery - evs.y,
                    player.rect.centerx - evs.x))
                bullet_list.add(Bullet(angulo_tiro, evs.x, evs.y, evs.baddie))
            if evs.type == EVT_REMOVE_BULLET:
                bullet_list.remove(evs.elto)
            if evs.type == EVT_ENEMY_KILLED:
                #print ('enemy down')
                evs.baddie.kill()
                score += 10
            if evs.type == EVT_PLAYER_KILLED:
                #lifes -= 1 # TODO: reactivate
                #print ('player down')
                pass

            if evs.type == MOUSEBUTTONDOWN:
                tx, ty = pg.mouse.get_pos()
                dx, dy = pala.displace(tx, ty)
                print "pulsaste en %s,%s (originalmente %s, %s) player %s, %s/%s" % (dx, dy, tx, 
                ty, player.rect.centerx, player.rect.centery, pala.angle)

                
        
        spawn_timer -= delta
        if spawn_timer <= 0:
            spawn_timer = SPAWNTIME
            if not random.randint(0,SPAWNRND):
                enemy_list.add(Enemy(random.randint(0,HEIGHT)))

        player.update(movex, movey, delta)
        pala.update2(angulo, delta)
        #for b in bullet_list:
        #    b.update(delta)
        bullet_list.update(delta, enemy_list, player, pala)
        #for e in enemy_list:
        #    e.update(delta)
        enemy_list.update(delta)

        punt, punt_rect = escribe("Lifes: %s Score: %s" % (lifes, score), 10, 20)

        background.blit(bg, (0,0), (xpos,0, WIDTH, HEIGHT))
        background.blit(bg, (WIDTH - xpos,0), (0,0, xpos, HEIGHT))
        #background.scroll(1,0)
        screen.blit(background,(0,0))
        screen.blit(player.img, player.rect)
        screen.blit(pala.img, pala.rect)
        #for b in bullet_list:
        #    screen.blit(b.img, b.rect)
        #for e in enemy_list:
        #    screen.blit(e.img, e.rect)
        bullet_list.draw(screen)
        enemy_list.draw(screen)
        screen.blit(punt, punt_rect)


        pg.display.flip()
    bullet_list.empty()
    enemy_list.empty()


def main():
    """ your app starts here
    """
    
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Bot uprise")
    
    juego(screen)
    return 0
