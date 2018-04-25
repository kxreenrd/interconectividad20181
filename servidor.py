import socket
import time
import json

frase = "este proxy no es malicioso y pasa la prueba bien"
HOST = 'localhost'
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('10.8.8.57', PORT))
s.listen(3)
conn, addr = s.accept()
#Lista para las palabras con checksum
listaPalabras = []

print ('Connected by', addr)
while True:
    data = conn.recv(4096)
    data = data.decode("ascii")
    print(data)
    if (data == "salir"):
        conn.send(data)
        print ("Adios")
        conn.close()
        break

    if (data == "get"):
        enviar = "prueba"
        enviar = enviar.encode('utf-8')
        conn.send(enviar)

conn.close()
s.close()

