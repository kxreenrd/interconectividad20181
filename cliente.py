

import socket, pickle
import json

HOST = 'localhost'
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('10.8.8.59', PORT))
s.settimeout(10.0)
i=0
while True:
    cadena = input("Introduce el mensaje: ")
    cadena = cadena.encode('utf-8')
    s.send(cadena)
    i+=1
    if (cadena=="get"):
        print("hola")
    if (cadena=="salir"):
        data = s.recv(4096)
        print(data)
        break
        s.close()

