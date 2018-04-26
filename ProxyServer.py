import socket
import time
import json
from random import randint

#Proyecto de prueba para demostrar un proxy CORRUPTO HP


####### CASO OMISO A ESTO #######
listaPalabras = []
listaPalabras.append(json.dumps({'checksum': '11111000', 'numero': 0, 'palabra': 'este'}))
listaPalabras.append(json.dumps({'checksum': '10010011', 'numero': 1, 'palabra': 'proxy'}))
listaPalabras.append(json.dumps({'checksum': '11111110', 'numero': 2, 'palabra': 'no'}))
listaPalabras.append(json.dumps({'checksum': '11101001', 'numero': 3, 'palabra': 'es'}))
listaPalabras.append(json.dumps({'checksum': '10001111', 'numero': 4, 'palabra': 'malicioso'}))
listaPalabras.append(json.dumps({'checksum': '10000110', 'numero': 5, 'palabra': 'y'}))
listaPalabras.append(json.dumps({'checksum': '11111100', 'numero': 6, 'palabra': 'pasa'}))
listaPalabras.append(json.dumps({'checksum': '11110010', 'numero': 7, 'palabra': 'la'}))
listaPalabras.append(json.dumps({'checksum': '11101110', 'numero': 8, 'palabra': 'prueba'}))
listaPalabras.append(json.dumps({'checksum': '11111111', 'numero': 9, 'palabra': 'bien'}))

for LP in listaPalabras:
    LP = LP.encode()
##################################

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
    if data == "obtain":
        ########################### OMITIR PAQUETE ###########################
        #--------------------------------------------------------------------#
        #Se elige un numero al azar entre 0 y 9 para buscarlo en la lista de palabras
        azar = randint(0,9)
        i=0
        #Bucle para recibir y enviar los datos que el servidor envio
        while i<len(listaPalabras):
            #Se elige un paquete para que no sea enviado
            if i == azar:
                i+=1
            #En caso contrario, se envia el paquete
            else:
                conn.send(listaPalabras[i].encode())
                time.sleep(0.2) #Se necesita esperar para que el cliente pueda hacer su logica
                i+=1
        ######################################################################

    if data == "get":
        ######################### MODIFICAR PAQUETE #########################
        #-------------------------------------------------------------------#
        #Se elige un numero al azar entre 0 y 9 para buscarlo en la lista de palabras
        azar = randint(0,9)
        i=0
        #Bucle para recibir y enviar los datos que el servidor envio
        while i<len(listaPalabras):
            #Envia una palabra diferente segun una posicion dada
            if i == azar:
                paquete = json.loads(listaPalabras[azar])
                numero = paquete.get("numero")
                checksum = paquete.get("checksum")
                checksum = checksum.encode("utf-8")
                #Envia la palabra 'corrupto'. Los demas datos son iguales
                corrupto = json.dumps({'numero': numero, 'palabra': 'corrupto', 'checksum': checksum})
                conn.send(corrupto.encode())
                time.sleep(0.2) #Se necesita esperar para que el cliente pueda hacer su logica
            else:
                conn.send(listaPalabras[i].encode())
                time.sleep(0.2) #Se necesita esperar para que el cliente pueda hacer su logica
            i+=1
        ######################################################################
