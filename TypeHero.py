# todo: 
# 死掉的角色從list刪除，飛出畫面的、停止的子彈從list刪除
# GJK碰撞實作
# 根據狀態更改角色外觀
# 碰撞一次只會造成一次傷害
# 輸入字顯示在畫面上
# Word子彈的顯示
# 打入正確的字後、存子彈
# 血量顯示

###### 多人遊戲的物件是從server獲取Word Player Monster物件
# tips: 要建screen、loop中更新screen
#       要建Surface、Surface才能用get_rect、取到的rect才能移動他，圖片也是種Surface
#       pygame.draw可以畫圖形在Surface上，但是不能取rect，畫上去就是死的，要透過移動Surface來移動他
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
bg_img = GO.Img('asset/background.png', (1280, 768))
# 遊戲物件
p1 = GO.Alien('zel', GO.Team.TeamA, (120, 360), (1, 0))
m1 = GO.Bacteria('Baekk', (1000, 360), (-1, 0))
m1 = GO.Bacteria('Baekk2', (1200, 360), (-1, 0))
bg = GO.Background(bg_img, (0, 0))
bg2 = GO.Background(bg_img, (1280, 0))
GO.Can_hurt(attacker=GO.Bullets, victim=GO.Players)
GO.Can_hurt(attacker=GO.Bullets, victim=GO.Monsters)
GO.Can_hurt(attacker=GO.Words, victim=GO.Players)
GO.Can_hurt(attacker=GO.Monsters, victim=GO.Players)



lastTick = 0
running = True
while running:
    pygame.time.Clock().tick(60)
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
                p1.save_round(GO.IceBall())
            if(event.key == pygame.K_RETURN):
                p1.shoot()
            if(event.key == pygame.K_r):
                for i in GO.Monsters:
                    i.hp = 10000
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
    GO.collision_dmg()
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
    [i.blit() for i in GO.Players]
    [i.blit() for i in GO.Monsters]
    [i.blit() for i in GO.Bullets if i.isFired is True]
    pygame.display.update()
pygame.quit() 