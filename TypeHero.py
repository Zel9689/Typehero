import pygame
import os

#init
pygame.init()
pygame.display.set_caption("Type Hero")
resolutionX=800
resolutionY=600
screen = pygame.display.set_mode((resolutionX, resolutionY))
background = pygame.Surface(screen.get_size())
path = os.path.split(os.path.abspath(__file__))[0]

#background
background.fill((125,125,125))
background = background.convert()

#words

#player picture

#player's bullet

#player health

#monsters picture
monster = pygame.image.load(os.path.join(path, 'monster01.png'))
monster = monster.convert()
monsterRect = monster.get_rect()
monsterHeight = monsterRect.height
monsterWidth = monsterRect.width
print('height= ', monsterHeight)
print('width= ', monsterWidth)
monsterRect.center = (800,500) #微調怪物位置
x, y = monsterRect.topleft
print(x,y)
dy = 3 #移動速度
print(monsterRect.top)
print(monsterRect.bottom)

#monsters health


#ball(example code)
'''
ball = pygame.Surface((30,30))
ball.fill((255,255,255))
pygame.draw.circle(ball, (0,0,255), (15,15), 15, 0)
rect1 = ball.get_rect()
rect1.center = (26,300)
x, y = rect1.topleft
dx = 3
'''

#game clock
clock = pygame.time.Clock()

#Loop
running = True
while running:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.blit(background, (0,0))

#moving monster
    y += dy
    monsterRect.center = (x, y)
    if (monsterRect.top<=0 or monsterRect.bottom>=screen.get_height()):
        dy *= -1
    screen.blit(monster,monsterRect.topleft)

    pygame.display.update()
pygame.quit()
