#Autor Julian chibuque barreto 
#Codigo: 20231005089

print(
  """
  ¡bienvenido! en este programa podra seleccionar una funcion para evaluar en el punto de su eleccion para ser calculado por medio de series de taylor
  
  ¿Que funcion desea realizar?
  
  1. exponencial
  2. cosenoidal 
  3. logaritmica
  
  """)

eleccion = int(input("que funcion desea calcular por medio de series de taylor:"))

def Exponencial(x, max_iter = 100):
    p = int(x)
    f = 1
    acc = 1
    for i in range(max_iter):
        d = p/f
        if d < 0.001:
            break
        acc = acc + d
        p = p*int(x)
        f = f*i
    return acc 

def coseno (x, max_iter= 100):
    p = x*x
    f = 2
    acc = 1 
    signo = -1
    n = 1
    for i in range(max_iter):
        d = p/f
        if d < 0.001:
            break
        acc = acc+d*signo
        p = p*x*x
        f = f*(2*n-1)*2*n
        signo = signo*-1
    return acc 

def logaritmica (x, max_iter):
    acc = 0
    p = x-1
    signo = 1 

    for i in range(max_iter):
        d = p/i
        if d < 0.001:
            break
        acc = acc+d*signo
        signo = signo*-1
        p=p*(x-1)
    return acc


def impresion(opcion):
    puntoX = float(input("muy bien, entonces dime en que punto deseas calcular la funcion:"))
    iteraciones = int(input("cuantas iteraciones deseas realizar, recuerda que no puede ser mas de 100:"))
    imprimir = True

    if opcion == 1:
        y = Exponencial(puntoX, iteraciones)
        func = "exponencial"
    elif opcion == 2:
        y = coseno(puntoX, iteraciones)
        func = "coseno"
    elif opcion == 3:
        y = logaritmica(puntoX, iteraciones)
        func = "logaritmica"
    else:
        print("el valor que se dijito es incorrecto")
        imprimir = False

    if imprimir:
        print("el resultado de evualuar la funcion "+func+" en el punto "+str(puntoX)+" da como resultado: "+str(y))

impresion(eleccion)
