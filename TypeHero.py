import pygame
import pygame.font as Pyfont
import os
import random
import math
#1 blit per frame
#compare的for好像可以用if替代
#讓字會往右彈
#一樣的字用特別顏色
#monster每隔一段時間變化移動方式
#加血量有提示
#沒辦法同時射兩顆

#全部調回預設值
def gameReset():
    global gameStart, gameOver, running, monsterMode, heroBulletFlag\
        , Count01, Count02, Count03, Count04, Count05, Count_bullet\
            , holdUP, holdDOWN, holdLEFT, holdRIGHT, holdBACK, monster_dx, monster_dy, flag_success, enterBool, enterBool02\
                , needMessage, heroHP, monsterHP, heroCenter, monsterCenter, reset, hero_dx, hero_dy
    #Before Loop
    gameStart = True #遊戲開始
    gameOver = False #遊戲結束
    running = True #視窗執行中
    monsterMode = True #monster哪一張圖片
    heroBulletFlag = False #子彈一開始沒出現
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
    enterBool = False #是否按下enter
    enterBool02 =False 
    needMessage = False #需要遊戲訊息
    reset = False
    heroHP = heroHP_origin
    monsterHP = monsterHP_origin
    heroCenter = [math.floor(resolution[0]/3), math.floor(resolution[1]/2)]
    monsterCenter = [math.floor(resolution[0]-monsterWidth/2), math.floor(resolution[1]/2)]
    monster_dy = monster_moveSpeed
    monster_dx = monster_moveSpeed
    hero_dx = hero_moveSpeed
    hero_dy = hero_moveSpeed
    Count_bullet = 0
    hitboxShift()
    Text.clear()
    Text_dy.clear()
    TextPosition.clear()
    randomText.clear()
    bulletArray.clear()
    bulletCenter_cache.clear()
    randomWordsAngle() #先產生一個字

#hitboxShift
def hitboxShift():
    global leftShift, rightShift, topShift, widthShift, heightShift
    if(not changeDirect):
        leftShift = 25
        rightShift = -70
        topShift = 17
        widthShift = rightShift - leftShift
        heightShift = -topShift
    if(changeDirect):
        leftShift = 70
        rightShift = -25
        topShift = 17
        widthShift = rightShift - leftShift
        heightShift = -topShift
#text的rect.top rect.bottom怪怪的，只好手動調整每個數值
def TextAttributes(i):
    global TextWidth, TextTop, TextBottom, TextHeight, TextRight, TextLeft_x, TextLeft_y
    j = Text.index(i) #j = 那個字的index
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
    Text_dy.insert(0, random.randint(-5,5)) #Text_dy -2~2 隨機 插入index 0
    print(randomText)
    TextPosition.insert(0, monsterCenter.copy()) #Text位置 = monster位置
    #修正文字到嘴巴的位置
    TextPosition[0][0] -= 55
    TextPosition[0][1] += 15

