import socket
import time
import json

HOST = 'localhost'
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(3)
conn, addr = s.accept()
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
        #enviar = "prueba"
        #conn.send(enviar)
        i=0
        while i != 10:
            data = json.dumps({i: "palabra"})
            conn.send(data)
            i=+1
        #data = json.dumps({"0":"dato1", "1": "dato2", "2":"dato3"})
        #data2 = conn.recv(4096)
        #data2 = json.loads(data2.decode())
        #conn.send("Usted ha enviado: ")
        #print(data2.get("0"))
        #print("hola")
conn.close()
s.close()
