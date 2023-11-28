'''
Author: Jacob Martinez
Description: 
'''

#character class

class Character():
    def __init__ (self, name, hp, speed, weapon):
        self.name = name
        self.hp = hp 
        self.speed = speed
        self.weapon = weapon

    def physics():
        pass

    def take_damage():
        pass

class Player(Character): 
    def move():
        pass

    def shoot():
        pass

    def fall():
        pass

class Enemy(Character):
    def move():
        pass

    def shoot():
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
    def __init__(self, speed, ammo):
        self.speed = speed
        self.ammo = ammo

