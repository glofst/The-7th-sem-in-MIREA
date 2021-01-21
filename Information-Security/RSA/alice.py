import random
import json
import socket
from key import Key
from collections import namedtuple
import sympy
from math import gcd


def getPrimes(start, stop):
    if start >= stop:
        return []
    primes = sympy.primerange(start, stop)
    return list(primes)


def areRelativelyPrime(a, b):
    return gcd(a, b) == 1


def getKeys(length):
    n_min = 1 << (length - 1)
    n_max = (1 << length) - 1

    start = 1 << (length // 2 - 1)
    stop = 1 << (length // 2 + 1)
    primes = getPrimes(start, stop)

    while primes:
        p = random.choice(primes)
        primes.remove(p)
        q_candidates = [q for q in primes
                        if n_min <= p * q <= n_max]
        if q_candidates:
            q = random.choice(q_candidates)
            break

    stop = (p - 1) * (q - 1)
    for e in range(3, stop, 2):
        if areRelativelyPrime(e, stop):
            break

    for d in range(3, stop, 2):
        if d * e % stop == 1:
            break

    return Key(p * q, e), Key(p * q, d)


def decrypt(cryptedList, private):
    text = ''
    for ch in cryptedList:
        text += chr(private.crypt(ch))
    return text


if __name__ == '__main__':
    public, private = getKeys(16)
    print(f'>> Public keys: {public.n}, {public.k}')
    print(f'>> Private keys: {private.n}, {private.k}')

    sock = socket.socket()
    sock.connect(('', 2000))

    
    message = json.dumps({
        'n' : public.n,
        'k' : public.k
    })
    print('>> Alice send to Bob: ', message)
    sock.send(message.encode('utf-8'))

    data = json.loads(sock.recv(1024).decode('utf-8'))
    print('>> Alice requested from Bob: ', data)

    decrypted = decrypt(data['crypted'], private)
    print('>> Decrypted message: ', decrypted)