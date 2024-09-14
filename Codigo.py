#Falta desarrollas funciones con respecto a sotck
#falta ultimoas impresiones (matrices finales)
#se necesita aclarar codigo de ruta 
#agregar docstrings o comentarios 




# Diccionario de rutas inicial
Rutas = {
    'Ruta1': 'Mendoza',
    'Ruta2': 'Córdoba',
    'Ruta3': 'Entre Ríos'
}

def gestionar_rutas():
    """Permite al usuario actualizar o agregar rutas al diccionario de rutas."""
    while True:
        print("\nOpciones para gestionar rutas:")
        print("1. Ver rutas actuales")
        print("2. Actualizar una ruta existente")
        print("3. Agregar una nueva ruta")
        print("4. Terminar gestión de rutas")
        opcion = input("Seleccione una opción (1-4): ")

        if opcion == '1':
            # Mostrar rutas actuales
            print("\nRutas actuales:")
            for ruta_id, destino in Rutas.items():
                print(f"{ruta_id}: {destino}")

        elif opcion == '2':
            # Actualizar una ruta existente
            print("\nRutas disponibles para actualizar:")
            for ruta_id, destino in Rutas.items():
                print(f"{ruta_id}: {destino}")
            actualizar_ruta = input("Ingrese el código de la ruta a actualizar: ")

            if actualizar_ruta in Rutas:
                nuevo_destino = input(f"Ingrese el nuevo destino para la {actualizar_ruta}: ")
                Rutas[actualizar_ruta] = nuevo_destino
                print(f"Ruta {actualizar_ruta} actualizada a {nuevo_destino}.")
            else:
                print("Error: El código de ruta no existe.")

        elif opcion == '3':
            # Agregar una nueva ruta
            nuevo_codigo = input("Ingrese el código para la nueva ruta (ej: Ruta4): ")
            if nuevo_codigo in Rutas:
                print("Error: El código de ruta ya existe.")
            else:
                nuevo_destino = input("Ingrese el destino para la nueva ruta: ")
                Rutas[nuevo_codigo] = nuevo_destino
                print(f"Nueva ruta agregada: {nuevo_codigo} -> {nuevo_destino}")

        elif opcion == '4':
            # Terminar la gestión de rutas
            print("Saliendo de la gestión de rutas.")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")
            
def cargar_datos_camiones():
    """Carga datos de los camiones en un diccionario."""
    camiones = {}  # Diccionario para almacenar la información de los camiones

    while True:
        codigo_camion = input("Ingrese el código del camión: ")

        # Validar que el código sea un número positivo
        while not codigo_camion.isdigit() or int(codigo_camion) < 0:
            print("Error: El código del camión debe ser un número positivo.")
            codigo_camion=input("Ingrese el código del camión: ")

        nombre_transportista=input("Ingrese el nombre del transportista: ")

        material_transportar=input("Ingrese el material a transportar: ")
        while not material_transportar.isalpha():
            print("Error: El material debe ser una cadena de caracteres.")
            material_transportar=input("Ingrese el material a transportar: ")
            
        cantidad_material=int(input("Cuantos kg se van a transportar de ese material?"))
        while not codigo_camion.isdigit() or int(codigo_camion) < 0:
            print("Error: La cantidad a transportar debe ser un número positivo.")
            codigo_camion=input("Cuantos kg se van a transportar de ese material? ")

        # Crear un diccionario con los datos del camión
        camiones[codigo_camion] = {
            'nombre_transportista': nombre_transportista,
            'material': material_transportar,
            'cantidad':cantidad_material,
            'rutas': {}  
        }
        
        # Preguntar si desea ingresar otro camión
        continuar = input("¿Desea ingresar otro camión? (s/n): ").lower()
        if continuar == 'n':
            break
            
    return camiones 
    

def cargar_rutas(camiones):
    """Carga las rutas para cada camión para cada día de la semana."""
    dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]

    for codigo_camion, datos_camion in camiones.items():
        print(f"\nCargando rutas para el camión {codigo_camion} ({datos_camion['nombre_transportista']}):")

        for dia in dias_semana:
            ruta = input(f"Ingrese la ruta para el {dia} (o deje vacío si no hay ruta): ")
            datos_camion['rutas'][dia] = ruta if ruta else "Sin viaje"  # Guarda la ruta o "Sin viaje" si está vacío


def crear_matriz_rutas(dias, camiones):
    """Crea una matriz de rutas, solo para almacenar las rutas de cada día y camión."""
    return [["" for i in range(len(camiones))] for i in range(dias)]


def cargar_matriz_rutas(matriz, camiones):
    """Llena la matriz de rutas con las rutas que deben transitar los camiones cada día."""
    dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    pass

def verificar_rutas(rutas):
    pass

def carga_stock():
    pass


def faltante_stock():
    pass

def 


# Programa principal
def main():
    print("Bienvenido al sistema de gestión de camiones.")
    gestionar_rutas()
    camiones = cargar_datos_camiones()
    cargar_rutas(camiones)

    matriz_rutas = crear_matriz_rutas(5, camiones)
    cargar_matriz_rutas(matriz_rutas, camiones)

    

main()

