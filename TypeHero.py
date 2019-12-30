import pygame
import pygame.font as Pyfont
import os
import random
import math
#1 blit per frame
#monster每隔一段時間變化移動方式 OK
#按下enter怪獸會跑過來
#時間內要擊敗怪獸
#同時被兩個字撞到的傷害不一樣
#按左右自動轉向 (?)
#轉向hitbox位置不變 OK
#特殊模式：已經打過的字傷害較低
def gameReset():
    global gameStart, gameOver, running, monsterMode, heroBulletFlag, alphaSolidHold, HPchangeColorHold01, HPchangeColorHold02\
        , Count01, Count02, Count03, Count04, Count05, Count_bullet, alphaSolidFlag, HPchangeColor, timeTotal\
            , holdUP, holdDOWN, holdLEFT, holdRIGHT, holdBACK, flag_success, enterBool, enterBool02, monster_dx, monster_dy\
                , needMessage, heroHP, monsterHP, heroCenter, monsterCenter, reset, hero_dx, hero_dy, playerInput
    #Before Loop
    gameStart = True #遊戲開始
    gameOver = False #遊戲結束
    monsterMode = True #monster哪一張圖片
    heroBulletFlag = [] #子彈一開始沒出現
    Count01 = 0 #monster換圖片的counter
    Count02 = 0 #Text的counter
    Count03 = 0 #Enter按下後動畫的counter
    Count04 = 0 #Back壓著的counter
    Count05 = 0 #monster血變紅的counter
    holdUP = False
    holdDOWN = False
    holdLEFT = False
    holdRIGHT = False
    holdBACK = False
    flag_success = False #是否有打對
    alphaSolidFlag = 0 #打錯背景紅一下的訊號，1 = 有打對 , 2 = 打錯
    HPchangeColor = 0 #1 = 打對 hero血條變綠一下 2 = 打錯 monster血條變綠
    alphaSolidHold = False #打錯背景紅一下的保持Flag
    HPchangeColorHold01 = False #打對hero血條變綠一下的保持Flag
    HPchangeColorHold02 = False #打錯monster血條變綠一下的保持Flag
    enterBool = False #是否按下enter
    enterBool02 =False 
    needMessage = False #需要遊戲訊息
    reset = False
    playerInput = ''
    heroHP = heroHP_origin
    monsterHP = monsterHP_origin
    heroCenter = heroCenter_origin.copy()
    monsterCenter = [math.floor(resolution[0]*5/6), math.floor(resolution[1]/2)]
    hero_dx = hero_moveSpeed
    hero_dy = hero_moveSpeed
    Count_bullet = 0
    timeTotal = []
    [monster_dx, monster_dy] = randomMonsterAngle()
    hitboxShift()
    Text.clear()
    Text_dx.clear()
    Text_dy.clear()
    TextPosition.clear()
    heroBulletFlag.clear()
    randomText.clear()
    bulletArray.clear()
    bulletCenter_cache.clear()
    heroBulletFlag.clear()
    randomWordsAngle() #先產生一個字
#hitboxShift 讓hitbox更接近玩家想像
def hitboxShift():
    global leftShift, rightShift, topShift, bottomShift, widthShift, heightShift
    if(not changeDirect):
        leftShift = 40
        rightShift = -85
        topShift = 17
        bottomShift = -15
        widthShift = rightShift - leftShift
        heightShift = -topShift - 15
    if(changeDirect):
        leftShift = 85
        rightShift = -40
        topShift = 17
        bottomShift = -15
        widthShift = rightShift - leftShift
        heightShift = -topShift - 15

