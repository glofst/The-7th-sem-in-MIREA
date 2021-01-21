from operator import itemgetter

class BigramFrequencyTable:
    
    __bigramTable = {}
    __bigramAmount = 0

    def __init__(self, filename, alphabet):
        self.__createBigramAlphabet(alphabet)
        with open(filename, 'r') as source:
            for line in source:
                lastSymbol = ''
                line = line.lower()
                for symbol in line:
                    if symbol in alphabet and lastSymbol in alphabet:
                        self.__bigramTable[symbol+lastSymbol] += 1
                    lastSymbol = symbol
        
        self.__bigramAmount = sum(self.__bigramTable.values())
        self.__bigramTable = {key: (value / self.__bigramAmount) for key, value in self.__bigramTable.items()}


    def __createBigramAlphabet(self, alphabet):
        self.__bigramTable = {(first+second): 0 for first in alphabet for second in alphabet}


    def getFreq(self, bigram):
        return self.__bigramTable[bigram]


    def getMaxValue(self):
        return max(self.__bigramTable.items(), key=itemgetter(1))


    def findKey(self, otherFreq):
        return -(alphabet.index(sourceFreq.getMaxValue()[0]) - 
                    alphabet.index(cryptedFreq.getMaxValue()[0]))

    def findClosestValue(self, value, used):
        minBigram = ''
        minDiffer = 100

        for bigram, freq in self.__bigramTable.items():
            currentDiffer = abs(value - freq)
            if currentDiffer < minDiffer and bigram not in used:
                minBigram = bigram
                minDiffer = currentDiffer
        
        return minBigram