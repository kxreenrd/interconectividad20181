

import socket, pickle
import json

HOST = 'localhost'
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('10.8.8.58', PORT))
s.settimeout(10.0)
i=0
while True:
    cadena = input("Introduce el mensaje: ")
    cadena = cadena.encode('utf-8')
    s.send(cadena)
    palabras = []
    i=0
    #while para recivir las palabras
    while i!=2:
        palabras.append(s.recv(4096))
        i=+1

    #data = s.recv(4096)
    #data = data.decode('ascii')
    #print(data)
    if (cadena=="get"):
        data = s.recv(4096)
        print(data)
    if (cadena=="salir"):
        data = s.recv(4096)
        print(data)
        break
        s.close()