#文字隨機出和隨機角度
def randomWordsAngle():
    randomText.insert(0, random.choice(wordCollection[Set]))
    Text.insert(0, Font.render(randomText[0], False, (255,255,255))) #在Text List插入隨機的字到index 0
    #依據畫面上有幾個同樣的字顯示字的顏色
    for i in range(len(randomText)):
        TextColor = (255,255,255)
        x = randomText.count(randomText[i])
        if(x == 2):
            TextColor = (130,234,255)
        if(x >= 3):
            TextColor = (255,94,94)
        Text[i] = Font.render(randomText[i], False, (TextColor))
    Text_dx.insert(0, random.randint(-3,3)) #Text_dx m~n 隨機 插入index 0
    Text_dy.insert(0, random.randint(-6,6)) #Text_dy m~n 隨機 插入index 0
    print(randomText)
    TextPosition.insert(0, monsterCenter.copy()) #Text位置 = monster位置
    #修正文字到嘴巴的位置
    TextPosition[0][0] -= 55
    TextPosition[0][1] += 15

def randomMonsterAngle(): #怪獸移動角度、速度 C^2 = A^2 + B^2
    monster_dx = 0
    minSpeed = 50 #最小速度
    maxSpeed = 300 #最大速度
    monster_moveSpeed = random.randint(minSpeed,maxSpeed)
    monster_dx = random.randint(1, math.floor(math.sqrt(monster_moveSpeed))) * random.choice([1, -1])
    monster_dy = monster_moveSpeed - math.pow(monster_dx, 2)
    monster_dy = math.sqrt(monster_dy) * random.choice([1, -1])
    return monster_dx, math.floor(monster_dy)
#比較打對哪個字的函式
def compare():
    global monsterHP, heroHP, playerTextColorFlag, heroBulletFlag, alphaSolidFlag, HPchangeColor, removeNum
    #playerTextColorFlag: 按下enter的訊號旗標，判斷是否打對
    #heroBulletFlag: 按下enter的訊號旗標，判斷是否正在飛
    flag_success = False
    if(playerInput in randomText): #打對
        flag_success = True
        playerTextColorFlag = flag_success #玩家輸入flag=True
        alphaSolidFlag = 1 #打對背景變綠
        HPchangeColor = 1 #打對hero血條變綠
        heroBulletFlag.insert(0, 1) #insert 1到子彈是否正在飛的Flag List
        j = randomText.index(playerInput)
        removeNum = removeText(j,0) #removeNum:一次消的個數
        heroHP += removeNum*5 #每消一個hero加5HP
        if(removeNum == 1):
            bulletPic = bullet
        elif(removeNum == 2):
            bulletPic = bullet02
        elif(removeNum >= 3):
            bulletPic = bullet03
        print(removeNum)
        print('你打對',playerInput,'了')
    if(not flag_success):#沒打對的話
        monsterHP += 5 #monster加血
        bulletPic = null #沒擊中的話 子彈圖案變空的
        playerTextColorFlag = flag_success
        alphaSolidFlag = 2 #打錯背景變紅
        HPchangeColor = 2 #沒打對怪血條變綠
        heroBulletFlag.insert(0, 0)
    bulletArray.insert(0, bulletPic) #加一顆子彈圖片到Array
    bulletCenter_cache.insert(0, bulletCenter) #加子彈位置到Array

#專門刪除List內的字
def removeText(j,mode): #j=字的index mode=0畫面上全消 mode=1只消一個
    Count = 0
    i = randomText[j]
    while(i in randomText):
        if(mode == 0):
            j = randomText.index(i)
        del Text[j]
        del randomText[j]
        del Text_dx[j]
        del Text_dy[j]
        del TextPosition[j]
        if(mode == 1):
            break  
        Count += 1
    if(mode == 0):
        return Count

HITBOX = True
#nonPygame side
consolePass = True
path = os.path.split(os.path.abspath(__file__))[0] #遊戲資料夾位址
f = open(path + '/dictionary.txt','r') #開啟字典
word_cache = f.read()
f.close()
wordCollection = [[]]
word_cache = word_cache.splitlines() #字的List
wordsNum = len(word_cache) #字的數量
k = 0
for i in range(wordsNum):
    word_cache[i] = word_cache[i].strip('\'')
    if(word_cache[i] == '#DIVIDER#'):
        wordCollection += [[]]
        k += 1
    else:
        wordCollection[k].append(word_cache[i])
