'''
Author: Jacob Martinez, Jason Chamorro
sources:
https://www.youtube.com/watch?v=JmpA7TU_0Ms
Description: 
'''
import pygame
import random

from pygame.sprite import _Group
from bootup import *
#character class

class Character():
    def __init__ (self, name, hp, speed, weapon, x, y):
        self.name = name
        self.hp = hp 
        self.speed = speed
        self.weapon = weapon
        self.rect = self.image.get_rect(topleft=(x, y))

    def physics():
        pass

    def take_damage():
        pass

    def shoot(self):
        return(Bullet(self.rect.topleft[0], self.rect.topleft[1], 10, 0))

    #possibly make the shoot, aka create bullet function here but I want to try and make it in other function 

class Player(Character): 
    def move():
        pass


     #change to make bullet speed and drop based on the weapon

        

    def fall():
        pass

class Enemy(Character):
    def move():
        pass

    def die():
        pass

#Platform Class

class Platform():
    def __init__(self, speed, hp):
        self.speed = speed
        self.hp = hp

    def move():
        pass

    def platform_break():
        pass

#Weapon Class

class Weapon():
    def __init__(self, speed, ammo, drop):
        self.speed = speed
        self.ammo = ammo
        self.drop = drop

class Bullet(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y, speed, drop):
        super().__init__()
        self.speed = speed
        self.drop = drop
        self.image = pygame.Surface(25,25)
        self.image.fill(255,0,0)
        self.rect = self.image.get_rect(center =(pos_x, pos_y))
    
    def update_bullet_pos(self):
        self.rect.x += self.speed
        self.rect.y -= self.drop #change this to have arc affect 


bullet_group = pygame.sprite.Group()




