
import socket, pickle
import json

HOST = 'localhost'
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.settimeout(10.0)
i=0
while True:
    cadena = raw_input("Introduce el mensaje: ")
    cadena = cadena.encode('utf-8')
    s.send(cadena)
    i+=1
    if (cadena=="get"):
        #data = "ome gonorrea ome, pablito escobar ome, aguante Nacional ome, Uribe el mejor presidente duelale a quien le duela ome"
        #data = json.dumps({"0":"dato1", "1": "dato2", "2":"dato3"})
        #s.send(data.encode())
    if (cadena=="salir"):
        data = s.recv(4096)
        print(data)
        break
        s.close()
