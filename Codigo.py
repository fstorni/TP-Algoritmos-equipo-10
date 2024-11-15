import re
import json 


# Diccionario de rutas inicial
Rutas = {
    'ruta1': {'origen': 'Buenos Aires', 'destino': 'Mendoza'},
    'ruta2': {'origen': 'Buenos Aires', 'destino': 'Córdoba'},
    'ruta3': {'origen': 'Buenos Aires', 'destino': 'Entre Ríos'}
}

def guardar_rutas_json(rutas, archivo='rutas.json'):
    """Guarda las rutas en un archivo JSON sin codificar caracteres especiales."""
    try:
        with open(archivo, 'w', encoding='utf-8') as file:
            json.dump(rutas, file, indent=4, ensure_ascii=False)
        print(f"Rutas guardadas en {archivo}.")
    except Exception as e:
        print(f"Error al guardar las rutas: {e}")


# Función para cargar rutas desde archivo JSON
def cargar_rutas_json(archivo='rutas.json'):
    """Carga las rutas desde un archivo JSON."""
    try:
        with open(archivo, 'r') as file:
            rutas = json.load(file)
        print(f"Rutas cargadas desde {archivo}.")
        return rutas
    except FileNotFoundError:
        print(f"No se encontró el archivo {archivo}. Se usará el diccionario de rutas predeterminado.")
        return Rutas
    except json.JSONDecodeError:
        print("Error: El archivo JSON está corrupto o malformado.")
        return Rutas
    except Exception as e:
        print(f"Error al cargar las rutas: {e}")
        return Rutas

def mostrar_rutas(rutas):
    """Muestra las rutas actuales."""
    print("\nRutas actuales:")
    for ruta_id, datos in rutas.items():
        print(f"{ruta_id}: Origen - {datos['origen']}, Destino - {datos['destino']}")

def actualizar_ruta(rutas):
    """Actualiza una ruta existente."""
    print("\nRutas disponibles para actualizar:")
    mostrar_rutas(rutas)
    actualizar_ruta = input("Ingrese el código de la ruta a actualizar (ej: ruta1): ").strip().lower()

    if actualizar_ruta in rutas:
        nuevo_origen = input(f"Ingrese el nuevo origen para la {actualizar_ruta}: ").strip()
        nuevo_destino = input(f"Ingrese el nuevo destino para la {actualizar_ruta}: ").strip()
        rutas[actualizar_ruta] = {'origen': nuevo_origen, 'destino': nuevo_destino}
        print(f"Ruta {actualizar_ruta} actualizada a Origen: {nuevo_origen}, Destino: {nuevo_destino}.")
    else:
        print("Error: El código de ruta no existe.")

def agregar_ruta(rutas):
    """Agrega una nueva ruta."""
    nuevo_codigo = input("Ingrese el código para la nueva ruta (ej: ruta4): ").strip().lower()
    if nuevo_codigo in rutas:
        print("Error: El código de ruta ya existe.")
    else:
        nuevo_origen = input("Ingrese el origen para la nueva ruta: ").strip()
        nuevo_destino = input("Ingrese el destino para la nueva ruta: ").strip()
        rutas[nuevo_codigo] = {'origen': nuevo_origen, 'destino': nuevo_destino}
        print(f"Nueva ruta agregada: {nuevo_codigo} -> Origen: {nuevo_origen}, Destino: {nuevo_destino}")

def gestionar_rutas(rutas):
    """Permite al usuario actualizar o agregar rutas al diccionario de rutas."""
    bandera = True
    while bandera:
        print("\nOpciones para gestionar rutas:")
        print("1. Ver rutas actuales")
        print("2. Actualizar una ruta existente")
        print("3. Agregar una nueva ruta")
        print("4. Guardar y salir de gestión de rutas")
        opcion = input("Seleccione una opción (1-4): ")

        if opcion == '1':
            mostrar_rutas(rutas)
        elif opcion == '2':
            actualizar_ruta(rutas)
        elif opcion == '3':
            agregar_ruta(rutas)
        elif opcion == '4':
            guardar_rutas_json(rutas)
            print("Saliendo de la gestión de rutas.")
            bandera = False
        else:
            print("Opción no válida. Por favor, intente de nuevo.")
    return rutas


