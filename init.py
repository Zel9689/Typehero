import pygame
def getCollectionList():
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
wordCollection = getCollectionList()
pygame.init()
pygame.font.init()
pygame.display.set_caption("Type Hero")
resolution = [1280, 768]
screen = pygame.display.set_mode(resolution)
lastTick = 0