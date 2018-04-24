import socket
HOST = 'localhost'
PORT = 50007

#Socket de cliente
sC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sC.connect((HOST, PORT))
#Supongo que aquí se coloca la dirección del servidor
#El proxy actua como cliente ante el servidor

#Socket de servidor
sS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sS.bind((HOST, PORT))
#Y aquí el del cliente
#El proxy actua como servidor ante el cliente
sS.listen(3)

while True:
    #Se supone que se tiene que escuchar al cliente
    data = conn.recv(4096)
    data = data.decode("ascii")
    #Si el cliente envia la palabra get
    if (data == "get"):
        obtener = "get"
        obtener = obtener.encode('utf-8')
        #Se envia la palabra get al servidor
        sC.send(obtener)
        #Se recibe y se decodifica el paquete que el servido envia 
        paquete = sS.recv(4096)
