import pygame
import pygame.font as Pyfont
import os
import random
import math
#角色子彈動畫
#角色射擊動作
#勝利 落敗畫面
#1 blit per frame

def TextAttributes(i):
    global TextWidth, TextTop, TextBottom, TextHeight, TextRight, TextLeft_x, TextLeft_y
    j = Text.index(i) #j = 那個字的index
    #---------------------------------------------------#
    #text的rect.top rect.bottom怪怪的，只好手動調整每個數值#
    #---------------------------------------------------#
    TextWidth = i.get_rect()
    TextWidth = TextWidth.width
    TextTop = TextPosition[j][1] + 5
    TextBottom = TextPosition[j][1] + 20
    TextHeight = TextBottom - TextTop
    TextRight = TextPosition[j][0] + TextWidth
    TextLeft_x = TextPosition[j][0]
    TextLeft_y = TextPosition[j][1]
    #---------------------------------------------------#
    return j


#文字隨機出和隨機角度
def randomWordsAngle():
    randomText.insert(0, random.choice(words))
    Text.insert(0, Font.render(randomText[0], True, (255,255,255))) #在Text List插入隨機的字到index 0
    Text_dy.insert(0, random.randint(-2,2)) #Text_dy -2~2 隨機 插入index 0
    print(randomText)
    TextPosition.insert(0, monsterCenter.copy()) #Text位置 = monster位置
    #修正文字到嘴巴的位置
    TextPosition[0][0] -= 55
    TextPosition[0][1] += 15

#比較打對哪個字的函式
def compare():
    global monsterHP, heroHP, monsterHPflag, playerTextColorFlag
    flag_success = False
    monsterHPflag = flag_success
    playerTextColorFlag = flag_success
    IsItPassedIF = 0
    for i in randomText:
        if(playerInput == i): #成功打入一樣的字母
            flag_success = True
            monsterHPflag = flag_success
            playerTextColorFlag = flag_success
            j = randomText.index(i)
            removeNum = removeText(j,0)
            monsterHP -= removeNum*5 #消一個monster扣5HP
            heroHP += removeNum*5 #消一個hero加5HP
            if(heroHP > heroHP_origin):
                heroHP = heroHP_origin
            if(monsterHP < 0): #HP不能低於0
                monsterHP = 0
            print(removeNum)
            print('你打對',playerInput,'了')
            print(monsterHP)
            IsItPassedIF += 1
    if(not flag_success):#沒打對的話
        monsterHP += 5 #monster加血
        if(monsterHP > monsterHP_origin):
            monsterHP = monsterHP_origin

#專門刪除List內的字
def removeText(j,mode): #j=字的index mode=0畫面上全消 mode=1只消一個
    Count = 0
    i = randomText[j]
    while(i in randomText):
        if(mode == 0):
            j = randomText.index(i)
        del Text[j]
        del randomText[j]
        del Text_dy[j]
        del TextPosition[j]
        if(mode == 1):
            break  
        Count += 1
    if(mode == 0):
        return Count

#nonPygame side
path = os.path.split(os.path.abspath(__file__))[0] #遊戲資料夾位址
f = open(path + '/dictionary.txt','r') #開啟字典
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
resolution = [1280, 768]
screen = pygame.display.set_mode(resolution)

#background
background = pygame.Surface(screen.get_size())
background = pygame.image.load(os.path.join(path, 'background.png'))
background = background.convert()
background_dx = 5
backgroundStart = 0

background02 = pygame.Surface(screen.get_size())
background02 = pygame.image.load(os.path.join(path, 'background.png'))
background02 = background02.convert()
backgroundStart02 = backgroundStart + 1492

#words
fontLocation = Pyfont.match_font('Minecraft Regular')
Font = Pyfont.Font(fontLocation, 20)
playerFont = Pyfont.Font(fontLocation, 100)
playerInput = ''
Alpha_origin = 175 #玩家輸入字的透明度(255不透明)
Alpha = Alpha_origin
playerText = Font.render(playerInput, True, (255,0,0))
playerTextRect = playerText.get_rect()
Text_dx = -2 #文字位移X軸
TextPosition = []
for i in range(10):
    TextPosition.append(2*[0])