def cargar_datos_camiones():
    """Carga datos de los camiones en una lista de diccionarios, validando la patente."""
    camiones = []
    bandera = True

    while bandera:
        es_patente_valida = False
        while not es_patente_valida:
            patente_camion = input("Ingrese la patente del camión (formato 'AB 123 CD'): ").strip().upper()
            if re.match(r"^[A-Z]{2} \d{3} [A-Z]{2}$", patente_camion):
                es_patente_valida = True  
            else:
                print("Error: La patente debe tener el formato 'AB 123 CD'.")

        nombre_transportista = input("Ingrese el nombre del transportista: ")
        
        material_transportar = input("Ingrese el material a transportar: ")
        while not material_transportar.isalpha():
            print("Error: El material debe ser una cadena de caracteres.")
            material_transportar = input("Ingrese el material a transportar: ")

        cantidad_material = int(input("Cuántos kg se van a transportar de ese material? "))
        while cantidad_material <= 0:
            print("Error: La cantidad a transportar debe ser un número positivo.")
            cantidad_material = int(input("Cuántos kg se van a transportar de ese material? "))

        camiones.append({
            'patente': patente_camion,
            'nombre_transportista': nombre_transportista,
            'material': material_transportar,
            'cantidad': cantidad_material,
            'rutas': [] 
        })

        continuar = input("¿Desea ingresar otro camión? (s/n): ").lower()
        bandera = continuar != 'n'
    
    return camiones



def cargar_rutas(camiones, rutas_disponibles):
    """Carga las rutas para cada camión para cada día de la semana."""
    dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]

    for codigo_camion, datos_camion in camiones.items():
        print(f"\nCargando rutas para el camión {codigo_camion} ({datos_camion['nombre_transportista']}):")

        for dia in dias_semana:
            ruta = input(f"Ingrese la ruta para el {dia} (o deje vacío si no hay ruta): ").strip().lower()
            if ruta in rutas_disponibles.keys() or not ruta:
                datos_camion['rutas'][dia] = ruta if ruta else "Sin viaje"
            else:
                print(f"La ruta {ruta} no es válida.")
    return camiones

def crear_matriz_rutas(dias, camiones):
    """Crea una matriz de rutas, solo para almacenar las rutas de cada día y camión."""
    return [["" for camion in range(len(camiones))] for dia in range(dias)]

def cargar_matriz_rutas(matriz, camiones):
    """Llena la matriz de rutas con las rutas que deben transitar los camiones cada día."""
    dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    for i, dia in enumerate(dias_semana):
        for j, (codigo_camion, datos_camion) in enumerate(camiones.items()):
            matriz[i][j] = datos_camion['rutas'].get(dia, "Sin viaje")
    return matriz

def verificar_rutas(camiones):
    """Verifica si hay rutas repetidas entre los camiones y permite reprogramar rutas en caso de repetición."""
    dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]

    for dia in dias_semana:
        rutas_dia = {}
        repetir = True

        while repetir:
            repetir = False
            rutas_dia.clear()

            for codigo_camion, datos_camion in camiones.items():
                ruta = datos_camion['rutas'][dia]

                if ruta in rutas_dia and ruta != "Sin viaje":
                    print(f"\n¡Repetición detectada el {dia} en la ruta {ruta} entre los camiones {codigo_camion} y {rutas_dia[ruta]}!")
                    
                    camion_reprogramado = False  
                    
                    while not camion_reprogramado:
                        reprogramar_camion = input(f"¿Qué camión desea reprogramar, {codigo_camion} o {rutas_dia[ruta]}? ").strip()
                        if reprogramar_camion in [codigo_camion, rutas_dia[ruta]]:
                            nuevo_destino = input(f"Ingrese el nuevo destino para el camión {reprogramar_camion}: ").strip().lower()
                            camiones[reprogramar_camion]['rutas'][dia] = nuevo_destino
                            print(f"Ruta del camión {reprogramar_camion} reprogramada a {nuevo_destino} para el {dia}.")
                            repetir = True 
                            camion_reprogramado = True  
                        else:
                            print("Error: Código de camión no válido. Intente nuevamente.")
                else:
                    rutas_dia[ruta] = codigo_camion  

    return camiones

