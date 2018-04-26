import socket
import time
import json
from random import randint

HOST = 'localhost'
PORT = 50007

#<---Socket de cliente--->#
sC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sC.connect(('10.8.8.57', PORT))
#Aqui se coloca la direccion del servidor
#El proxy actua como cliente ante el servidor

#<---Socket de servidor--->#
sS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sS.bind(('10.8.8.58', PORT))
#Aqui se coloca la direccion del cliente
#El proxy actua como servidor ante el cliente
sS.listen(3)
conn, addr = sS.accept()
print ('Connected by', addr)

while True:
    #Se escucha al cliente
    data = conn.recv(4096)
    data = data.decode("ascii")
    print(data)

    #Si el cliente envia la palabra get se modificara una palabra
    if (data == "get"):
        obtener = "get"
        obtener = obtener.encode('utf-8')
        #Se envia la palabra get al servidor
        sC.send(obtener)

        ######################### MODIFICAR PAQUETE #########################
        #-------------------------------------------------------------------#
        #Se elige un numero al azar entre 0 y 9 para modificarlo eventualmente
        azar = randint(0,9)
        i=0
        #Bucle para recibir y enviar los datos que el servidor envio
        while i!=10:
            PaqueteRecibido = sC.recv(4096)
            #Envia una palabra diferente segun una posicion dada
            if i == azar:
                paquete = json.loads(PaqueteRecibido)
                numero = paquete.get("numero")
                checksum = paquete.get("checksum")
                checksum = checksum.encode("utf-8")
                #Envia la palabra 'corrupto'. Los demas datos son iguales
                corrupto = json.dumps({'numero': numero, 'palabra': 'corrupto', 'checksum': checksum})
                conn.send(corrupto.encode())
                time.sleep(0.2) #Se necesita esperar para que el cliente pueda hacer su logica
            else:
                conn.send(PaqueteRecibido)
                time.sleep(0.2) #Se necesita esperar para que el cliente pueda hacer su logica
            i+=1
        ######################################################################

    #Si el cliente envia la palabra obtain se omitira un paquete
    if (data == "obtain"):
        obtener = "get"
        obtener = obtener.encode('utf-8')
        #Se envia la palabra get al servidor
        sC.send(obtener)

        ########################### OMITIR PAQUETE ###########################
        #--------------------------------------------------------------------#
        #Se elige un numero al azar entre 0 y 9 para no enviarlo
        azar = randint(0,9)
        i=0
        #Bucle para recibir y enviar los datos que el servidor envio
        while i!=10:

            if i == azar: #Se elige un paquete para que no sea enviado
                i+=1

            else: #En caso contrario, se envia el paquete
                paquete = sC.recv(4096)
                conn.send(paquete)
                time.sleep(0.2) #Se necesita esperar para que el cliente pueda hacer su logica
                i+=1
        ######################################################################

    #Si el cliente escribe 'salir' cierra las conexiones
    if (data == "salir"):
        salir = "salir"
        salir = salir.encode('utf-8')
        sS.send(salir)
        sC.close()
        conn.close()
        break