#hero picture
hero = pygame.image.load(os.path.join(path, 'hero01.png'))
hero = hero.convert_alpha()
hero = pygame.transform.scale(hero, (150,120)) #hero大小調整
heroRect = hero.get_rect()
heroHeight = heroRect.height
heroWidth = heroRect.width
#hero picture_b
heroChange = pygame.image.load(os.path.join(path, 'hero01_b.png'))
herorChange = heroChange.convert_alpha()
heroChange = pygame.transform.scale(heroChange, (150,120)) #hero大小調整
#heroPosition
heroCenter = [math.floor(resolution[0]/3), math.floor(resolution[1]/2)]
moveSpeed = 10 #按一下移動多少
hero_dy = moveSpeed 
hero_dx = moveSpeed
#player's bullet

#Heor health
heroHP_origin = 500
heroHP = heroHP_origin
heroHPheight = 10
heroHPwidth = 125

#monsters picture
monster = pygame.image.load(os.path.join(path, 'monster01.png'))
monster = monster.convert_alpha()
monster = pygame.transform.scale(monster, (200,180)) #monster大小調整
monsterRect = monster.get_rect()
monsterHeight = monsterRect.height
monsterWidth = monsterRect.width
monsterPic = monster
#monsters pictrue_b
monsterChange = pygame.image.load(os.path.join(path, 'monster01_b.png'))
monsterChange = monsterChange.convert_alpha()
monsterChange = pygame.transform.scale(monsterChange, (200,180)) #monster大小調整
#monsterPosition
monsterCenter = [math.floor(resolution[0]-monsterWidth/2), math.floor(resolution[1]/2)]
monster_dy = 3 #移動速度

#monsters HP
monsterHP_origin = 100
monsterHP = monsterHP_origin
monsterHPheight = 20
monsterHPwidth = 180

#game clock
clock = pygame.time.Clock()
lastTick = 0
#hitboxShift
leftShift = 25
rightShift = -72
topShift = 17
widthShift = rightShift - leftShift
heightShift = -topShift

#Loop
running = True
monsterMode = True
Count01 = 0 #monster的counter
Count02 = 0 #Text的counter
Count03 = 0 #Enter按下後動畫的counter
Count04 = 0 #Back壓著的counter
Count05 = 0 #monster血變紅的counter
randomWordsAngle() #先產生一個字
monsterHPcolor = [255,255,255]
monsterHPflag = False