os.system('cls')
while(True):
    print('輸入要玩的文字組合：',end='')
    for i in range(len(wordCollection)):
        wordCollection[i][0] = wordCollection[i][0].strip('$')
        print('(',i,') ', sep='', end='') 
        print(wordCollection[i][0],'',end='')
    print(': ', end='')
    try:
        Set = int(input())
    except(ValueError):
        print('請輸入數字')
    except(EOFError): #輸入ctrl+z or ctrl+c
        consolePass = False
        break
    else:
        if(Set > len(wordCollection) - 1):
            print('請輸入選項內的數字')
        else:
            break
for i in wordCollection:
    i.pop(0)
while(True and consolePass):
    print('選擇難度:(0)簡單 (1)普通 (2)緊張 (3)刺激 (4)怕: ',end = '')
    try:
        Difficult = int(input())
    except(ValueError):
        print('請輸入數字')
    except(EOFError): #輸入ctrl+z or ctrl+c
        consolePass = False
        break
    else:
        if(Difficult > 4):
            print('請輸入選項內的數字')
        else:
            break
Text = [] #準備給遊戲渲染的字串list
Text_dx = []
Text_dy = [] #字移動的dy List
randomText = [] #真的字的List

#init
pygame.init()
pygame.font.init()
resolution = [1280, 768]
pygame.display.set_caption("Type Hero")
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
alphaSolid = pygame.Surface(screen.get_size()) #背景閃一下半透明顏色的Surface

#words
fontLocation = Pyfont.match_font('Minecraft Regular')
FontSize = 30
Font = Pyfont.Font(fontLocation, FontSize)
playerFont = Pyfont.Font(fontLocation, 100)
playerInput = ''
Alpha_origin = 175 #玩家輸入字的透明度(255不透明)
Alpha = Alpha_origin
playerText = Font.render(playerInput, True, (255,0,0))
playerTextRect = playerText.get_rect()
TextPosition = []

#hero picture
hero = pygame.image.load(os.path.join(path, 'hero01.png'))
hero = hero.convert_alpha()
hero = pygame.transform.scale(hero, (150,120)) #hero大小調整
heroRect = hero.get_rect()
heroHeight = heroRect.height
heroWidth = heroRect.width
heroPic = hero
#hero picture_b
heroChange = pygame.image.load(os.path.join(path, 'hero01_b.png'))
herorChange = heroChange.convert_alpha()
heroChange = pygame.transform.scale(heroChange, (150,120)) #hero大小調整
#heroPosition
hero_moveSpeed = 10 #按一下移動多少
heroCenter_origin = [math.floor(resolution[0]/7), math.floor(resolution[1]/2)]
hero_dy = hero_moveSpeed 
hero_dx = hero_moveSpeed
#hero's bullet
bulletArray = [] #存三種bulletPic
bulletRect = [] #存三個bullet矩形(最後指定位置用)
bulletCenter_cache = [] #存正在飛的bullet位置
bullet = pygame.image.load(os.path.join(path, 'hero_bullet01.png'))
bullet = bullet.convert_alpha()
bullet = pygame.transform.scale(bullet, (60,50)) #bullet大小調整
bulletPic = bullet
for i in range(15): #弄4個一樣的Rect
    bulletRect.append(bullet.get_rect())
#hero's bullet02
bullet02 = pygame.image.load(os.path.join(path, 'hero_bullet02.png'))
bullet02 = bullet02.convert_alpha()
bullet02 = pygame.transform.scale(bullet02, (100,56)) #bullet02大小調整
bullet02Rect = bullet02.get_rect()
bullet02Height = bullet02Rect.height
bullet02Width = bullet02Rect.width
#hero's bullet03
bullet03 = pygame.image.load(os.path.join(path, 'hero_bullet03.png'))
bullet03 = bullet03.convert_alpha()
bullet03 = pygame.transform.scale(bullet03, (100,56)) #bullet03大小調整
bullet03Rect = bullet03.get_rect()
bullet03Height = bullet03Rect.height
bullet03Width = bullet03Rect.width
#null bullet
null = pygame.image.load(os.path.join(path, 'null.png'))
null = null.convert_alpha()
#Hero health
heroHP_origin = 500
heroHP = heroHP_origin
heroHPheight = 10
heroHPwidth = 125

