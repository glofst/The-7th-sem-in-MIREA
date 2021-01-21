import socket
from key import Key
import json


def encrypt(text, public):
    cryptedList = []
    for ch in text:
        cryptedList.append(public.crypt(ord(ch)))
    return cryptedList


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
        print('>> Bob requested from Alice: ', data)

        message = 'Hello, world!'
        print('>> Message to sent: ', message)
        public = Key(data['n'], data['k'])
        crypted = encrypt(message, public)

        message = json.dumps({'crypted': crypted})
        print('>> Bob send to Alice: ', message)
        conn.send(message.encode('utf-8'))
        conn.close()
        print('>> Bob said Goodbye')
