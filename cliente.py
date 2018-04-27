from socket import *
from tkinter import *
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

def enviarPalabra():
    try:
        paquetes = []
        respuestas = []
        cadena = entry.get()
        cadena =  cadena.encode('utf-8')
        print(cadena)
        s.send(cadena)
        cadena = cadena.decode('ascii')
        if cadena=='get' or cadena=='obtain':
            i=0
            while i<10:
                
                paquetes.append(s.recv(4096))                
                paquete = json.loads(paquetes[len(paquetes)-1].decode())
                numero = paquete.get("numero")
                palabra = paquete.get("palabra")
                checksum = paquete.get("checksum")

                #Se hace el checksum de la palabra que llego
                acumulador=0
                for caracter in palabra:
                    caracterp = int(format(ord(caracter), 'b'),2)
                    acumulador = acumulador^caracterp
                inverso = ~acumulador & 0xFF
                resultado = format(inverso, 'b')

                if checksum == resultado:
                    respuesta = "El paquete ", numero, " es valido"
                    respuestas.append(respuesta)
                else:
                    respuesta = "Ha llegado la palabra ", palabra, " en la cabecera ", numero
                    respuestas.append(respuesta)
                i+=1
            imprimirRespuestas(respuestas)
        elif cadena == 'salir':
            s.close()
            ventana.destroy()
        else:
            Mensaje = s.recv(4096)
            print(Mensaje)
            respuestas.append("El servidor ha respondido: ")
            respuestas.append(Mensaje)
            imprimirRespuestas(respuestas)
    except timeout:
        respuestas.append("Se ha exedido el tiempo de espera")

        if len(paquetes) == 0:
            print("No hubo ninguna respuesta del servidor")
            respuestas.append("No hubo ninguna respuesta del servidor")
        #### El siguiente 'elif' imprimer los paquetes que hacen falta
        elif len(paquetes) !=0:
            i=0
            while i<(len(paquetes)-1):

                # Compara dos posiciones seguidas de la lista 'paquetes' en busqueda de algun paquete perdido
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
                        faltantes-=1
                i+=1
        imprimirRespuestas(respuestas)

def imprimirRespuestas(respuesta):
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
