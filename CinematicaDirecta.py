#Julian Chibuque Barreto
#20231005089

import math 

def hallar_XY(a1, a2,a3,g2,g3):

    x2 = a2*math.sin(g2)
    y2 = a1*math.cos(g2)+a1

    r = math.pi-g3-g2

    x3 = a3*math.sin(r)+x2
    y3 =abs(a3*math.cos(r)-y2)

    return (x2,x3,y2,y3)

def main():
    print("bienvenido por favor digite los siguientes datos:")
    a1 = int(input("Digite el valor de la longitud de la primera parte del brazo"))
    a2 = int(input("Digite el valor de la longitud de la segunda parte del brazo"))
    a3 = int(input("Digite el valor de la longitud de la tercera parte del brazo"))

    g2 = float(input("Cual es el angulo entre la priemra y segunda parte del brazo"))
    g3=float(input("Digite cual el angulo entre la segunda y tercera parte del brazo"))

    impresion(hallar_XY(a1,a2,a3,g2,g3), a1)


def impresion(tupla, a1):
    print(f"la primera parte del brazo comienza en (0,0) y termina en (0,{a1})")
    print(f"la segunda parte del brazo comienza en (0,{a1}) y termina en ({tupla[0]},{tupla[2]}) ")
    print(f"la tercera parte del brazo comienza en ({tupla[0]},{tupla[2]})  y termina en ({tupla[1]},{tupla[3]}) ")

main()
