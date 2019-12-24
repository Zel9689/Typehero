import pygame
import pygame.font as Pyfont
import os
import random

#nonPygame side
path = os.path.split(os.path.abspath(__file__))[0] #遊戲資料夾位址
f = open(path + '\dictionary.txt','r')
Dict = f.read()
words = Dict.splitlines() #字的List
wordsNum = len(words) #字的數量
for i in range(wordsNum):
    words[i] = words[i].strip('\'')


#init
pygame.init()
pygame.font.init()
pygame.display.set_caption("Type Hero")
resolution = (1024, 768)
screen = pygame.display.set_mode(resolution)
background = pygame.Surface(screen.get_size())

#background
background.fill((125,125,125))
background = background.convert()

#words
fontLocation = Pyfont.match_font('Minecraft Regular')
Font = Pyfont.Font(fontLocation, 20)
Text = Font.render(words[0], True, (0,0,0))
TextPosition = [1024, random.randint(20, resolution[1]-20)]
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

dy = 3 #移動速度

#monsters health

#game clock
clock = pygame.time.Clock()

#Loop
running = True
while running:
    clock.tick(30) #fps
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.blit(background, (0,0))
    screen.blit(Text, TextPosition)

#moving monster
    monsterCenter[1] += dy
    monsterRect.center = (monsterCenter)
    if (monsterRect.top<=0 or monsterRect.bottom>=screen.get_height()):
        dy *= -1
    #每500ms換一次圖片
    if (pygame.time.get_ticks()%1000 <= 500): 
        screen.blit(monster,monsterRect.topleft)
    else:
        screen.blit(monsterChange,monsterRect.topleft)

    pygame.display.update()
pygame.font.quit()
pygame.quit()
