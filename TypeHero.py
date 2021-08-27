###### 多人遊戲的物件是從server獲取Word Player Monster物件
# tips: 要建screen、loop中更新screen
#       要建Surface、Surface才能用get_rect、取到的rect才能移動他，圖片也是種Surface
#       pygame.draw可以畫圖形在Surface上，但是不能取rect，畫上去就是死的，要透過移動Surface來移動他
import pygame
import math
import GameObject as GO

# 圖片資訊封裝
bg_img = GO.Img('asset/background.png', (1280, 768))
# 遊戲物件
p1 = GO.Alien('zel', GO.Team.TeamA, (120, 360), (1, 0))
m1 = GO.Bacteria('Baekk', (1000, 360), (-1, 0))
m1 = GO.Bacteria('Baekk2', (1200, 360), (-1, 0))
bg = GO.Background(bg_img, (0, 0))
bg2 = GO.Background(bg_img, (1280, 0))
# 物件關係
GO.TriggerRegister(type='collision', attacker=GO.Bullets, victim=GO.Players)
GO.TriggerRegister(type='collision', attacker=GO.Bullets, victim=GO.Monsters)
GO.TriggerRegister(type='collision', attacker=GO.Words, victim=GO.Players)
GO.TriggerRegister(type='collision', attacker=GO.Monsters, victim=GO.Players)
# 暴露在main loop的setTimeout要新增一個True在List中，當lock flag
GO.TimerFlags = [True]
# for debug
GO.Words = [GO.Word('a'), GO.Word('b'), GO.Word('c'), GO.Word('c'), GO.Word('b'), GO.Word('c')]

isHoldBackspace = False
running = True
while running:
    pygame.time.Clock().tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if(event.key == pygame.K_UP):
                p1.isUp = 1
            if(event.key == pygame.K_DOWN):
                p1.isDown = 1
            if(event.key == pygame.K_LEFT):
                p1.isLeft = 1
            if(event.key == pygame.K_RIGHT):
                p1.isRight = 1
            if(event.key == pygame.K_LCTRL):
                p1.shoot()
            if(event.key == pygame.K_RETURN):
                p1.commit()
            if(event.key == pygame.K_F2):
                for i in GO.Monsters:
                    i.hp = 10000
            if(event.key == pygame.K_BACKSPACE):
                p1.input = p1.input[:-1]
                print(p1.input)
                isHoldBackspace = True
                HoldBackspaceTick = pygame.time.get_ticks()
            if(event.key == pygame.K_ESCAPE):
                p1.input = ''
            if(event.key != pygame.K_RETURN 
            and event.key != pygame.K_ESCAPE
            and event.key != pygame.K_BACKSPACE):
                p1.input += event.unicode
                print(p1.input)
        if event.type == pygame.KEYUP:
            if(event.key == pygame.K_UP):
                p1.isUp = 0
            if(event.key == pygame.K_DOWN):
                p1.isDown = 0
            if(event.key == pygame.K_LEFT):
                p1.isLeft = 0
            if(event.key == pygame.K_RIGHT):
                p1.isRight = 0
            if(event.key == pygame.K_BACKSPACE):
                isHoldBackspace = False
    [i.updateCoordinate() for i in GO.Players]
    [i.fly() for i in GO.Bullets if i.isFired is True]
    [GO.Bullets.remove(i) for i in GO.Bullets if(i.isFired is True and i.isOutOfScreen())]
    GO.CollisionDetection()
    # 暴露在main loop的setTimeout記得在TimerFlags加一個True
    GO.setTimeout(lambda: print('setTimeout 5s'), 5000, 0)
    if(isHoldBackspace and pygame.time.get_ticks() - HoldBackspaceTick >= 400):
        p1.input = p1.input[:-1]
        print(p1.input)

    
    ## 背景移動
    # bg.move((-5, 0))
    # bg2.move((-5, 0))
    # if(bg.position[0] + bg.Rect.right <= 0):
    #     bg.moveto((1280, 0))
    # if(bg2.position[0] + bg2.Rect.right <= 0):
    #     bg2.moveto((1280, 0))
    ## 執行延時任務
    [i.exec() for i in GO.Timers]
    ## 圖層渲染
    [i.blit() for i in GO.Backgrounds]
    [i.blit() for i in GO.Players]
    [i.blit() for i in GO.Monsters]
    [i.blit() for i in GO.Bullets if i.isFired is True]
    pygame.display.update()
pygame.quit() 