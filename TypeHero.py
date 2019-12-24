import pygame
import pygame.font as Pyfont
import os
import random

#Todo 字跑出的時機
#Todo 鍵盤輸入消字

#文字隨機出和隨機角度
def randomWordsAngle():
    Text.insert(0, Font.render(random.choice(words), True, (0,0,0))) #在Text List插入隨機的字到index 0
    Text_dy.insert(0, random.randint(-2,2)) #Text_dy -2~2 隨機 插入index 0

def compare():
    for i in Text:
        if(playerInput == i):
            print(playerInput)

#nonPygame side
path = os.path.split(os.path.abspath(__file__))[0] #遊戲資料夾位址
f = open(path + '\dictionary.txt','r') #開啟字典
Dict = f.read()
words = Dict.splitlines() #字的List
wordsNum = len(words) #字的數量
for i in range(wordsNum):
    words[i] = words[i].strip('\'')
Text = [] #準備給遊戲渲染的字串list
Text_dy = [] #字移動的dy List

#init
pygame.init()
pygame.font.init()
pygame.display.set_caption("Type Hero")
resolution = (1024, 768)
screen = pygame.display.set_mode(resolution)
background = pygame.Surface(screen.get_size())
#pygame.event.pump()
#pygame.event.set_blocked(pygame.MOUSEMOTION)



#background
background.fill((125,125,125))
background = background.convert()

#words
fontLocation = Pyfont.match_font('Minecraft Regular')
Font = Pyfont.Font(fontLocation, 20)
Text_dx = -2
TextPosition = []
for i in range(10):
    TextPosition.append(2*[0])
print(TextPosition)

#player picture

#player's bullet

#player health

#monsters picture
monster = pygame.image.load(os.path.join(path, 'monster01.png'))
monster = monster.convert_alpha()
monsterRect = monster.get_rect()
monsterHeight = monsterRect.height
monsterWidth = monsterRect.width
#monsters pictrue_b
monsterChange = pygame.image.load(os.path.join(path, 'monster01_b.png'))
monsterChange = monsterChange.convert_alpha()
#monsterPosition
monsterCenter = [resolution[0]-monsterWidth/2, resolution[1]/2]
monster_dy = 3 #移動速度

#monsters health

#game clock
clock = pygame.time.Clock()
lastTick = 0

#Loop

running = True
monsterMode = True
Count01 = 0 #monster的counter
Count02 = 0 #Text的counter
randomWordsAngle() #先產生一個字
TextPosition.insert(0, monsterCenter.copy()) #Text位置 = monster位置
TextPosition[0][0] -= 50
playerInput = ''
while running:
    clock.tick(30) #fps
    pygame.key.start_text_input()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        #玩家輸入
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    
                    compare()
                    playerInput = ''
                elif event.key == pygame.K_BACKSPACE:
                    playerInput = playerInput[:-1]
                else:
                    playerInput += event.unicode
        
    screen.blit(background, (0,0))
    
    #monster 移動&反彈
    monsterCenter[1] += monster_dy
    monsterRect.center = (monsterCenter)
    if (monsterRect.top<=0 or monsterRect.bottom>=screen.get_height()):
        monster_dy *= -1
    
    #每100ms觸發一次
    if (pygame.time.get_ticks() - lastTick >= 100):
        if(Count01 == 5): #集滿五次觸發換monster圖片
            monsterMode = not monsterMode
            Count01 = 0
        if(Count02 == 50): #集滿十次觸發Text產生
            randomWordsAngle()
            j = len(Text)
            TextPosition.insert(0, monsterCenter.copy()) #Text位置 = monster位置
            Count02 = 0
            #修正文字到嘴巴的位置
            TextPosition[0][0] -= 55
            TextPosition[0][1] += 20
        lastTick = pygame.time.get_ticks()
        Count01 += 1
        Count02 += 1
    if(monsterMode): #monster圖1
        screen.blit(monster,monsterRect.topleft)
    else: #monster圖2
        screen.blit(monsterChange,monsterRect.topleft)
    if(len(Text) != 0): #字
        #Text movement and blit(掃描的概念)
        for i in Text: #i = 掃到的字
            j = Text.index(i) #j = 那個字的index
            TextTop = TextPosition[j][1]
            TextBottom = TextPosition[j][1] + 20
            if (TextTop <= 0 or TextBottom >= screen.get_height()):  #字反彈
                Text_dy[j] *= -1
            TextPosition[j][0] += Text_dx
            TextPosition[j][1] += Text_dy[j]
            screen.blit(i, (TextPosition[j][0], TextPosition[j][1])) #字移動
        

    pygame.display.update()
    if (len(Text) > 10): #字的數量超過10就pop掉一個
        Text.pop()
        Text_dy.pop()
        TextPosition.pop()
pygame.font.quit()
pygame.quit()
