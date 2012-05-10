from common import *
import data
import pygame as pg
import math
import random

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
                pg.event.post(pg.event.Event(EVT_REFLECT_BULLET))
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
