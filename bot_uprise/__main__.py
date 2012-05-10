import data
import pygame as pg
from pygame.locals import *
import sys
import math
import cmath
import random
from common import *
from enemy import *
from player import *

def juego(screen):
    clock = pg.time.Clock()
    movey = 0         # movimiento de la pala1
    movex = 0
    angulo = 0
    points = 0  # puntuacion de las palas
    xpos = 0
    player = Player()
    pala = Pala(player)
    shadow = Pala(player, 'shadow.png')
    bullet_list = pg.sprite.Group()
    enemy_list = pg.sprite.Group()
    bg = load_image(data.filepath('bg.png'))
    background = pg.Surface(screen.get_size())
    #background.fill((0,0,0))
    background.blit(bg, (xpos,0))
    spawn_timer = SPAWNTIME
    lifes = NUMLIFES
    score = 0

    explosion_snd = load_sound(data.filepath('explosion.wav'))
    hit_snd = load_sound(data.filepath('hit.wav'))
    laser_snd = load_sound(data.filepath('laser.wav'))
    reflect_snd = load_sound(data.filepath('reflect.wav'))

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
                laser_snd.play()
            if evs.type == EVT_REMOVE_BULLET:
                bullet_list.remove(evs.elto)
            if evs.type == EVT_ENEMY_KILLED:
                print ('enemy down')
                explosion_snd.play()
                evs.baddie.kill()
                score += 10
            if evs.type == EVT_PLAYER_KILLED:
                lifes -= 1 # TODO: reactivate
                hit_snd.play()
                print ('player down')
            if evs.type == EVT_REFLECT_BULLET:
                reflect_snd.play()
                

            if evs.type == MOUSEBUTTONDOWN:
                tx, ty = pg.mouse.get_pos()
                dx, dy = pala.displace(tx, ty)
                #print "pulsaste en %s,%s (originalmente %s, %s) player %s, %s/%s" % (dx, dy, tx, 
                #ty, player.rect.centerx, player.rect.centery, pala.angle)

                
        
        spawn_timer -= delta
        if spawn_timer <= 0:
            spawn_timer = SPAWNTIME
            if not random.randint(0,SPAWNRND):
                enemy_list.add(Enemy(random.randint(0,HEIGHT)))

        player.update(movex, movey, delta)
        pala.update2(angulo, delta)
        shadow.update2(angulo, delta)
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
        
        #for b in bullet_list:
        #    screen.blit(b.img, b.rect)
        #for e in enemy_list:
        #    screen.blit(e.img, e.rect)
        bullet_list.draw(screen)
        enemy_list.draw(screen)
        #subshadow = shadow.img.subsurface(pg.rect.Rect(0,0,WIDTH,HEIGHT))
        screen.blit(shadow.img, shadow.rect)
        screen.blit(pala.img, pala.rect)
        screen.blit(punt, punt_rect)

        pg.display.flip()
    bullet_list.empty()
    enemy_list.empty()
    return score


def title(screen):
    '''
    Title screen
    '''
    bg = load_image(data.filepath('inicio.png'))
    blinky = load_image(data.filepath('title.png'))
    title = pg.Surface(blinky.get_size())
    clock = pg.time.Clock()
    itson = False
    fin = 1
    if itson:
        count = random.choice([1000,5000,15000, 20000])
    else:
        count = random.choice([500, 2000])
    screen.blit(bg, (0,0))
    title.blit(blinky,(0,0))
    while fin:
        delta = clock.tick(30)
        count -= delta

        for evs in pg.event.get():
            if evs.type == QUIT:
                sys.exit()
            if evs.type == KEYDOWN:
                if evs.key in (K_KP_ENTER, K_RETURN):
                    fin = 0
                if evs.key == K_ESCAPE:
                    sys.exit()

        
        if count<=0:
            itson = not itson
            if itson:
                count = random.choice([100,500,1500, 2000])
            else:
                count = random.choice([50, 200])
        if itson:
            title.blit(blinky,(0,0))
        else:
            title.fill((0,0,0))
        screen.blit(title, (330, 160))
        pg.display.flip()

def main():
    """ your app starts here
    """
    
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Bot uprise")
    while 1:
        title(screen)
        score = juego(screen)
    return 0