#monsters picture
monster = pygame.image.load(os.path.join(path, 'monster02.png'))
monster = monster.convert_alpha()
monster = pygame.transform.scale(monster, (200,180)) #monster大小調整
monsterRect = monster.get_rect()
monsterHeight = monsterRect.height
monsterWidth = monsterRect.width
monsterPic = monster
#monsters pictrue_b
monsterChange = pygame.image.load(os.path.join(path, 'monster02_b.png'))
monsterChange = monsterChange.convert_alpha()
monsterChange = pygame.transform.scale(monsterChange, (200,180)) #monster大小調整
#monsterPosition
monster_moveSpeed = 5 #移動速度
monster_dy = monster_moveSpeed
monster_dx = monster_moveSpeed
#monsters HP
monsterHP_origin = 100
monsterHP = monsterHP_origin
monsterHPheight = 20
monsterHPwidth = 180

#game clock
clock = pygame.time.Clock()
lastTick = 0

#BeforeLoop
changeDirect = False #角色換方向旗標
running = True #視窗執行中
if(consolePass): #console端停止就不呼叫Reset
    gameReset()
#Loop
while running and consolePass: #console端停止就不進去
    clock.tick(30) #fps
    #輸入事件新增位置
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if(gameStart):
                gameReset()
                gameStart = False
                needMessage = False
            elif(gameOver and event.key == pygame.K_RETURN):
                gameOver = False
                needMessage = False
                reset = True
            elif(monsterHP == 0):
                if event.key == pygame.K_UP:
                    holdUP = True
                elif event.key == pygame.K_DOWN:
                    holdDOWN = True
                elif event.key == pygame.K_LEFT:
                    holdLEFT = True
                elif event.key == pygame.K_RIGHT:
                    holdRIGHT = True
                elif event.key == (pygame.K_LCTRL):
                    if(changeDirect):
                        changeDirect = False
                    elif(not changeDirect):
                        changeDirect = True
                    hitboxShift()
                    hero = pygame.transform.flip(hero, True, False)
                    heroChange = pygame.transform.flip(heroChange, True, False)
                    heroPic = pygame.transform.flip(heroPic, True, False)
                    bullet = pygame.transform.flip(bullet, True, False)
                    bullet02 = pygame.transform.flip(bullet02, True, False)
                    bullet03 = pygame.transform.flip(bullet03, True, False)
            elif(heroHP == 0):
                pass
            else:
                if event.key == pygame.K_UP:
                    holdUP = True
                elif event.key == pygame.K_DOWN:
                    holdDOWN = True
                elif event.key == pygame.K_LEFT:
                    holdLEFT = True
                elif event.key == pygame.K_RIGHT:
                    holdRIGHT = True
                elif event.key == pygame.K_RETURN:
                    if(playerInput.split() != []):
                        compare() #比較有沒有打一樣的
                        enterBool = True #給打字特效的
                    enterBool02 = True #給hero換圖片的
                    changeDirect_cache = changeDirect #讓子彈不要亂亂動
                    inputCache = playerInput
                    playerInput = ''
                elif event.key == pygame.K_ESCAPE:
                    enterBool = False
                    playerInput = '' #清空字
                elif event.key == pygame.K_BACKSPACE:
                    holdBACK = True
                    enterBool = False
                    playerInput = playerInput[:-1]
                elif event.key == (pygame.K_LCTRL):
                    if(changeDirect):
                        changeDirect = False
                        hitboxStayMid = 1
                    elif(not changeDirect):
                        changeDirect = True
                        hitboxStayMid = -1
                    hitboxShift()
                    heroCenter[0] += 40*hitboxStayMid  #因為轉方向而產生hero位置偏移的修正
                    hero = pygame.transform.flip(hero, True, False)
                    heroChange = pygame.transform.flip(heroChange, True, False)
                    heroPic = pygame.transform.flip(heroPic, True, False)
                    bullet = pygame.transform.flip(bullet, True, False)
                    bullet02 = pygame.transform.flip(bullet02, True, False)
                    bullet03 = pygame.transform.flip(bullet03, True, False)
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
        if(Count02 == 20 and monsterHP != 0): #觸發Text產生
            randomWordsAngle()
            Count02 = 0
        if(enterBool02): #按enter的動畫
            Count03 += 1
            if(Count03 == 1):
                heroPic = heroChange
            if(Count03 == 2):
                heroPic = hero
                enterBool02 = False
                Count03 = 0
        if(holdBACK):
            Count04 += 1
            if(Count04 >= 5):
                playerInput = playerInput[:-1] #刪一個字
        if(not holdBACK):
            Count04 = 0
        if(Count05 == 40 and monsterHP != 0): #觸發改變monster移動方向
            [monster_dx, monster_dy] = randomMonsterAngle()
            Count05 = 0
        lastTick = pygame.time.get_ticks()
        Count01 += 1
        Count02 += 1
        Count05 += 1
        
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
        if(heroRect.bottom <= resolution[1]):
            heroCenter[1] += hero_dy
    if(holdLEFT):
        if(heroRect.left>=0):
            heroCenter[0] -= hero_dx
    if(holdRIGHT):
        if(heroRect.right <= resolution[0]):
            heroCenter[0] += hero_dx
    if(holdBACK):
        pass #刪一個字
    #--------------------------------------#
    #--------------按下enter字的動畫-----------------#
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
    monsterRect.center = (monsterCenter) #把monsterCenter更新到真的monster位置
    #monster的HitboxShift
    monster_leftShift = 30
    monster_rightShift = -30
    monster_topShift = 40
    monster_widthShift = monster_rightShift - monster_leftShift
    monster_heightShift = -monster_topShift
    #monster的Hitbox
    if(HITBOX):
        RECTCOORD = [monsterRect.left + monster_leftShift, monsterRect.top + monster_topShift, monsterWidth + monster_widthShift , monsterHeight + monster_heightShift]
        HEROhitbox = pygame.Rect(RECTCOORD)
        pygame.draw.rect(screen, (0,0,0), HEROhitbox, 3)
    HIT_direct = False
    Condition12 = (heroRect.left + leftShift <= monsterRect.right + monster_rightShift and heroRect.right + rightShift >= monsterRect.right + monster_rightShift) #hero在monster右邊
    Condition13 = (heroRect.left + leftShift <= monsterRect.left + monster_leftShift and heroRect.right + rightShift >= monsterRect.left + monster_leftShift) #hero在monster左邊
    Condition14 = (heroRect.left + leftShift >= monsterRect.left + monster_leftShift and heroRect.right + rightShift <= monsterRect.right + monster_rightShift) #hero在monster右邊和左邊之間
    Condition15 = (heroRect.top + topShift <= monsterRect.bottom and heroRect.bottom + bottomShift >= monsterRect.bottom) #hero在monster下面
    Condition16 = (heroRect.bottom + bottomShift >= monsterRect.top + monster_topShift and heroRect.top + topShift <= monsterRect.top + monster_topShift) #hero在monster上面
    Condition17 = (heroRect.bottom + bottomShift <= monsterRect.bottom and heroRect.top + topShift >= monsterRect.top + monster_topShift) #hero在monster上面和下面之間
    if((Condition12 or Condition13 or Condition14) and (Condition15 or Condition16 or Condition17)): #碰撞條件
        HIT_direct = True 
    #反彈
    if(monsterRect.top<=0):
        monsterRect.top = 0
        monster_dy *= -1
    if(monsterRect.bottom>=resolution[1]):
        monsterRect.bottom = resolution[1]
        monster_dy *= -1
    if(monsterRect.left<=0):
        monsterRect.left = 0
        monster_dx *= -1
    if(monsterRect.right>=resolution[0]):
        monsterRect.right = resolution[0]
        monster_dx *= -1
    if(monsterMode): #monster圖1
        monsterPic = monster
    else: #monster圖2
        monsterPic = monsterChange
    screen.blit(monsterPic,monsterRect.topleft)
    #monster 移動
    monsterCenter[1] += monster_dy
    monsterCenter[0] -= monster_dx

    #--------------------------------#
    #---------------------------------和文字有關的--------------------------------#
    HIT = False
    if(len(Text) != 0): 
        #Text movement and blit(用掃描的概念)
        for i in Text: #i = 掃到的字
            j = Text.index(i)
            TextRect = i.get_rect()
            TextRect.center = TextPosition[j] #TextCenter更新回去Text真的位置
            #Text的Hitbox
            if(HITBOX):
                RECTCOORD = [TextRect.left, TextRect.top, TextRect.width, TextRect.height]
                TEXThitbox = pygame.Rect(RECTCOORD)
                pygame.draw.rect(screen, (0,0,0), TEXThitbox, 3)
            #碰到hero就扣血
            Condition0 = (TextRect.left <= heroRect.right + rightShift and TextRect.right >= heroRect.right + rightShift) #字在hero右邊
            Condition1 = (TextRect.left <= heroRect.left + leftShift and TextRect.right >= heroRect.left + leftShift) #字在hero左邊
            Condition2 = (TextRect.left >= heroRect.left + leftShift and TextRect.right <= heroRect.right + rightShift) #字在hero右邊和左邊之間
            Condition3 = (TextRect.top <= heroRect.bottom + bottomShift and TextRect.bottom >= heroRect.bottom + bottomShift) #字在hero下面
            Condition4 = (TextRect.bottom >= heroRect.top + topShift and TextRect.top <= heroRect.top + topShift) #字在hero上面
            Condition5 = (TextRect.bottom <= heroRect.bottom + bottomShift and TextRect.top >= heroRect.top + topShift) #字在hero上面和下面之間
            if((Condition0 or Condition1 or Condition2) and (Condition3 or Condition4 or Condition5)): #碰撞條件
                HIT = True
            #字反彈
            if (TextRect.top <= 0 or TextRect.bottom >= resolution[1]):
                Text_dy[j] *= -1
            #字移動
            TextPosition[j][0] += Text_dx[j]
            TextPosition[j][1] += Text_dy[j]
            #字超過螢幕左邊就刪掉
            if (TextRect.right <= 0):
                removeText(j,1)
            elif (TextRect.left >= resolution[0]):
                removeText(j,1)
            screen.blit(i, (TextRect.topleft))
    #----------------------------------------------------------------------------# 
    #----------heroBlit-----------# 
    heroRect.center = (heroCenter)
    screen.blit(heroPic,heroRect.topleft)
    #HERO的Hitbox
    if(HITBOX):
        RECTCOORD = [heroRect.left + leftShift, heroRect.top + topShift, heroWidth + widthShift , heroHeight + heightShift]
        HEROhitbox = pygame.Rect(RECTCOORD)
        pygame.draw.rect(screen, (0,0,0), HEROhitbox, 3)
    #-----------------------------#
    #-------------------------------------------------Bullet飛行---------------------------------------------------#
    #平常子彈一直追蹤英雄位置(最新位置在index 0)
    if(not changeDirect):
        bulletCenter = [heroCenter[0] + 100, heroCenter[1] + 4]
    elif(changeDirect):
        bulletCenter = [heroCenter[0] - 100, heroCenter[1] + 4]
    #掃描顯示
    HIT_monster = False
    for i in bulletArray:
        j = bulletArray.index(i)
        bulletRect[j].center = bulletCenter_cache[j] #更新Center到真的子彈位置
    #----------看是否擊中monster------------#
        Condition6 = (bulletRect[j].left <= monsterRect.right + monster_rightShift and bulletRect[j].right >= monsterRect.right + monster_rightShift) #子彈在monster右邊
        Condition7 = (bulletRect[j].left <= monsterRect.left + monster_leftShift and bulletRect[j].right >= monsterRect.left + monster_leftShift) #子彈在monster左邊
        Condition8 = (bulletRect[j].left >= monsterRect.left + monster_leftShift and bulletRect[j].right <= monsterRect.right + monster_rightShift) #子彈在monster右邊和左邊之間
        Condition9 = (bulletRect[j].top <= monsterRect.bottom and bulletRect[j].bottom >= monsterRect.bottom) #子彈在monster下面
        Condition10 = (bulletRect[j].bottom >= monsterRect.top + monster_topShift and bulletRect[j].top <= monsterRect.top + monster_topShift) #子彈在monster上面
        Condition11 = (bulletRect[j].bottom <= monsterRect.bottom and bulletRect[j].top >= monsterRect.top + monster_topShift) #子彈在monster上面和下面之間
        if(heroBulletFlag[j] == 1):
            if((Condition6 or Condition7 or Condition8) and (Condition9 or Condition10 or Condition11)): #碰撞條件
                HIT_monster = True
            if(changeDirect_cache): #看hero身體方向飛
                if(bulletCenter_cache[j][0] >= 0):
                    bulletCenter_cache[j][0] -= 50
                else:
                    heroBulletFlag[j] = 0
                    bulletArray.pop(j)
                    bulletCenter_cache.pop(j)
                    heroBulletFlag.pop(j)
            else:
                if(bulletCenter_cache[j][0] <= resolution[0]):
                    bulletCenter_cache[j][0] += 50
                else:
                    heroBulletFlag[j] = 0
                    bulletArray.pop(j)
                    bulletCenter_cache.pop(j)
                    heroBulletFlag.pop(j)
        screen.blit(i ,bulletRect[j].topleft) #一次tick只要blit一次物件就好
    #---------------------------------------------------------------------------------------------------------------#
    #--------------------血條顯示------------------------------------------------#
    heroHPcolor = [255,255,255]
    monsterHPcolor = [255,255,255]
    #-------扣血--------#
    if((HIT or HIT_direct) and not gameOver and not gameStart): #HIT撞到字 HIT_direct撞到怪
        if(HIT):
            heroHP -= 10 #扣的血量
            print('hit by a word!')
        if(HIT_direct):
            heroHP -= 15
            print('hit by monster!')
        heroHPcolor = [255,103,92]
    if(HIT_monster):
        monsterHP -= removeNum*3 #傷害 = 消一個*2
        monsterHPcolor = [255,103,92]
        print('monster get hit!')
    #血量不會突破限制
    if(heroHP > heroHP_origin):
        heroHP = heroHP_origin
    if(heroHP <= 0):
        heroHP = 0
    if(monsterHP > monsterHP_origin):
        monsterHP = monsterHP_origin
    if(monsterHP <= 0):
        monsterHP = 0
    #--------加血換顏色-----------#
    if(HPchangeColor != 0): #把按enter(非空字串)檢查的訊號變正緣訊號
        if(HPchangeColor == 1):
            HPchangeColorHold01 = True #啟動timer01
        elif(HPchangeColor == 2):
            HPchangeColorHold02 = True #啟動timer02
        simTimer01 = 100
        simTimer02 = 100
        HPchangeColor = 0
    if(HPchangeColorHold01):
        heroHPcolor = [82,255,139] #打對英雄變的顏色
        simTimer01 -= 5 #遞減單位 越高時間越短
        if(simTimer01 <= 0):
            HPchangeColorHold01 = False
    if(HPchangeColorHold02):
        monsterHPcolor = [82,255,139] #打錯怪物變的顏色
        simTimer02 -= 5 #遞減單位 越高時間越短
        if(simTimer02 <= 0):
            HPchangeColorHold02 = False
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
    #------------------------------------------------------------------------------#
    #------------背景閃一下------------#
    if(alphaSolidFlag != 0):
        if(alphaSolidFlag == 1): #一拿到訊號就把它關掉，並開啟另一個訊號(轉換成正緣訊號的概念)
            alphaSolid.fill((0,150,0))  #打對的顏色
            AlphaVal02_origin = 30 #打對的alpha
        elif(alphaSolidFlag == 2):
            alphaSolid.fill((120,0,0)) #打錯的顏色
            AlphaVal02_origin = 80 #打錯的alpha
        AlphaVal02 = AlphaVal02_origin    
        alphaSolidHold = True
        alphaSolidFlag = 0
    if(alphaSolidHold):
        AlphaVal02 -= math.floor(AlphaVal02_origin/15) #背景紅一下的alpha值
        alphaSolid.set_alpha(AlphaVal02)
        screen.blit(alphaSolid, (0,0))
        if(AlphaVal02 <= 0):
            alphaSolidHold = False
    #---------------------------------#
    #---------遊戲訊息-----------#
    gameMessage_small = ''
    messageColor = [248,210,34] #訊息顏色
    if(gameStart): #遊戲開始訊息
        gameMessage = 'Press any key to START'
        needMessage = True
    if(monsterHP == 0): #WIN的訊息
        gameMessage = 'YOU WIN'
        gameMessage_small = 'Press Enter to Restart'
        needMessage = True
        gameOver = True
        if(monsterHP == 0):
            monster_dy = 0
            monster_dx = 0
    if(heroHP == 0): #LOSE的訊息
        gameMessage = 'YOU ARE DEAD'
        gameMessage_small = 'Press Enter to Restart'
        needMessage = True
        gameOver = True
        if(heroHP == 0):
            hero_dy = 0
            hero_dx = 0
    if(needMessage):
        #訊息render
        gameText = playerFont.render(gameMessage, 0, messageColor)
        gameText_small = Font.render(gameMessage_small, 0, (255,255,255))
        if(gameStart):
            gameTextRect = gameText.get_rect()
            scaleVal = (math.floor(gameTextRect.width * 0.6), math.floor(gameTextRect.height * 0.6)) #遊戲開始的訊息大小調整
            gameText = pygame.transform.scale(gameText, scaleVal)
        gameText.set_alpha(230) #設定訊息透明度
        gameTextRect = gameText.get_rect()
        gameText_smallRect = gameText_small.get_rect()
        X = math.floor(resolution[0]/2-gameTextRect.width/2) #位置置中
        Y = math.floor(resolution[1]/2-gameTextRect.height/2) #位置置中
        gameTextRect.topleft = (X, Y) #大字的Rect
        gameText_smallRect.topleft = (X, Y+150) #按enter繼續的Rect
        screen.blit(gameText, gameTextRect.topleft)
        screen.blit(gameText_small, gameText_smallRect.topleft)
        #--------外框--------#
        RECTCOORD = [gameTextRect.left - 10, gameTextRect.top - 5, gameTextRect.width + 20, gameTextRect.height + 10]
        MESSAGErect1 = pygame.Rect(RECTCOORD)
        pygame.draw.rect(screen, (248,210,34), MESSAGErect1, 6) #外框顏色
    if(gameStart):
        startTime = pygame.time.get_ticks()
    if(gameOver and not timeTotal): #timePast如果為空回傳False
        endTime = pygame.time.get_ticks()
        timeTotal = (endTime - startTime)/1000 #經過timeTotal秒
        print('遊戲結束，花了', timeTotal, '秒')
    #nowTime = pygame.time.get_ticks()

    if(reset):
        gameReset()
    #----------------------------#

    pygame.display.update()
    
    if(len(Text) > 40): #字的數量超過40就pop掉一個
        Text.pop()
        Text_dx.pop()
        Text_dy.pop()
        randomText.pop()
        TextPosition.pop()
    if(len(bulletArray) > 14):
        bulletArray.pop()
        bulletCenter_cache.pop()
        heroBulletFlag.pop()
pygame.font.quit()
pygame.quit()
