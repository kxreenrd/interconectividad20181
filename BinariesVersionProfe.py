import sys

frase = "estamos escribiendo con rutinas en python"
separacion= frase.split(" ")


for palabra in separacion:
    acumulador=0
    for caracter in palabra:
        caracterp = int(format(ord(caracter), 'b'),2)
        acumulador = acumulador^caracterp
    inverso = ~acumulador & 0xFF
    print(palabra,format(inverso, 'b'))
% e -> 01100101
% n -> 01101110
%      00001011
%      11110100
