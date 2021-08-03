import pygame
import math
import GameObject as GO
#比較打對哪個字的函式
def isCorrect(player):
    if(player.input in GO.Words):
        return True
    else:
        return False
#專門刪除List內的字
def delWord(word):
    while(word in GO.Words):
        GO.Words.remove(word)
# 跑出畫面外的元素刪除
def delOutsideElement():
    pass

# 圖片資訊封裝
p1_img = GO.Img('asset/player01.png', (150,120))
bg_img = GO.Img('asset/background.png', (1280, 768))
# 遊戲物件
p1 = GO.Player(p1_img, 'zel', GO.Team.TeamA, [640, 360], (1, 0))
bg = GO.Background(bg_img, [0, 0])
bg2 = GO.Background(bg_img, [1280, 0])


lastTick = 0
while True:
    pygame.time.Clock().tick(60)
    for event in pygame.event.get():
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
                p1.save_round(GO.NormalBall(p1))
                print(len(p1.round), '顆子彈')
            if(event.key == pygame.K_RETURN):
                p1.shoot()
        if event.type == pygame.KEYUP:
            if(event.key == pygame.K_UP):
                p1.isUp = 0
            if(event.key == pygame.K_DOWN):
                p1.isDown = 0
            if(event.key == pygame.K_LEFT):
                p1.isLeft = 0
            if(event.key == pygame.K_RIGHT):
                p1.isRight = 0
    for i in GO.Players:
        i.updateCoordinate()
    [i.fly() for i in GO.Bullets if i.isFired is True]
    ## 延時性任務
    # if(pygame.time.get_ticks() - lastTick >= 5000):
    #     lastTick = pygame.time.get_ticks()
    ## 背景移動
    # bg.move((-5, 0))
    # bg2.move((-5, 0))
    # if(bg.position[0] + bg.Rect.right <= 0):
    #     bg.moveto((1280, 0))
    # if(bg2.position[0] + bg2.Rect.right <= 0):
    #     bg2.moveto((1280, 0))
    ## 圖層渲染
    [i.blit() for i in GO.Backgrounds]
    [i.blit() for i in GO.Bullets if i.isFired is True]
    [i.blit() for i in GO.Players]
    pygame.display.update()