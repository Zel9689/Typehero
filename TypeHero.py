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

#monsters
monster = pygame.image.load(os.path.join(path, 'monster01.png'))
monster = monster.convert()

#ball(example code)
ball = pygame.Surface((30,30))
ball.fill((255,255,255))
pygame.draw.circle(ball, (0,0,255), (15,15), 15, 0)
rect1 = ball.get_rect()
rect1.center = (320,45)
x, y = rect1.topleft
dx = 3

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
    screen.blit(monster, (0,0))
    x += dx
    rect1.center = (x, y)
    if (rect1.left<=0 or rect1.right>=screen.get_width()):
        dx *= -1
    screen.blit(ball,rect1.topleft)
    pygame.display.update()
pygame.quit()
