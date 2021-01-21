import string
from sys import maxsize, exit
import random
import socket
from hashlib import sha256
import json


def calculateHash(data):
    return int(sha256(data.encode()).hexdigest(), 16)


class SRPClient:

    def __init__(self):
       self.__sock = socket.socket()


    def connect(self, host, port):
       self.__sock.connect((host, port))
       
       primeData = json.loads(self.__sock.recv(1024).decode('utf-8'))
       print(primeData)
       self.chooseScript()(primeData)

       self.__sock.close()


    def chooseScript(self):
        answer = input('What you want to do? (login/register)\n')
        if answer == 'login':
            return self.loginScript
        elif answer == 'register':
            return self.registerScript
        
        
    def __generateSalt(self, length):
        letters_and_digits = string.ascii_letters + string.digits
        return ''.join((random.choice(letters_and_digits) for i in range(length)))


    def registerScript(self, primeData):
        username = input("Username: ")
        password = input("Password: ")
        salt = self.__generateSalt(10)

        x = calculateHash(salt + password)
        verifier = pow(primeData['generator'], x, primeData['primeNumber'])

        jMessage = json.dumps({
            'script' : 'register',
            'username' : username,
            'salt' : salt,
            'verifier' : verifier
            })

        print(jMessage)
        
        self.__sock.send(jMessage.encode('utf-8'))


    def loginScript(self, primeData):
        username = input("Username: ")
        password = input("Password: ")

        print(primeData)

        primeNumber = primeData['primeNumber']
        generator = primeData['generator']
        k = primeData['parameterK']

        a = random.randint(0, maxsize)
        A = pow(generator, a, primeNumber)
        print('A: ', A)
        jData = json.dumps({
            'script' : 'login',
            'username' : username,
            'publicKeyA' : A
        })
        self.__sock.send(jData.encode('utf-8'))
        jData = json.loads(self.__sock.recv(1024).decode('utf-8'))
        print(jData)

        B = jData['publicKeyB']
        salt = jData['salt']
        if B == 0:
            self.weFuckedUp()

        scrambler = calculateHash(str(A) + str(B))
        print('u: ', scrambler)
        if scrambler == 0:
            self.weFuckedUp()

        x = calculateHash(salt + password)
        S = B - k * (pow(generator, x, primeNumber)) 
        S = pow(S, a + scrambler * x, primeNumber)
        print('S: ', S)

        K = calculateHash(str(S))
        print('K: ', K)

        M = calculateHash(self.calculateM(
            primeNumber, 
            generator, 
            username, 
            salt, 
            A, B, K
            )) 
        print('M: ', M)
        self.__sock.send(str(M).encode('utf-8'))

        serverR = (self.__sock.recv(1024)).decode('utf-8')

        R = calculateHash(str(A) + str(M) + str(K))

        if str(R) == serverR:
            print('Yeah, Boy!')
        else:
            print('We fucked up! Run!')
        print('clientR: ', R)
        print('serverR: ', serverR)


    def calculateM(self, N, g, I, salt, A, B, K):
        tmp = calculateHash(str(N))
        tmp ^= calculateHash(str(g))
        result = str(tmp) + str(calculateHash(I))
        result += salt + str(A) + str(B) + str(K)
        return result


    def weFuckedUp(self): 
        print('We fucked up! Run!')
        self.__sock.close()
        exit(1)
