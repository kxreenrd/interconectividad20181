
from socket import *
from Tkinter import *
import time
import socket, pickle
import json

HOST = 'localhost'
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#En HOST se coloca la IP de la maquina proxy
s.connect((HOST, PORT))

#Timeout de 2 segundos
s.settimeout(2.0)

#lista de paquetes
paquetes = []
#Respuestas a los paquetes traidos por el servidor
respuestas = []

def enviarPalabra():
    hecho = False; #Variable para verificar que se hallan enviado los 10 paquetes
    while hecho == False:
        cadena = entry.get()
        cadena = cadena.encode('utf-8')
        s.send(cadena)
        #### 'get' realiza cambios a un paquete
        #### 'obtain' omite uno o mas paquetes
        if (cadena=="get" or cadena=="obtain"):
            paquetes = [] #Se reinicia la lista 'paquetes' cada vez que el usuario escriba 'get' o 'obtain'
            respuestas = [] #Lista de mensajes hechos por el cliente ante los paquetes entrantes
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
                        respuesta = "El paquete ", paquete.get("numero"), " es valido"
                        respuestas.append(respuesta)
                        print ("El paquete ", paquete.get("numero"), " es valido")
                    else:
                        respuesta = "El paquete ", paquete.get("numero"), " es invalido. La palabra encontrada fue " , paquete.get("palabra")
                        respuestas.append(respuesta)
                        print("El paquete ", paquete.get("numero"), " es invalido. Por favor intentelo de nuevo")
                    i+=1
                #Se imprimen las respuestas de los mensajes
                abrir(respuestas)
                hecho = True #Si han llegado los 10 paquetes, se sale del ciclo

            ######Excepcion en caso de TimeOut#####
            except timeout:

                print("El tiempo se ha acabado")
                respuestas.append("El tiempo se ha acabado")
                ### La siguiente condicion verifica si ha faltado algun paquete antes de cerrar la comunicacion ###

                #Si 'paquetes' esta vacio, quiere decir que el servidor no respondio nada
                if len(paquetes) == 0:
                    print("No hubo ninguna respuesta del servidor")
                    respuestas.append("No hubo ninguna respuesta del servidor")
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
                                respuesta = 'No se ha encontrado la cabecera ', (i+faltantes)
                                respuestas.append(respuesta)
                                print ('No se ha encontrado la cabecera ', (i+faltantes))
                                faltantes-=1
                        i+=1
                # Espera 3 segundos antes de terminar
                abrir(respuestas)
                time.sleep(3)
                break;
        elif (cadena=="salir"):
            #Se mostrara en una ventana la respuesta cuando se escribe la palabra 'salir'
            data = s.recv(4096)
            respuestas = []
            respuestas.append("El servidor ha respondido: ")
            respuestas.append(data)
            respuestas.append("La conexion se ha cerrado")
            respuestas.append("El programa dejara de funcionar")
            abrir(respuestas)
            s.close()
            break
        else:
            data = s.recv(4096)
            respuestas = []
            respuestas.append("El servidor ha respondido: ")
            respuestas.append(data)
            abrir(respuestas)
            hecho = True

########################### Interfaz Grafica ###########################

#Metodo que abre una ventana con la informacion de los paquetes recibidos
def abrir(respuesta):
    #Para mostrar los mensajes, se usa una lista llamada 'labels'
    labels = []
    Respuestas = Tk()
    Respuestas.title("Respuesta del servidor")

    #Se crean los mensajes para mostrar
    for res in respuesta:
        labels.append(Label(Respuestas, text=res))

    #Se anaden los mensajes a la ventana
    for label in labels:
        label.pack()
    Respuestas.mainloop()


#Ventana principal, desde aqui se envian los mensajes
ventana = Tk()

#Se crean todos los elementos que se anadiran a la ventana principal
title = Label(ventana, text="Protocolo de comunicacion", font=("Helvetica", 16))
label = Label(ventana, text="\nEl objetivo de este proyecto es implementar un protocolo de comunicacion entre dos \nmaquinas, con otra de por medio actuando como proxy malicioso. \nLos mensajes pueden ser 'get', 'obtain' , 'salir'")
mensaje= Label(ventana, text="\nPor favor ingrese el mensaje")
entry = Entry(ventana, width="30")
espacio = Label(ventana, text="\n\n")
button = Button(ventana, text="Aceptar", width="30", height="2", command=enviarPalabra)
integrantes = Label(ventana, text="\n\n\(*o*)/ INTEGRANTES \(*o*)/\nAngelica Cuesta\nFabian Miranda\nKaren Rodriguez")

#Se configura la ventana principal
ventana.geometry('500x400')
ventana.title("Protocolo de comunicacion")

#Se anaden los elementos a la ventana principal
title.pack()
label.pack()
mensaje.pack()
entry.pack()
espacio.pack()
button.pack()
integrantes.pack()

#Se muestra
ventana.mainloop()

#########################################################################
