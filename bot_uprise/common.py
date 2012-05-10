#Utility functions and constants
from pygame.locals import *
import data
import pygame as pg
import math
import cmath
import os

HEIGHT = 600
WIDTH = 800

GLOBALSPEED = 1 

MOVESPEED = 0.3 * GLOBALSPEED
ANGSPEED = 12 * GLOBALSPEED
BGSPEED = 0.3 * GLOBALSPEED
BULLETSPEED = 0.5 * GLOBALSPEED
RECARGA = 500 * GLOBALSPEED
SPAWNRND = 5 * GLOBALSPEED # 1 in SPAWNRND posibilities of spawning a baddie
SPAWNTIME = 400 * GLOBALSPEED
NUMLIFES = 5

EVT_FIRE = 24
EVT_REMOVE_BULLET = 25
EVT_ENEMY_KILLED = 26
EVT_PLAYER_KILLED = 27
EVT_REFLECT_BULLET = 28


def angulo(x1,y1, x2, y2):
    return math.atan2(y2-y1, x1-x2)

def rotate_point(x,y, angle):
    cangle = cmath.exp(angle*1j)  # in radians
    res = cangle * complex(x, y)
    return res.real, res.imag 

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

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pg.mixer:
        return NoneSound()
    fullname = os.path.join('data', name)
    try:
        sound = pg.mixer.Sound(fullname)
    except pg.error, message:
        print 'Cannot load sound:', wav
        raise SystemExit, message
    return sound

def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pg.transform.rotate(image, angle)
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