import sympy
import random
import sys


def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a%b)


def findPrimitiveRoot(modulus):
    required_set = set(num for num in range (1, modulus) if gcd(num, modulus) == 1)
    for g in range(1, modulus):
        actual_set = set(pow(g, powers) % modulus for powers in range (1, modulus))
        if required_set == actual_set:
            return g


def fastMultiply(multiplier, multiplicand, modulus):
	if multiplicand == 1:
		return multiplier

	if multiplicand % 2 == 0:
		temp = fastMultiply(multiplier, multiplicand/2, modulus)
		return (2 * temp) % modulus
	
	return (fastMultiply(multiplier, multiplicand-1, modulus) + multiplier) % modulus


def fastPows(base, exponent, modulus):
	if exponent == 0:
		return 1
        
	if exponent % 2 == 0:
		temp = fastPows(base, exponent/2, modulus)
		return fastMultiply(temp, temp, modulus) % modulus
	
	return (fastMultiply(fastPows(base, exponent-1, modulus), base, modulus)) % modulus


class DH_Endpoint:

    def __init__(self, publicKeyP=None, publicKeyG=None):
        self.__privateKey = random.randint(0, sys.maxsize)
        if publicKeyP == None and publicKeyG == None:
            self.__publicKeyP = self.generatePublicKeyP() 
            self.__publicKeyG = self.generatePublicKeyG() 
        else:
            self.__publicKeyP = publicKeyP
            self.__publicKeyG = publicKeyG

        print(self.__publicKeyG, self.__privateKey, self.__publicKeyP)


    def generatePublicKeyP(self):
        return sympy.prime(random.randint(0, 1000))


    def generatePublicKeyG(self):
        return findPrimitiveRoot(self.__publicKeyP)


    def getPublicKeyP(self):
        return self.__publicKeyP


    def getPublicKeyG(self):
        return self.__publicKeyG


    def generatePartialKey(self):
        return fastPows(self.__publicKeyG, self.__privateKey, self.__publicKeyP)


    def generateFullKey(self, recievedPartialKey):
        return fastPows(recievedPartialKey, self.__privateKey, self.__publicKeyP)

