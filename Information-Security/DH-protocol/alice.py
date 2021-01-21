import socket
import sys
import sympy
import random
from dh_protocol import DH_Endpoint
import json


if __name__ == "__main__":
    Alice = DH_Endpoint() 

    sock = socket.socket()
    sock.connect(('', 2000))
    print('>> Alice met Bob')

    message = json.dumps({
        'PublicKeyG': Alice.getPublicKeyG(), 
        'PublicKeyP': Alice.getPublicKeyP(), 
        'PartialKey': Alice.generatePartialKey()
    }).encode('utf-8')
    sock.send(message)

    data = sock.recv(1024)
    sock.close()
    data = json.loads(data.decode('utf-8'))
    key = Alice.generateFullKey(data['PartialKey']) 

    print('Crypted key: ', key)
