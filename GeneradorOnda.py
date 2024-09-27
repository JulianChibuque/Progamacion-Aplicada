import math
#Julian Chibque Barreto
#20231005089

# Menú de selección
def mostrar_menu():
    print("Bienvenido al menú del generador de onda")
    print("""
          1. Onda cuadrada
          2. Onda diente de sierra
          """)

# Función para generar una onda cuadrada
def OndaCuadrada(tiempo, frecuencia, amplitud):
    periodo = 1 / frecuencia  # Calcular el periodo de la onda
    tiempo_normalizado = tiempo % periodo  # Asegurarse de que esté dentro de un ciclo
    if tiempo_normalizado < (periodo / 2):
        return amplitud  # Valor alto
    else:
        return -amplitud  # Valor bajo


# Función para evaluar la elección del usuario
def evaluar_eleccion(eleccion, tiempo, frecuencia, amplitud):
    if eleccion == 1:
        voltaje = OndaCuadrada(tiempo, frecuencia, amplitud)
        tipo_onda = "Onda cuadrada"
    else:
        print("La elección no es válida.")
        return None, None
    
    return voltaje, tipo_onda

# Programa principal
def main():
    mostrar_menu()
    eleccion = int(input("Digite el número del menú que desea elegir: "))
    tiempo = float(input("Ingrese el tiempo en el cual desea calcular el valor del voltaje: "))
    frecuencia = float(input("Ingrese la frecuencia de la onda (Hz): "))
    amplitud = float(input("Ingrese la amplitud de la onda: "))

    # Evaluar la elección del usuario
    voltaje, tipo_onda = evaluar_eleccion(eleccion, tiempo, frecuencia, amplitud)
    
    # Mostrar el resultado si la elección es válida
    if voltaje is not None:
        print(f"El valor del voltaje en t={tiempo} para la {tipo_onda} es: {voltaje} V")

# Ejecutar el programa principal
main()
