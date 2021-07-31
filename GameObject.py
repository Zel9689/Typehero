import pygame
import pygame.font as Pyfont
import os
import random
import math
from enum import Enum, auto

# Global Default Variables
## Character
D_max_hp = 5
D_speed = 10
## Player
D_init_round = 0
D_max_round = 3
D_player_max_hp = 5
D_player_speed = 10
## Monster
D_monster_max_hp = 5
D_monster_speed = 10
D_monster_dmg = 5
## bullet
D_normal_bullet_dmg = 5
D_normal_bullet_speed = 10
D_fireball_dmg = 2
D_fireball_speed = 15
D_iceball_dmg = 20
D_iceball_speed = 10
D_word_dmg = 20
D_word_speed = 10

class Gamemode(Enum):
    Menu = auto()
    Start = auto()
    Pause = auto()
    Dead = auto()
class Team(Enum):
    Monster = auto()
    TeamA = auto()
    TeamB = auto()
    TeamC = auto()
    TeamD = auto()

class Character:
    def __init__(self, name, team):
        self.name = name
        self.team = team
        self.max_hp = D_max_hp
        self.hp = self.max_hp
        # self.position
        # self.direction
        self.speed = D_speed
        self.is_alive = True
        self.dmg = 0
    def move_up(self):
        pass
    def move_down(self):
        pass
    def move_left(self):
        pass
    def move_right(self):
        pass
    def rush(self):
        pass
    def get_hit(self, obj):
        dmg = obj.dmg
        if(obj.owner.team is not self.team):
            if(self.hp >= dmg):
                self.hp -= dmg
            else:
                self.hp = 0
                self.is_alive = False
        #else it's bullet from teammates
    def heal(self, amount):
        if(self.hp + amount < self.max_hp):
            self.hp += amount
        else:
            self.hp = self.max_hp
            return -1 # tell caller heal failed
    def shoot(self):
        bullet = self.round[-1]
        if(len(self.round) > 0):
            self.round.pop()
            bullet.fire(self.position, self.direction)
        else:
            return -1 # tell caller shoot failed

class Player(Character):
    def __init__(self, name, team):
        super().__init__(name, team)
        self.max_hp = D_player_max_hp
        self.hp = self.max_hp
        self.round = []
        self.max_round = D_max_round 
    def change_shoot_mode(self, mode):
        pass
    def save_round(self, bullet):
        if(len(self.round) < self.max_round):
            self.round.append(bullet)

class Monster(Character):
    def __init__(self, name):
        super().__init__(name, Team.Monster)
        self.max_hp = D_monster_max_hp
        self.hp = self.max_hp
        self.dmg = D_monster_dmg
    def random_walk(self):
        pass
    def straight_to_target(self, target):
        pass
    def spin_bot(self):
        pass

class Bullet:
    def __init__(self, owner):
        self.owner = owner
        self.dmg = D_normal_bullet_dmg
        self.speed = D_normal_bullet_speed
        self.can_through = False
    def fire(self, origin, direction):
        # go to the direction from origin
        pass
    def extra_fx():
        pass
    def stop(self, character):
        self.extra_fx()
        if(self.can_through):
            pass
        else:
            self.speed = 0
            # bullet gone or some effect
    
class FireBall(Bullet):
    def __init__(self, owner):
        super().__init__(owner)
        self.dmg = D_fireball_dmg
        self.speed = D_fireball_speed
    def extra_fx(self):
        pass
        # fire enemy up
class IceBall(Bullet):
    def __init__(self, owner):
        super().__init__(owner)        
        self.dmg = D_iceball_dmg
        self.speed = D_iceball_speed
    def extra_fx(self):
        pass
        # freeze enemy
class Word(Bullet):
    def __init__(self, owner):
        super().__init__(owner)  
        self.dmg = D_word_dmg
        self.speed = D_word_speed