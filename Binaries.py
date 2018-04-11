
#No hay tildes porque me sale error :(

#El siguiente metodo obtiene la suma de los caracteres en binario de una palabra
#Se suma de la siguiente manera:
# 0 + 0 = 0
# 1 + 1 = 0
# 0 + 1 = 1
#Al resultado se le hace una negacion (Se invierte)

# EJ: "hola" h -> 01101000, o -> 01101111, l -> 01101100, a -> 01100001
# 01101000 + 01101111 = 00000111
# 00000111 + 01101100 = 01101011
# 01101011 + 01100001 = 00001010 <- Resultado
# Negacion: 11110101

def getChecksum(word):
    binaries = []
    sum = ""
    #Transforma los caracteres en binarios y los anade al array 'binaries'
    for i in word:
        binary = bin(ord(i))
        binary = binary.replace('b', '')
        print(binary)
        binaries.append(binary)

    sum = binaries[0] #La suma comienza desde el primer dato en 'binaries'
    var = 1 #Comienza en 1 para tomar el segundo dato en 'binaries'

    #Realiza la suma de todos los datos en 'binaries' y lo guarda en la variable 'sum'
    while var < len(binaries):
        auxsum = ""
        char = 7 #Porque hay 8 bytes por cada caracter en binario
        while char >= 0:
            if sum[char] == binaries[var][char]:
                auxsum = "0" + auxsum
            else:
                auxsum = "1" + auxsum
            char-=1
        sum = auxsum
        var+=1

    naturals = list(sum) #Lista de numeros en 'sum'
    Checksum = ""

    #Hace la negacion invirtiendo los numeros en la lista 'naturals' y lo guarda en la variable 'Checksum'
    for i in naturals:
        if i == "1":
            Checksum = Checksum + "0"
        else:
            Checksum = Checksum + "1"

    #Resultado final
    print(Checksum)
    return Checksum

#Ejemplo de uso
getChecksum("hola")
