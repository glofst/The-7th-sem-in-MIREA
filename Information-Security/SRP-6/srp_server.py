import string
from sys import maxsize, exit
import random
import socket
from hashlib import sha256
import json
import sympy
from math import gcd


def findPrimitiveRoot(modulo):
    required_set = set(num for num in range (1, modulo) if gcd(num, modulo) == 1)
    for g in range(1, modulo):
        actual_set = set(pow(g, powers) % modulo for powers in range (1, modulo))
        if required_set == actual_set:
            return g


def calculateHash(data):
    return int(sha256(data.encode()).hexdigest(), 16)


class SRPServer:

    def __init__(self, host, port):
        self.__sock = socket.socket()
        self.__sock.bind((host, port))
        self.__sock.listen(1)

        self.__primeNumber = sympy.prime(random.randint(100, 1000))
        self.__generator = findPrimitiveRoot(self.__primeNumber)
        self.__parameterK = 3
        self.__database = {}
        print('>> Server initiated')


    def online(self):
        while True:
            print('>> Waiting for connections...')
            conn, addr = self.__sock.accept()
            print('>> Accepted connection: ', addr)
            self.sendPrimeValues(conn)
            print('>> Prime values was sent')

            jData = json.loads(conn.recv(1024).decode('utf-8'))
            self.chooseScript(jData['script'])(jData, conn)
            conn.close()
            print('>> Connection closed')


    def chooseScript(self, script):
        if script == 'register':
            return self.registerScript
        elif script == 'login':
            return self.loginScript


    def registerScript(self, jData, conn):
        self.__database[jData['username']] = {
            'salt' : jData['salt'],
            'verifier' : jData['verifier']
        }


    def loginScript(self, jData, conn):
        if jData['publicKeyA'] == 0:
            print('We fucked up! Run!')
            return

        print(jData) 
        username = jData['username']
        salt = self.__database[username]['salt']
        v = self.__database[username]['verifier']
        A = jData['publicKeyA']
        b = random.randint(0, maxsize)
        B = (self.__parameterK * v + pow(self.__generator, b, self.__primeNumber)) % self.__primeNumber
        jData = json.dumps({
            'salt' : salt,
            'publicKeyB' : B
        })
        print(jData) 
        conn.send(jData.encode('utf-8'))

        scrambler = calculateHash(str(A) + str(B))
        print('u: ', scrambler)
        if scrambler == 0:
            print('We fucked up! Run!')
            return


        S = pow((A * pow(v, scrambler, self.__primeNumber)), b, self.__primeNumber) 
        print('S: ', S)
        K = calculateHash(str(S))
        print('K: ', K)


        clientM = conn.recv(1024).decode('utf-8')
        M = calculateHash(self.calculateM(username, salt, A, B, K)) 
        print('serverM: ', M)
        print('clientM: ', clientM)
        if str(M) == clientM:
            print('Yeah, Boy!')
        else:
            print('We fucked up! Run!')
            return

        R = calculateHash(str(A) + str(M) + str(K))
        conn.send(str(R).encode('utf-8'))


    def calculateM(self, I, salt, A, B, K):
        tmp = calculateHash(str(self.__primeNumber))
        tmp ^= calculateHash(str(self.__generator))
        result = str(tmp) + str(calculateHash(I))
        result += salt + str(A) + str(B) + str(K)
        return result


    def sendPrimeValues(self, conn):
        jMessage = json.dumps({
            'primeNumber' : self.__primeNumber, 
            'generator' : self.__generator, 
            'parameterK' : self.__parameterK
            })
        conn.send(jMessage.encode('utf-8'))