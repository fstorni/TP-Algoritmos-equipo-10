# Diccionario de rutas inicial
Rutas = {
    'ruta1': 'Mendoza',
    'ruta2': 'Córdoba',
    'ruta3': 'Entre Ríos'
}

def gestionar_rutas(rutas):
    """Permite al usuario actualizar o agregar rutas al diccionario de rutas."""
    bandera = True
    while bandera:
        print("\nOpciones para gestionar rutas:")
        print("1. Ver rutas actuales")
        print("2. Actualizar una ruta existente")
        print("3. Agregar una nueva ruta")
        print("4. Terminar gestión de rutas")
        opcion = input("Seleccione una opción (1-4): ")

        if opcion == '1':
            # Mostrar rutas actuales
            print("\nRutas actuales:")
            for ruta_id, destino in rutas.items():
                print(f"{ruta_id}: {destino}")

        elif opcion == '2':
            # Actualizar una ruta existente
            print("\nRutas disponibles para actualizar:")
            for ruta_id, destino in rutas.items():
                print(f"{ruta_id}: {destino}")
            actualizar_ruta = input("Ingrese el código de la ruta a actualizar (ruta+(numero)): ").strip().lower()

            if actualizar_ruta in rutas:
                nuevo_destino = input(f"Ingrese el nuevo destino para la {actualizar_ruta}: ").strip()
                rutas[actualizar_ruta] = nuevo_destino
                print(f"Ruta {actualizar_ruta} actualizada a {nuevo_destino}.")
            else:
                print("Error: El código de ruta no existe.")

        elif opcion == '3':
            # Agregar una nueva ruta
            nuevo_codigo = input("Ingrese el código para la nueva ruta (ej: ruta4): ").strip().lower()
            if nuevo_codigo in rutas:
                print("Error: El código de ruta ya existe.")
            else:
                nuevo_destino = input("Ingrese el destino para la nueva ruta: ").strip()
                rutas[nuevo_codigo] = nuevo_destino
                print(f"Nueva ruta agregada: {nuevo_codigo} -> {nuevo_destino}")

        elif opcion == '4':
            print("Saliendo de la gestión de rutas.")
            bandera = False
        else:
            print("Opción no válida. Por favor, intente de nuevo.")
    return rutas

def cargar_datos_camiones():
    """Carga datos de los camiones en un diccionario."""
    camiones = {}
    bandera = True
    while bandera:
        codigo_camion = input("Ingrese el código del camión: ")

        while not codigo_camion.isdigit() or int(codigo_camion) < 0:
            print("Error: El código del camión debe ser un número positivo.")
            codigo_camion = input("Ingrese el código del camión: ")

        nombre_transportista = input("Ingrese el nombre del transportista: ")
        material_transportar = input("Ingrese el material a transportar: ")
        while not material_transportar.isalpha():
            print("Error: El material debe ser una cadena de caracteres.")
            material_transportar = input("Ingrese el material a transportar: ")

        cantidad_material = int(input("Cuantos kg se van a transportar de ese material? "))
        while cantidad_material <= 0:
            print("Error: La cantidad a transportar debe ser un número positivo.")
            cantidad_material = int(input("Cuantos kg se van a transportar de ese material? "))

        #diccionario de diccionario(codigo_camion como clave, valor asociado es el otro dic)
        camiones[codigo_camion] = {
            'nombre_transportista': nombre_transportista,
            'material': material_transportar,
            'cantidad': cantidad_material,
            'rutas': {}
        }

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

        # Repetimos la verificación hasta que no haya más rutas duplicadas
        while repetir:
            repetir = False
            rutas_dia.clear()

            # Recorre las rutas de cada camión en el día específico
            for codigo_camion, datos_camion in camiones.items():
                ruta = datos_camion['rutas'][dia]

                # Si la ruta ya existe en otro camión para ese día, hay una repetición
                if ruta in rutas_dia and ruta != "Sin viaje":
                    print(f"\n¡Repetición detectada el {dia} en la ruta {ruta} entre los camiones {codigo_camion} y {rutas_dia[ruta]}!")
                    
                    camion_reprogramado = False  
                    
                    # Permitir reprogramar la ruta repetida
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
    """Muestra todos los datos de los camiones."""
    print("\nDatos de los camiones:")
    print("\n")
    print(f"{'Camion':<10} {'Transportista':<20} {'Material':<15} {'Cantidad (kg)':<15}")
    print("-" * 60)  # Línea separadora para mayor claridad

    for codigo_camion, datos in camiones.items():
        print(f"{codigo_camion:<10} {datos['nombre_transportista']:<20} {datos['material']:<15} {datos['cantidad']:<15}")

# Programa principal
def main():
    print("Bienvenido al sistema de gestión de camiones.")
    rutas = gestionar_rutas(Rutas)
    camiones = cargar_datos_camiones()
    camiones = cargar_rutas(camiones, rutas)

    matriz_rutas = crear_matriz_rutas(5, camiones)
    matriz_rutas = cargar_matriz_rutas(matriz_rutas, camiones)
    verificar_rutas(camiones)

    # Definir stock disponible
    stock_disponible = 1000  
    gestionar_stock(camiones, stock_disponible)
    
    mostrar_datos_camiones(camiones)
    mostrar_matriz_rutas(matriz_rutas, camiones)

main()

