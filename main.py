import pygame
import pygame.font as Pyfont
import os
import random
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
def getCollectionList(name):
    path = os.path.dirname(os.path.abspath(__file__)) #遊戲資料夾位址
    f = open('./dictionary.txt','r') #開啟字典
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
    return wordCollection

#init
pygame.init()
pygame.font.init()
resolution = [1280, 768]
pygame.display.set_caption("Type Hero")
screen = pygame.display.set_mode(resolution)
