import pygame
import os
import math
from enum import Enum, auto
from init import screen, resolution
from CollisionDetection import Collider, GJK
import numpy as np

# 遊戲資料夾位址
path = os.path.dirname(os.path.abspath(__file__))
# 友軍火力傷害
friendly_fire = True
# Global Default Variables
## Character
## Player
D_init_round = 0
D_max_round = 3
D_player_max_hp = 5
D_player_speed = 30
## Monster
D_monster_max_hp = 5
D_monster_speed = 10
D_monster_dmg = 5
## bullet
D_normal_bullet_dmg = 5
D_normal_bullet_speed = 60
D_fireball_dmg = 2
D_fireball_speed = 50
D_iceball_dmg = 20
D_iceball_speed = 40
D_word_dmg = 20
D_word_speed = 10

# List of Players
Players = []
# List of Words
Words = []
# List of Monsters
Monsters = []
# List of Bullets
Bullets = []
# List of Backgrounds
Backgrounds = []
# List of HPs
HPs = []
# List of Timers
TimerFlags = []
Timers = []
# List of relations of objects
CollisionTriggerList = []
AoeTriggerList = []
InstantTriggerList = []

class Timer:
    def __init__(self, tick, callback, flag_index):
        Timers.append(self)
        self.lastTick = pygame.time.get_ticks()
        self.tick = tick
        self.callback = callback
        self.flag_index = flag_index
    def exec(self):
        if(pygame.time.get_ticks() - self.lastTick >= self.tick):
            self.callback()
            if(self.flag_index is not None):
                Timers.remove(self)
                TimerFlags[self.flag_index] = True
def setTimeout(callback, ms, flagIndex=None):
        if(TimerFlags[flagIndex]):
            Timer(ms, callback, flagIndex)
            TimerFlags[flagIndex] = False
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
class Img:
    def __init__(self, path, size):
        self.path = path
        self.size = size
def ColliderHelper(x):
    topleft = np.add(x.position, x.Rect.topleft)
    topright = np.add(x.position, x.Rect.topright)
    bottomleft = np.add(x.position, x.Rect.bottomleft)
    bottomright = np.add(x.position, x.Rect.bottomright)
    return Collider((
    (bottomleft[0], bottomleft[1], 0),\
    (bottomright[0], bottomright[1], 0),\
    (topleft[0], topleft[1], 0),\
    (topright[0], topright[1], 0)\
    ))
def is_collision(i, j):
    i = ColliderHelper(i)
    j = ColliderHelper(j)
    return GJK(i, j)
def TriggerRegister(type, attacker, victim, both_way=False):
    # type => 'collision', 'AOE', 'instant'
    # attacker, victim: List of Objs
    x = {'attacker':attacker, 'victim':victim, 'both_way':both_way}
    if(type == 'collision'):
        CollisionTriggerList.append(x)
    elif(type == 'AOE'):
        AoeTriggerList.append(x)
    elif(type == 'instant'):
        InstantTriggerList.append(x)
    
def CollisionDetection():
    for relation in CollisionTriggerList:
        attacker = relation['attacker']
        victim = relation['victim']
        both_way = relation['both_way']
        for i in attacker:
            if(i.collision_dmg == 0):
                continue
            for j in victim:
                if(is_collision(i, j)):
                    # inform attacker
                    i.collide_with(j)
                    if(both_way is True):
                        # inform victim
                        j.collide_with(i)
                    print(j.name, j.hp)
class _NeedRender:
    def __init__(self, position):
        self.position = position # position是該物件topleft的絕對位置
        self.PygameObj = None
        self.Rect = None
    def blit(self):
        screen.blit(self.PygameObj, self.position)
    def createPygameObj(self):
    # Class need to have [img](path, size), [position] Properties
        self.PygameObj = pygame.image.load(os.path.join(path, self.img.path)).convert_alpha()
        self.PygameObj  = pygame.transform.scale(self.PygameObj , self.img.size)
        self.Rect = self.PygameObj.get_rect() 
    def move(self, diffXYList):
        self.position = np.add(self.position, diffXYList)
    def moveto(self, XYList):
        self.position = (XYList[0], XYList[1])
    def isOutOfScreen(self):
        return (self.position[0] > resolution[0] or \
                self.position[1] > resolution[1] or \
                self.position[0] + self.Rect.width < 0 or \
                self.position[1] + self.Rect.height < 0)
class _Character(_NeedRender):
    def __init__(self, name, team, position, direction):
        super().__init__(position)
        self.name = name
        self.team = team
        self.owner = self
        self.direction = direction
        self.is_alive = True
        self.collision_dmg = 0
        self.max_hp = 404
        self.hp = self.max_hp
        self.round = []
    def rush(self):
        pass
    def hurtBy(self, who, amount):
        if(who.owner.team is not self.team or friendly_fire is False):
            if(self.hp >= amount):
                self.hp -= amount
            else:
                self.hp = 0
                self.is_alive = False
    def heal(self, amount):
        if(self.hp + amount < self.max_hp):
            self.hp += amount
        else:
            self.hp = self.max_hp
            return -1 # tell caller heal failed
    def shoot(self):
        if(len(self.round) > 0):
            bullet = self.round[-1]
            self.round.pop()
            bullet.fire(self)
        else:
            return -1 # tell caller shoot failed
