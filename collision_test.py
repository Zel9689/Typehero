import pygame
from CollisionDetection import Collider, GJK
pygame.init()
screen = pygame.display.set_mode([500, 500])
bg = pygame.Surface(screen.get_size())
bg = bg.convert()
bg.fill((255, 255, 255))
x = pygame.draw.rect(bg, (0,0,255),[70, 70, 200, 60], 4)
rr = pygame.Surface((200, 60))
rr.fill((255,0,255))
y = pygame.draw.rect(rr, (0,0,0),[0, 0, 200, 60], 4)
rect = rr.get_rect()
def ColliderHelper(x):
    return Collider((
    (x.bottomleft[0], x.bottomleft[1], 0),\
    (x.bottomright[0], x.bottomright[1], 0),\
    (x.topleft[0], x.topleft[1], 0),\
    (x.topright[0], x.topright[1], 0)\
    ))
xx = ColliderHelper(x)


pygame.display.update()
clock = pygame.time.Clock() 
running = True
while running:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if(event.key == pygame.K_UP):
                rect.center = (rect.center[0], rect.center[1] - 5)
            if(event.key == pygame.K_DOWN):
                rect.center = (rect.center[0], rect.center[1] + 5)
            if(event.key == pygame.K_LEFT):
                rect.center = (rect.center[0] - 5, rect.center[1])
            if(event.key == pygame.K_RIGHT):
                rect.center = (rect.center[0] + 5, rect.center[1])
            yy = ColliderHelper(rect)
            print(GJK(xx, yy))
    screen.blit(bg, (0,0))
    screen.blit(rr, rect.topleft)
    
    pygame.display.update()
pygame.quit()  