#比較打對哪個字的函式
def compare():
    global monsterHP, heroHP, playerTextColorFlag, heroBulletFlag, heroBulletFlag02, removeNum
    flag_success = False
    playerTextColorFlag = flag_success
    heroBulletFlag = flag_success
    heroBulletFlag02 = flag_success
    for i in randomText: 
        if(playerInput == i): #成功打入一樣的字母
            flag_success = True
            playerTextColorFlag = flag_success
            heroBulletFlag = flag_success
            heroBulletFlag02 = flag_success
            j = randomText.index(i)
            removeNum = removeText(j,0)
            if(removeNum == 1):
                bulletPic = bullet
            elif(removeNum == 2):
                bulletPic = bullet02
            elif(removeNum >= 3):
                bulletPic = bullet03
            bulletArray.insert(0, bulletPic) #加一顆子彈圖片到Array
            bulletCenter_cache.insert(0, bulletCenter) #加子彈位置到Array
            heroHP += removeNum*5 #消一個hero加5HP
            if(heroHP > heroHP_origin):
                heroHP = heroHP_origin
            print(removeNum)
            print('你打對',playerInput,'了')
            print(monsterHP)
    if(not flag_success):#沒打對的話
        monsterHP += 10 #monster加血
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
heroPic = hero
#hero picture_b
heroChange = pygame.image.load(os.path.join(path, 'hero01_b.png'))
herorChange = heroChange.convert_alpha()
heroChange = pygame.transform.scale(heroChange, (150,120)) #hero大小調整
#heroPosition
heroCenter = [math.floor(resolution[0]/3), math.floor(resolution[1]/2)]
hero_moveSpeed = 10 #按一下移動多少
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
for i in range(4): #弄4個一樣的Rect
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
monsterCenter = [math.floor(resolution[0]-monsterWidth/2), math.floor(resolution[1]/2)]
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
changeDirect = False
gameReset()
#Loop
while running:
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
                    hero = pygame.transform.flip(hero, True, False)
                    heroChange = pygame.transform.flip(heroChange, True, False)
                    heroPic = pygame.transform.flip(heroPic, True, False)
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
                    elif(not changeDirect):
                        changeDirect = True
                    hitboxShift()
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
        if(Count02 == 15 and monsterHP != 0): #觸發Text產生
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
        lastTick = pygame.time.get_ticks()
        Count01 += 1
        Count02 += 1
        
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
    #monster 移動&反彈
    monsterCenter[1] += monster_dy
    monsterCenter[0] -= monster_dx
    monsterRect.center = (monsterCenter)
    if (monsterRect.top<=0 or monsterRect.bottom>=resolution[1]):
        monster_dy *= -1
    if (monsterRect.left<=0 or monsterRect.right>=resolution[0]):
        monster_dx *= -1
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
            screen.blit(i, (TextPosition[j][0], TextPosition[j][1]))
            #字超過螢幕左邊就刪掉
            if (TextRight <= 0):
                removeText(j,1)
            '''
            #Text的Hitbox
            RECTCOORD = [TextLeft_x, TextTop, TextWidth, TextHeight]
            TEXThitbox = pygame.Rect(RECTCOORD)
            pygame.draw.rect(screen, (0,0,0), TEXThitbox, 3)
            '''
    #----------------------------------------------------------------------------# 
    #----------HeroBlit-----------# 
    heroRect.center = (heroCenter)
    screen.blit(heroPic,heroRect.topleft)

    #HERO的Hitbox
    RECTCOORD = [heroRect.left + leftShift, heroRect.top + topShift, heroWidth + widthShift , heroHeight + heightShift]
    HEROhitbox = pygame.Rect(RECTCOORD)
    pygame.draw.rect(screen, (0,0,0), HEROhitbox, 3)

    #-----------------------------#
    #-------------------------------------------------Bullet飛行---------------------------------------------------#
    #平常子彈一直追蹤英雄位置
    if(not changeDirect):
        bulletCenter = [heroCenter[0] + 100, heroCenter[1] + 4]
    elif(changeDirect):
        bulletCenter = [heroCenter[0] - 100, heroCenter[1] + 4]
    #掃描顯示
    HIT_monster = False
    for i in bulletArray:
        j = bulletArray.index(i)
        bulletRect[j].center = bulletCenter_cache[j]
    #----------看是否擊中monster------------#
        Condition6 = (bulletRect[j].left <= monsterRect.right + rightShift and bulletRect[j].right >= monsterRect.right + rightShift) #字在hero右邊
        Condition7 = (bulletRect[j].left <= monsterRect.left + leftShift and bulletRect[j].right >= monsterRect.left + leftShift) #字在hero左邊
        Condition8 = (bulletRect[j].left >= monsterRect.left + leftShift and bulletRect[j].right <= monsterRect.right + rightShift) #字在hero右邊和左邊之間
        Condition9 = (bulletRect[j].top <= monsterRect.bottom and bulletRect[j].bottom >= monsterRect.bottom) #字在hero下面
        Condition10 = (bulletRect[j].bottom >= monsterRect.top + topShift and bulletRect[j].top <= monsterRect.top + topShift) #字在hero上面
        Condition11 = (bulletRect[j].bottom <= monsterRect.bottom and bulletRect[j].top >= monsterRect.top + topShift) #字在hero上面和下面之間
        if(heroBulletFlag):
            if((Condition6 or Condition7 or Condition8) and (Condition9 or Condition10 or Condition11)): #碰撞條件
                HIT_monster = True
            if(changeDirect_cache):
                if(bulletCenter_cache[j][0] >= 0): #讓位置1的子彈位移
                    bulletCenter_cache[j][0] -= 50
                else:
                    heroBulletFlag = False
                    bulletArray.pop(j)
                    bulletCenter_cache.pop(j)
            else:
                if(bulletCenter_cache[j][0] <= resolution[0]): #讓位置1的子彈位移
                    bulletCenter_cache[j][0] += 50
                else:
                    heroBulletFlag = False
                    bulletArray.pop(j)
                    bulletCenter_cache.pop(j)
        screen.blit(i ,bulletRect[j].topleft)
    #---------------------------------------------------------------------------------------------------------------#
    #--------------------血條顯示------------------------------------------------#
    heroHPcolor = [255,255,255]
    monsterHPcolor = [255,255,255]
    #-------扣血--------#
    if(HIT and not gameOver and not gameStart):
        heroHP -= 5 #扣的血量
        heroHPcolor = [255,0,0]
        if(heroHP <= 0):
            heroHP = 0
        print('HIT')
    if(HIT_monster):
        monsterHP -= removeNum*2 #消一個monster扣5HP
        monsterHPcolor = [255,0,0]
        if(monsterHP <= 0):
            monsterHP = 0
        print('HIT_monster')
    #-------------------#
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
    #---------遊戲訊息-----------#
    messageColor = [248,210,34] #訊息顏色
    if(gameStart): #遊戲開始訊息
        gameMessage = 'Press any key to START'
        needMessage = True
    if(monsterHP == 0): #WIN的訊息
        gameMessage = 'YOU WIN'
        needMessage = True
        gameOver = True
        if(monsterHP == 0):
            monster_dy = 0
            monster_dx = 0
    if(heroHP == 0): #LOSE的訊息
        gameMessage = 'YOU ARE DEAD'
        needMessage = True
        gameOver = True
        if(heroHP == 0):
            hero_dy = 0
            hero_dx = 0
    if(needMessage):
        gameText = playerFont.render(gameMessage, 0, messageColor)
        if(gameStart):
            gameTextRect = gameText.get_rect()
            scaleVal = (math.floor(gameTextRect.width * 0.6), math.floor(gameTextRect.height * 0.6))
            gameText = pygame.transform.scale(gameText, scaleVal)
        gameText.set_alpha(230) #設定訊息透明度
        gameTextRect = gameText.get_rect()
        X = math.floor(resolution[0]/2-gameTextRect.width/2)
        Y = math.floor(resolution[1]/2-gameTextRect.height/2)
        gameTextRect.topleft = (X, Y)
        screen.blit(gameText, gameTextRect.topleft)
        RECTCOORD = [gameTextRect.left - 10, gameTextRect.top - 5, gameTextRect.width + 20, gameTextRect.height + 10]
        MESSAGErect1 = pygame.Rect(RECTCOORD)
        pygame.draw.rect(screen, (248,210,34), MESSAGErect1, 6) #外框顏色
    if(reset):
        gameReset()

    #----------------------------#
    
    
    pygame.display.update()
    
    if(len(Text) > 40): #字的數量超過40就pop掉一個
        Text.pop()
        Text_dy.pop()
        TextPosition.pop()
pygame.font.quit()
pygame.quit()