class _Player(_Character):
    def __init__(self, name, team, position, direction):
        super().__init__(name, team, position, direction)
        Players.append(self)
        self.max_hp = D_player_max_hp
        self.hp = self.max_hp
        self.max_round = D_max_round
        self.speed = D_player_speed
        self.input = ''
        self.isUp = 0
        self.isDown = 0
        self.isLeft = 0
        self.isRight = 0
    def change_shoot_mode(self, mode):
        pass
    def save_round(self, bullet):
        if(len(self.round) < self.max_round):
            self.round.append(bullet)
        else:
            Bullets.remove(bullet)
    def updateCoordinate(self):
        if(self.isUp + self.isDown + self.isLeft + self.isRight != 0):
            direction = [self.isLeft * -1 + self.isRight * 1 , self.isUp * -1 + self.isDown * 1]
            if(abs(direction[0] + direction[1]) != 1):
                direction = np.multiply(direction, 0.7071)
            self.direction = tuple(direction)
            self.move(np.multiply(direction, self.speed))
    def commit(self):
        c = 0
        for i in Words:
            if(i.content == self.input):
                c += 1
                i.content = None
        while(None in Words):
            Words.remove(None)
        if(c == 0):
            pass
        elif(c == 1):
            self.save_round(NormalBall())
        elif(c == 2):
            self.save_round(FireBall())
        elif(c == 3):
            self.save_round(IceBall())
        self.input = ''
class Alien(_Player):
    def __init__(self, name, team, position, direction):
        super().__init__(name, team, position, direction)
        self.img = Img('asset/player01.png', (150,120))
        self.createPygameObj()

class _Monster(_Character):
    def __init__(self, name, position, direction):
        super().__init__(name, Team.Monster, position, direction)
        Monsters.append(self)
        self.collision_dmg = D_monster_dmg
        self.hp = D_monster_max_hp
        self.max_hp = D_monster_max_hp
        self.speed = D_monster_speed
    def random_walk(self):
        pass
    def straight_to_target(self, target):
        pass
    def spin_bot(self):
        pass
class Bacteria(_Monster):
    def __init__(self, name, position, direction):
        super().__init__(name, position, direction)
        self.img = Img('asset/monster01.png', (200,180))
        self.createPygameObj()
    def collide_with(self, who):
        if(who in Players):
            who.hurtBy(self, self.collision_dmg)
class _Bullet(_NeedRender):
    def __init__(self):
        super().__init__(position=None)
        Bullets.append(self)
        self.owner = None
        self.collision_dmg = 0
        self.fired_dmg = 0
        self.speed = 0
        self.isFired = False
        self.fired_direction = None
        self.can_through = False
    def fire(self, owner):
        self.isFired = True
        self.owner = owner
        self.position = owner.position
        self.fired_direction = owner.direction
        self.collision_dmg = self.fired_dmg
    def fly(self):
        self.move(np.multiply(self.fired_direction, self.speed))
    def extra_fx():
        pass
    def stop(self, obj):
        self.extra_fx()
        if(self.can_through):
            pass
        else:
            self.speed = 0
            # bullet gone or some effect  
    def collide_with(self, who):
        if(who in Players or who in Monsters):
            who.hurtBy(self, self.collision_dmg)
class NormalBall(_Bullet):
    def __init__(self):
        super().__init__()
        self.fired_dmg = D_normal_bullet_dmg
        self.speed = D_normal_bullet_speed
        self.img = Img('asset/bullet01.png', (60, 50))
        self.createPygameObj()
class FireBall(_Bullet):
    def __init__(self):
        super().__init__()
        self.fired_dmg = D_fireball_dmg
        self.speed = D_fireball_speed
        self.img = Img('asset/bullet03.png', (100, 56))
        self.createPygameObj()
    def extra_fx(self):
        pass
        # fire enemy up
class IceBall(_Bullet):
    def __init__(self):
        super().__init__()        
        self.fired_dmg = D_iceball_dmg
        self.speed = D_iceball_speed
        self.img = Img('asset/bullet02.png', (100, 56))
        self.createPygameObj()
    def extra_fx(self):
        pass
        # freeze enemy
class Word(_Bullet):
    def __init__(self, content):
        super().__init__()  
        Words.append(self)
        self.fired_dmg = D_word_dmg
        self.speed = D_word_speed
        self.content = content
        # self.img = Img('asset/bullet01.png', (60, 50))
        # self.createPygameObj()
    def changeContent(self, content):
        self.content = content
class Background(_NeedRender):
    def __init__(self, img, position):
        super().__init__(position)
        Backgrounds.append(self)
        self.img = img
        self.createPygameObj()



    