def gestionar_stock(camiones, stock_actual):
    """Calcula el total de material transportado y verifica si hay faltante para los próximos viajes."""
    
    material_total = sum(map(lambda datos_camion: datos_camion['cantidad'], camiones.values()))

    if material_total > stock_actual:
        print(f"Alerta: Se transportarán {material_total} kg, pero el stock disponible es de {stock_actual} kg.")
    else:
        print(f"Todo en orden. Se transportarán {material_total} kg, y hay {stock_actual} kg disponibles.")
    return material_total

def mostrar_matriz_rutas(matriz, camiones):
    """Muestra la matriz de rutas de manera legible."""
    dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    print("\nMatriz de rutas:")
    print(f"{'Dia':<15} " + " ".join([f"{codigo_camion:<15}" for codigo_camion in camiones.keys()]))
    print("-" * (15 + 15 * len(camiones)))

    for i, dia in enumerate(dias_semana):
        print(f"{dia:<15} " + " ".join([f"{matriz[i][j]:<15}" for j in range(len(camiones))]))

def mostrar_datos_camiones(camiones):
    """Muestra todos los datos de los camiones en formato de tabla."""
    print("\nDatos de los camiones:")
    print("\n")
    print(f"{'Patente':<10} {'Transportista':<20} {'Material':<15} {'Cantidad (kg)':<15}")
    print("-" * 60)

    for camion in camiones:
        print(f"{camion['patente']:<10} {camion['nombre_transportista']:<20} {camion['material']:<15} {camion['cantidad']:<15}")


def menu_principal():
    """Muestra el menú principal y ejecuta la acción seleccionada por el usuario."""
    # Intentar cargar rutas desde el archivo JSON al iniciar
    rutas = cargar_rutas_json()

    camiones = {}  # Asumiendo que esta función está definida
    matriz_rutas = []
    continuar = True  

    while continuar:
        print("\n--- Menú Principal ---")
        print("1. Gestionar rutas")
        print("2. Cargar datos de camiones")
        print("3. Cargar rutas para camiones")
        print("4. Mostrar datos de camiones")
        print("5. Mostrar matriz de rutas")
        print("6. Verificar rutas")
        print("7. Gestionar stock")
        print("8. Salir")
        
        opcion = input("Seleccione una opción (1-8): ")

        if opcion == '1':
            rutas = gestionar_rutas(rutas)

        elif opcion == '2':
            camiones = cargar_datos_camiones()
        elif opcion == '3':
            if camiones:
                camiones = cargar_rutas(camiones, rutas)
                matriz_rutas = crear_matriz_rutas(5, camiones)
                matriz_rutas = cargar_matriz_rutas(matriz_rutas, camiones)
            else:
                print("Primero debe cargar los datos de los camiones.")
        elif opcion == '4':
            if camiones:
                mostrar_datos_camiones(camiones)
            else:
                print("Primero debe cargar los datos de los camiones.")
        elif opcion == '5':
            if matriz_rutas:
                mostrar_matriz_rutas(matriz_rutas, camiones)
            else:
                print("Primero debe cargar las rutas de los camiones.")
        elif opcion == '6':
            if camiones:
                verificar_rutas(camiones)
            else:
                print("Primero debe cargar los datos de los camiones.")
        elif opcion == '7':
            if camiones:
                stock_disponible = 1000  # Definir stock disponible
                gestionar_stock(camiones, stock_disponible)
            else:
                print("Primero debe cargar los datos de los camiones.")
        elif opcion == '8':
            print("Saliendo del sistema. ¡Adiós!")
            continuar = False  
        else:
            print("Opción no válida, intente nuevamente.")

# Programa principal
menu_principal()
