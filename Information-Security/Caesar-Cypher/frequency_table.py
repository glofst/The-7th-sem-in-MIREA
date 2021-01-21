from operator import itemgetter

class FrequencyTable:
    
    __table = {}
    __wordAmount = 0

    def __init__(self, filename, alphabet):
        self.__table = dict.fromkeys(alphabet, 0)
        with open(filename, 'r') as source:
            for line in source:
                line = line.lower()
                for symbol in line:
                    if symbol in alphabet:
                        self.__table[symbol] += 1
        
        self.__wordAmount = sum(self.__table.values())
        self.__table = {key: (value / self.__wordAmount) for key, value in self.__table.items()}


    def getFreq(self, symbol):
        return self.__table[symbol]


    def getMaxValue(self):
        return max(self.__table.items(), key=itemgetter(1))


    def findClosestValue(self, value, used):
        minSymbol = ''
        minDiffer = 100

        for symbol, freq in self.__table.items():
            currentDiffer = abs(value - freq)
            if currentDiffer < minDiffer and symbol not in used:
                minSymbol = symbol
                minDiffer = currentDiffer
        
        return minSymbol