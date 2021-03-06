import socket
import time
import json

###Las palabras en este proyecto no tienen tildes ni caracteres especiales por la codificacion ASCII

#Frase de 10 palabras que se va a enviar
frase = "este proxy no es malicioso y pasa la prueba bien"

#Lista para las palabras con numeracion y checksum
listaPalabras = []

#<---Inicio del checksum--->#
#Obtener el checksum de las palabras puestas en 'frase'
separacion= frase.split(" ")
for palabra in separacion:
    acumulador=0
    for caracter in palabra:
        caracterp = int(format(ord(caracter), 'b'),2)
        acumulador = acumulador^caracterp
    inverso = ~acumulador & 0xFF

    #se anade a la lista tres datos en notacion JSON, estos datos son: numero, palabra y checksum
    #Ejemplo: {"checksum": "11111000", "palabra": "este", "numero": 0}
    listaPalabras.append(json.dumps({"numero":len(listaPalabras),"palabra":palabra, "checksum": format(inverso,'b')}))
#<---Fin del checksum--->#

HOST = 'localhost'
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#En HOST se coloca la IP de este computador
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
        print ("Se enviaran las palabras")
        #Se envia las palabras colocaldas en 'listaPalabras'
        for LP in listaPalabras:
            conn.send(LP.encode())
            #Espera 0.2 segundos para que el cliente pueda hacer su proceso
            #Si no se hace, el cliente se sale por TimeOut
            time.sleep(0.2)

conn.close()
s.close()
