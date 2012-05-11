from common import *
import data
import pygame as pg
import random
import math

class Player(pg.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.img_original = load_image(data.filepath('nave.png'), True)
        self.img = self.img_original
        self.no_img = pg.Surface(self.img.get_size())
        self.no_img.fill((0,0,0))
        self.rect = self.img.get_rect()
        self.rect.centerx = 50
        self.rect.centery = WIDTH/2
        self.collider = pg.rect.Rect(
            self.rect.centerx - 30, #left
            self.rect.centery - 10, #top
            60,
            40)
        self.invulnerable = 0
        self.visible = True

    def update(self, movex, movey, delta=1):
        '''update ship.s movement '''
        if self.invulnerable > 0:
            self.invulnerable -= delta
            self.visible = not self.visible
            if self.invulnerable <= 0:
                self.invulnerable = 0
                self.visible = True
        if self.visible:
            self.img = self.img_original
        else:
            self.img = self.no_img
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
    def __init__(self, player, img='pala2.png'):
        super(Pala, self).__init__()
        self.player = player
        #self.img = load_image(data.filepath('palashadow_placeholder.png'), True)
        self.img = load_image(data.filepath(img), True)
        self.img_original = self.img.copy()
        self.rect = self.img.get_rect()
        self.angle = 0
        self.angle2 = 0
        self.distance = 0
        self.rect.centerx = self.player.rect.centerx + self.distance
        self.rect.centery = self.player.rect.centery
        self.collider = pg.rect.Rect(-4,-30,20,60) #bullets have to be displaced to check against

    def update2(self, angle, delta=1):
        self.angle = (self.angle + angle)%360
        re = self.rect.copy()
        img = pg.transform.rotate(self.img_original, self.angle)
        re.center = img.get_rect().center
        self.img = img.subsurface(re).copy()
        
        self.rect.centerx = self.player.rect.centerx + math.cos(math.radians(self.angle)) * self.distance
        self.rect.centery = self.player.rect.centery + math.sin(math.radians(self.angle)) * self.distance
        #if (angle):
        #    print('%d,%d - %f/%f: %f-%f\n' % (self.rect.centerx, self.rect.centery, self.angle, 
        #        math.radians(self.angle), math.cos(math.radians(self.angle)) * self.distance, 
        #        math.sin(math.radians(self.angle)) * self.distance))

    def displace(self, x, y):
        '''puts the center in the same space as the crane'''
        an = math.radians(-self.angle)
        x1 = x - (self.player.rect.centerx + 64*math.cos(an))
        y1 = y - (self.player.rect.centery + 64*math.sin(an)) 
        x2, y2 = rotate_point(x1, y1, an)
        #return (x1*math.cos(an) + y1*math.sin(an), (-x1*math.sin(an) + y1*math.cos(an)))
        return x2, y2
        
        #are signs right? :S

    def collide_bullet(self, bullet):
        if ((bullet.angle + 90) % 360 <= self.angle and (bullet.angle - 90) % 360 >= self.angle):
            (x, y) = self.displace(bullet.rect.centerx, bullet.rect.centery)
            return self.collider.colliderect(pg.rect.Rect(x-8, y - 8, 16,16))
        else: #don't want it bouncing inside the rect
            return False


class Shadow(pg.sprite.Sprite):
    def __init__(self, pala):
        self.pala = pala
        self.img = load_image(data.filepath('shadow.png'), True)
        self.img_original = self.img.copy()
        self.rect = self.img.get_rect()
        self.rect.center = self.pala.rect.center

    def update(self, angle, delta=1):
        self.angle = (self.angle + angle) % 360
        re = self.rect.copy()
        img = pg.transform.rotate(self.img_original, self.angle)
        re.center = img.get_rect().center
        self.img = img.subsurface(re).copy()
        
        self.rect.centerx = self.pala.player.rect.centerx + math.cos(math.radians(self.angle)) * self.distance
        self.rect.centery = self.pala.player.rect.centery + math.sin(math.radians(self.angle)) * self.distance