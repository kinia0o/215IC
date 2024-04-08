import random
import string
from collections import Counter

if __name__ == '__main__':
    L22677 = []
    ciag = ''.join(random.choices(string.ascii_lowercase, k=100))
    print(ciag)
    # wersja 1
    Dznakow ={}
    for znak in ciag:
        if znak in Dznakow:
            Dznakow[znak]+=1
        else:
            Dznakow[znak]=1
    print(Dznakow)
    # wersja 2
    D2znakow=Counter(ciag)
    print(D2znakow)
    #  Utwórzona lista, której każdy element to krotka 
    for x in Dznakow:
        L22677.append((x,Dznakow[x]))
    print(L22677)
