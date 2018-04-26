

from socket import *
import time
import socket, pickle
import json

HOST = 'localhost'
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#En HOST se coloca la IP de la maquina servidor
s.connect((HOST, PORT))

#Timeout de 2 segundos
s.settimeout(2.0)

#lista de paquetes
paquetes = []

while True:
    cadena = raw_input("Introduce el mensaje: ")
    cadena = cadena.encode('utf-8')
    s.send(cadena)
    #### 'get' realiza cambios a un paquete
    #### 'obtain' omite uno o mas paquetes
    if (cadena=="get" or cadena=="obtain"):
        paquetes = [] #Se reinicia la lista 'paquetes' cada vez que el usuario escriba 'get' o 'obtain'
        i=0
        try:
            #while para recibir los paquetes, tiene que ser exactamente 10
            while i != 10:
                #Los paquetes que llegan se van metiendo en la lista 'paquetes'
                paquetes.append(s.recv(4096))
                #Se decodifica el paquete
                paquete = json.loads(paquetes[len(paquetes)-1].decode())
                numero = paquete.get("numero")
                palabra = paquete.get("palabra")
                palabra = palabra.encode("utf-8")
                checksum = paquete.get("checksum")
                checksum = checksum.encode("utf-8")

                #Se hace el checksum de la palabra que llego
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
                i+=1
        #Excepcion en caso de TimeOut
        except timeout:
            print("El tiempo se ha acabado, la conexion se va a cerrar")

            ### La siguiente condicion verifica si ha faltado algun paquete antes de cerrar la comunicacion ###

            #Si 'paquetes' esta vacio, no hace nada
            if len(paquetes) == 0:
                print("No hubo ninguna respuesta del servidor")

            #### El siguiente 'elif' imprimer los paquetes que hacen falta
            elif len(paquetes) !=0:
                i=0
                while i<(len(paquetes)-1):

                    # Compara dos posiciones seguidas de la lista 'paquetes' en busqueda de algun paquete perdido
                    #Ejemplo:
                    #[0][hola][11110000]
                    #[1][mundo][10101010]
                    #[3][bello][00001111]
                    paquete = json.loads(paquetes[i].decode())
                    numero = paquete.get("numero")
                    paquete2 = json.loads(paquetes[i+1].decode())
                    numero2 = paquete2.get("numero")

                    #Si la diferencia entre las cabeceras es diferente de 1, se sabe que hay al menos un paquete que no llego
                    if (numero2 - numero)!=1:
                        faltantes = (numero2 - numero)-1
                        while faltantes!=0:
                            print ('No se ha encontrado la cabecera ', (i+faltantes))
                            faltantes-=1
                    i+=1
            # Espera 3 segundos antes de terminar
            time.sleep(3)
            break;
    if (cadena=="salir"):
        data = s.recv(4096)
        print(data)
        break
        s.close()
