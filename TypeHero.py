import pygame
import pygame.font as Pyfont
import os
import random

#Todo 字跑出的時機
#控制角色移動(上下)
#角色打對字射出子彈(自動瞄準)
#角色被字碰到會扣血
#魔王的血量
#同時跑出畫面外的字會有問題 吧?

#文字隨機出和隨機角度
def randomWordsAngle():
    randomText.insert(0, random.choice(words))
    Text.insert(0, Font.render(randomText[0], True, (0,0,0))) #在Text List插入隨機的字到index 0
    Text_dy.insert(0, random.randint(-2,2)) #Text_dy -2~2 隨機 插入index 0

#比較打對哪個字的函式
class removeText():
    def __init__(self, name):
    self.name = name
a = Animal("dog")  #建立一個名叫dog的Animal實體(物件)
print(a.name)

def compare():
    global monsterHP
    for i in randomText:
        if(playerInput == i): #成功打入一樣的字母
            
            removeNum = removeText(i,0)
            monsterHP -= removeNum*5
            print('你打對',playerInput,'了')
            print(monsterHP)
        else: #沒打對的話
            pass

#專門刪除List內的字
def removeText(j,mode): #j=字的index mode=0畫面上全消 mode=1只消一個
    Count = 0
    if(mode = 0):
        while(i in randomText):
            j = randomText.index(i)
            Text.remove(Text[j])
            randomText.remove(i)
            Text_dy.remove(Text_dy[j])
            TextPosition.remove(TextPosition[j])
            if(mode==1):
                break
            Count += 1
        return Count
    if(mode = 1):
        

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
randomText = [] #真的字的List

#init
pygame.init()
pygame.font.init()
pygame.display.set_caption("Type Hero")
resolution = (1024, 768)
screen = pygame.display.set_mode(resolution)



#background
background = pygame.Surface(screen.get_size())
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

#monsters HP
monsterHP = 100
HP = pygame.Surface((200,20))
HP.fill((0,0,0))
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
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        #玩家輸入
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    compare() #比較有沒有打一樣的
                    playerInput = ''
                elif event.key == pygame.K_BACKSPACE:
                    playerInput = playerInput[:-1]
                else:
                    playerInput += event.unicode
        
    screen.blit(background, (0,0)) #背景在這
    
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
        if(Count02 == 20): #集滿十次觸發Text產生
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
            #------------------------------------------#
            #text的rect.top rect.bottom怪怪的，只好這樣用#
            #------------------------------------------#
            TextWidth = i.get_rect()
            TextWidth = TextWidth.width
            TextTop = TextPosition[j][1]
            TextBottom = TextPosition[j][1] + 20
            TextRight = TextPosition[j][0] + TextWidth
            if (TextTop <= 0 or TextBottom >= screen.get_height()):  #字反彈
                Text_dy[j] *= -1
            TextPosition[j][0] += Text_dx
            TextPosition[j][1] += Text_dy[j]
            screen.blit(i, (TextPosition[j][0], TextPosition[j][1])) #字移動
            if (TextRight <= 0):
                print(randomText)
                print(randomText[j],'被丟棄了')
                removeText(randomText[j],1)
                print(randomText)
    #monsterHPbar
    screen.blit(HP, (monsterRect.left + 55, monsterRect.top - 20))

    pygame.display.update()
    if (len(Text) > 10): #字的數量超過10就pop掉一個
        Text.pop()
        Text_dy.pop()
        TextPosition.pop()
pygame.font.quit()
pygame.quit()
