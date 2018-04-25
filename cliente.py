

import socket, pickle
import json

HOST = 'localhost'
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#En HOST se coloca la IP de la maquina servidor
s.connect((HOST, PORT))

#Timeout de 2 segundos
s.settimeout(2.0)

while True:
    cadena = raw_input("Introduce el mensaje: ")
    cadena = cadena.encode('utf-8')
    s.send(cadena)
    #lista de paquetes
    paquetes = []

    if (cadena=="get"):

        #while para recibir los paquetes, tiene que ser exactamente 10
        #Se va revisando los paquetes uno por uno de acuerdo a su llegada
        while len(paquetes) != 10:
            #Los paquetes se van metiendo en la lista 'paquetes'
            paquetes.append(s.recv(4096))

            #Se decodifica el paquete 
            paquete = json.loads(paquetes[len(paquetes)-1].decode())
            palabra = paquete.get("palabra")
            palabra = palabra.encode("utf-8")
            checksum = paquete.get("checksum")
            checksum = checksum.encode("utf-8")

            #Se hace el checksum de la palabra que llegó
            acumulador=0
            for caracter in palabra:
                caracterp = int(format(ord(caracter), 'b'),2)
                acumulador = acumulador^caracterp
            inverso = ~acumulador & 0xFF
            resultado = format(inverso, 'b')

            #Se revisa si el checksum de la palabra es valido
            if checksum == resultado:
                print ("El paquete ", paquete.get("numero"), " es valido")
            else:
                print("El paquete ", paquete.get("numero"), " es invalido. Por favor intentelo de nuevo")

    if (cadena=="salir"):
        data = s.recv(4096)
        print(data)
        break
        s.close()
