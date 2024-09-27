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

def Exponencial(x, max_iter=100):
    acc = 1  # Comienza en 1 porque el primer término es 1 (x^0/0!)
    factorial = 1
    for i in range(1, max_iter):
        factorial *= i  # Calcula el factorial en cada iteración
        term = x**i / factorial  # Calcula el siguiente término de la serie
        if abs(term) < 0.001:  # Condición de convergencia
            break
        acc += term  # Suma el término al acumulador
    return acc


def coseno(x, max_iter=100):
    acc = 1  # Primer término es 1
    factorial = 1
    signo = -1
    for i in range(1, max_iter):
        factorial *= (2 * i) * (2 * i - 1)  # Factorial para el término
        term = (x**(2 * i)) / factorial  # x^(2n) / (2n)!
        if abs(term) < 0.001:  # Condición de convergencia
            break
        acc += signo * term  # Alterna el signo
        signo *= -1  # Cambia el signo
    return acc

def logaritmica(x, max_iter=100):
    if x <= 0:  # El logaritmo natural no está definido para x <= 0
        return float('nan')
    if x == 1:
        return 0  # log(1) = 0
    acc = 0
    term = (x - 1) / x  # Primer término
    for i in range(1, max_iter):
        acc += (term**i) / i * (-1 if i % 2 == 0 else 1)  # Alterna el signo
        if abs((term**i) / i) < 0.001:
            break
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
