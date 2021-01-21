from pathlib import Path
from math import sqrt

for_training_dir = Path('workout')
for_competition_dir = Path('competition')
picture_size = 7

symbols = { -1 : '-', 1 : '@' }

def getSymbol(index):
    return symbols[index]


def getId(symbol):
    return list(symbols.keys())[list(symbols.values()).index(symbol)]


# Печатает образ в виде ASCII-графики
def print_picture(picture):
    for i in range(len(picture)):
        if i % picture_size == 0:
            print()
        print(symbols[picture[i]], end='')
    print('\n')