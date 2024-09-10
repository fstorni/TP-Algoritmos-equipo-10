def crear_matriz(filas, columnas):
    """Crea una matriz vacía con el número de filas y columnas """
    return [[0] * columnas for filas in range(filas)]

def cargar_datos(matriz):
    """Carga datos de camiones en la matriz."""
    for i in range(len(matriz)):
        print(f"Ingresando datos para el camión {i + 1}:")
        codigo_camion = input("Ingrese el código del camión: ")
        nombre_transportista = input("Ingrese el nombre del transportista: ")
        material_transportar = input("Ingrese el material a transportar: ")
        ruta = input("Ingrese la ruta a transcurrir: ")
        
        # Asignar los datos a la fila correspondiente de la matriz
        matriz[i][0] = codigo_camion
        matriz[i][1] = nombre_transportista
        matriz[i][2] = material_transportar
        matriz[i][3] = ruta

def mostrar_datos(matriz):
    """Muestra todos los datos almacenados en la matriz con alineación adecuada."""
    print("\nDatos de los camiones:")
    print("\n")
    print(f"{'Camion':<20} {'Transportista':<20} {'Material':<20} {'Ruta':<20}")
    print("-" * 60)  # Línea separadora para mayor claridad

    for fila in matriz:
        print(f"{fila[0]:<20} {fila[1]:<20} {fila[2]:<20} {fila[3]:<20}")


def main():
    filas = 5 
    columnas = 4  

    # Crear matriz vacía
    matriz_camiones = crear_matriz(filas, columnas)

    # Cargar datos en la matriz
    cargar_datos(matriz_camiones)

    # Mostrar los datos almacenados
    mostrar_datos(matriz_camiones)

if __name__ == "__main__":
    main()


