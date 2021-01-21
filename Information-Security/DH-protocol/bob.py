import socket
import sympy
import random
import sys
from dh_protocol import DH_Endpoint
import json


if __name__ == "__main__":
    sock = socket.socket()
    sock.bind(('', 2000))
    sock.listen(1)
    print(">> Bob waked up")

    while True:
        print('>> Bob waiting for new friends')
        conn, addr = sock.accept()
        print ('>> Bob met: ', addr)

        data = conn.recv(1024)
        if not data:
            print('Data failed')
            conn.close()

        data = json.loads(data.decode('utf-8'))
        Bob = DH_Endpoint(data['PublicKeyP'], data['PublicKeyG'])

        conn.send(json.dumps({'PartialKey': Bob.generatePartialKey()}).encode('utf-8'))
        conn.close()
        print('>> Bob said Goodbye')

        key = Bob.generateFullKey(data['PartialKey'])
        print('Crypted key: ', key)