holdUP = False
holdDOWN = False
holdLEFT = False
holdRIGHT = False
holdBACK = False
flag_success = False
enterBool = False
while running:
    clock.tick(30) #fps
    #輸入事件新增位置
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                compare() #比較有沒有打一樣的
                enterBool = True
                inputCache = playerInput
                playerInput = ''
            elif event.key == pygame.K_ESCAPE:
                enterBool = False
                playerInput = '' #清空字
            elif event.key == pygame.K_BACKSPACE:
                holdBACK = True
                enterBool = False
                playerInput = playerInput[:-1]
            elif event.key == pygame.K_UP:
                holdUP = True
            elif event.key == pygame.K_DOWN:
                holdDOWN = True
            elif event.key == pygame.K_LEFT:
                holdLEFT = True
            elif event.key == pygame.K_RIGHT:
                holdRIGHT = True
            else:
                playerInput += event.unicode
                enterBool = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                holdUP = False
            elif event.key == pygame.K_DOWN:
                holdDOWN = False
            elif event.key == pygame.K_LEFT:
                holdLEFT = False
            elif event.key == pygame.K_RIGHT:
                holdRIGHT = False
            elif event.key == pygame.K_BACKSPACE:
                holdBACK = False
        if event.type == pygame.QUIT:
            running = False
    #時間觸發事件(每100ms觸發一次)
    if (pygame.time.get_ticks() - lastTick >= 100):
        if(Count01 == 5): #觸發換monster圖片
            monsterMode = not monsterMode
            Count01 = 0
        if(Count02 == 15): #觸發Text產生
            randomWordsAngle()
            Count02 = 0
        if(Count04 == 1):
            if(holdBACK):
                playerInput = playerInput[:-1] #刪一個字
            Count04 = 0
        if(monsterHPflag):
            Count05 += 1
            if(Count05 == 4):
                monsterHPcolor = [255,255,255]
                monsterHPflag = False
                Count05 = 0
        lastTick = pygame.time.get_ticks()
        Count01 += 1
        Count02 += 1
        Count03 += 1
        Count04 += 1

    #-------兩個背景輪流頂替---------#
    backgroundStart -= background_dx
    backgroundStart02 = backgroundStart + 1492
    screen.blit(background, (backgroundStart,0))
    screen.blit(background02, (backgroundStart02,0)) #背景在這
    if(backgroundStart <= -1492):
        flag = backgroundStart
        backgroundStart = backgroundStart02
        backgroundStart02 = flag
    #------------------------------#
    #----------按著方向鍵的動作------------#
    if(holdUP):
        if(heroRect.top>=0):
            heroCenter[1] -= hero_dy
    if(holdDOWN):
        if(heroRect.bottom <= screen.get_height()):
            heroCenter[1] += hero_dy
    if(holdLEFT):
        if(heroRect.left>=0):
            heroCenter[0] -= hero_dx
    if(holdRIGHT):
        if(heroRect.right<=1024):
            heroCenter[0] += hero_dx
    if(holdBACK):
        pass #刪一個字
    #--------------------------------------#
    #--------------按下enter的動畫-----------------#
    if(enterBool):
        Alpha -= 15 #淡出多快(越高越快)
        multiply = 1.08 #放大多快(越高越快)
        playerText_enter = playerText
        playerTextRect.width = math.floor(playerTextRect.width * multiply)
        playerTextRect.height = math.floor(playerTextRect.height * multiply)
        scaleVal = [playerTextRect.width, playerTextRect.height]
        if(playerTextColorFlag):
            playerText_enter = Font.render(inputCache, 0, (0,150,180)) #答對的顏色
        playerText_enter.set_alpha(Alpha)
        if(playerTextRect.width <= resolution[0] and playerTextRect.height <= resolution[1]):
            playerText_enter = pygame.transform.scale(playerText_enter, scaleVal)
            playerText_enterRect = playerText_enter.get_rect()
    if(Alpha <= 0):
        enterBool = False
        Alpha = Alpha_origin
    #----------------------------------------------#
    #----------中間顯示打甚麼字的Blit---------------#
    if(not enterBool):
        playerText = playerFont.render(playerInput, 0, (255,0,0))
        playerText.set_alpha(Alpha_origin)
        playerTextRect = playerText.get_rect()
        X = math.floor(resolution[0]/2-playerTextRect.width/2)
        Y = math.floor(resolution[1]/2-playerTextRect.height/2)
        screen.blit(playerText, (X, Y))
    if(enterBool):
        playerText_enterRect = playerText_enter.get_rect()
        X = math.floor(resolution[0]/2-playerTextRect.width/2)
        Y = math.floor(resolution[1]/2-playerTextRect.height/2)
        screen.blit(playerText_enter, (X, Y))
    #-----------------------------------------------#
    #----------monsterBilt-----------#
    #monster 移動&反彈
    monsterCenter[1] += monster_dy
    monsterRect.center = (monsterCenter)
    if (monsterRect.top<=0 or monsterRect.bottom>=screen.get_height()):
        monster_dy *= -1
    if(monsterMode): #monster圖1
        monsterPic = monster
    else: #monster圖2
        monsterPic = monsterChange
    screen.blit(monsterPic,monsterRect.topleft)
    #--------------------------------#
    #---------------------------------和文字有關的--------------------------------#
    HIT = False
    if(len(Text) != 0): 
        #Text movement and blit(用掃描的概念)
        for i in Text: #i = 掃到的字
            j = TextAttributes(i)
            #字反彈
            if (TextTop <= 0 or TextBottom >= screen.get_height()):
                Text_dy[j] *= -1
            #字移動
            TextPosition[j][0] += Text_dx
            TextPosition[j][1] += Text_dy[j]
            #碰到hero就扣血 monster加血
            Condition0 = (TextLeft_x <= heroRect.right + rightShift and TextRight >= heroRect.right + rightShift) #字在hero右邊
            Condition1 = (TextLeft_x <= heroRect.left + leftShift and TextRight >= heroRect.left + leftShift) #字在hero左邊
            Condition2 = (TextLeft_x >= heroRect.left + leftShift and TextRight <= heroRect.right + rightShift) #字在hero右邊和左邊之間
            Condition3 = (TextTop <= heroRect.bottom and TextBottom >= heroRect.bottom) #字在hero下面
            Condition4 = (TextBottom >= heroRect.top + topShift and TextTop <= heroRect.top + topShift) #字在hero上面
            Condition5 = (TextBottom <= heroRect.bottom and TextTop >= heroRect.top + topShift) #字在hero上面和下面之間
            if((Condition0 or Condition1 or Condition2) and (Condition3 or Condition4 or Condition5)): #碰撞條件
                HIT = True
            #字超過螢幕左邊就刪掉
            if (TextRight <= 0):
                removeText(j,1)
            '''
            #Text的Hitbox
            RECTCOORD = [TextLeft_x, TextTop, TextWidth, TextHeight]
            TEXThitbox = pygame.Rect(RECTCOORD)
            pygame.draw.rect(screen, (0,0,0), TEXThitbox, 3)
            '''
            screen.blit(i, (TextPosition[j][0], TextPosition[j][1]))
    #------------------------------------------------------------------------------# 
    #HeroBilt   
    '''
    #HERO的Hitbox
    RECTCOORD = [heroRect.left + leftShift, heroRect.top + topShift, heroWidth + widthShift , heroHeight + heightShift]
    HEROhitbox = pygame.Rect(RECTCOORD)
    pygame.draw.rect(screen, (0,0,0), HEROhitbox, 3)
    '''
    heroRect.center = (heroCenter)
    screen.blit(hero,heroRect.topleft) #hero顯示
    #--------------------血條顯示----------------------#
    heroHPcolor = [255,255,255]
    #-----------被字撞到-----------#
    if(HIT):
        heroHP -= 5 #扣的血量
        heroHPcolor = [255,0,0]
        if(heroHP <= 0):
            heroHP = 0
        print('HIT')
    #-----------------------------#
    if(monsterHPflag):
        monsterHPcolor = [255,0,0]
    #HeroHP裡面
    LEFT = heroRect.left
    TOP = heroRect.top - 17
    RECTCOORD = [LEFT, TOP, math.floor((heroHPwidth+4)*heroHP/heroHP_origin), heroHPheight]
    heroHPrect2 = pygame.Rect(RECTCOORD)
    #HeroHP外框
    LEFT = heroRect.left
    TOP = heroRect.top - 20
    RECTCOORD = [LEFT, TOP, heroHPwidth+6, heroHPheight+6]
    heroHPrect1 = pygame.Rect(RECTCOORD)
    #先印裡面再印外框
    pygame.draw.rect(screen, heroHPcolor, heroHPrect2, 0)
    pygame.draw.rect(screen, (0,0,0), heroHPrect1, 3)
    #monsterHP裡面
    LEFT = monsterRect.left + 7
    TOP = monsterRect.top - 17
    RECTCOORD = [LEFT, TOP, math.floor((monsterHPwidth+4)*monsterHP/monsterHP_origin), monsterHPheight]
    monsterHPrect2 = pygame.Rect(RECTCOORD)
    #monsterHP外框
    LEFT = monsterRect.left + 7
    TOP = monsterRect.top - 20
    RECTCOORD = [LEFT, TOP, monsterHPwidth+6, monsterHPheight+6]
    monsterHPrect1 = pygame.Rect(RECTCOORD)
    #先印裡面再印外框
    pygame.draw.rect(screen, monsterHPcolor, monsterHPrect2, 0)
    pygame.draw.rect(screen, (0,0,0), monsterHPrect1, 3)
    #-----------------------------------------------------#

    pygame.display.update()
    if (len(Text) > 40): #字的數量超過40就pop掉一個
        Text.pop()
        Text_dy.pop()
        TextPosition.pop()
pygame.font.quit()
pygame.quit()
