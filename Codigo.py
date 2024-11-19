import re
import json 

# Diccionario iniciales 
rutas = {
    'ruta1': {'origen': 'Buenos Aires', 'destino': 'Mendoza'},
    'ruta2': {'origen': 'Buenos Aires', 'destino': 'Córdoba'},
    'ruta3': {'origen': 'Buenos Aires', 'destino': 'Entre Ríos'}
}

materiales = {
    "arena": 100,
    "ladrillos": 200,
    "tierra": 150,
    "piedras": 100,
}


# Archivos json
def guardar_rutas_json(rutas, archivo='rutas.json'):
    try:
        with open(archivo, 'w', encoding='utf-8') as file:
            json.dump(rutas, file, indent=4, ensure_ascii=False)
        print(f"Rutas guardadas en {archivo}.")
    except Exception as e:
        print(f"Error al guardar las rutas: {e}")

def cargar_rutas_json(archivo='rutas.json'):
    try:
        with open(archivo, 'r', encoding='utf-8') as file:
            rutas = json.load(file)
        print(f"Rutas cargadas desde {archivo}.")
        return rutas
    except FileNotFoundError:
        print(f"No se encontró el archivo {archivo}. Se usará el diccionario de rutas predeterminado.")
        return rutas
    except json.JSONDecodeError:
        print("Error: El archivo JSON está corrupto o malformado.")
        return rutas
    except Exception as e:
        print(f"Error al cargar las rutas: {e}")
        return rutas

def guardar_camiones_json(camiones, archivo='camiones.json'):
    try:
        with open(archivo, 'w', encoding='utf-8') as file:
            json.dump(camiones, file, indent=4, ensure_ascii=False)
        print(f"Datos de camiones guardados en {archivo}.")
    except Exception as e:
        print(f"Error al guardar los datos de camiones: {e}")

def cargar_camiones_json(archivo='camiones.json'):
    try:
        with open(archivo, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Archivo {archivo} no encontrado. Iniciando con datos vacíos.")
        return {}
    except json.JSONDecodeError:
        print("Error: Archivo JSON malformado.")
        return {}
    except Exception as e:
        print(f"Error al cargar los datos de camiones: {e}")
        return {}

def cargar_materiales(archivo='materiales.json'):
    try:
        with open(archivo, 'r', encoding='utf-8') as file:
            materiales = json.load(file)
    except FileNotFoundError:
        print("El archivo de materiales no existe. Creando uno nuevo.")
        materiales = {}
        guardar_materiales(materiales, archivo)
    except json.JSONDecodeError:
        print("Error al leer el archivo JSON. Creando uno nuevo.")
        materiales = {}
        guardar_materiales(materiales, archivo)
    return materiales

def guardar_materiales(materiales, archivo='materiales.json'):
    try:
        with open(archivo, 'w', encoding='utf-8') as file:
            json.dump(materiales, file, indent=4, ensure_ascii=False)
        print(f"Materiales guardados en {archivo}.")
    except Exception as e:
        print(f"Error al guardar los materiales: {e}")

def cargar_datos_camiones(camiones):
    """Carga datos de los camiones en un diccionario."""
    bandera = True
    while bandera:
        # Validar el formato de la patente
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

        # Validar cantidad de material
        cantidad_material = -1  
        while cantidad_material <= 0:
            try:
                cantidad_material = int(input("Cuántos kg se van a transportar de ese material? "))
                if cantidad_material <= 0:
                    print("Error: La cantidad a transportar debe ser un número positivo.")
            except ValueError:
                print("Error: Debe ingresar un número válido (solo números positivos).")

        tipo_viaje = input("Ingrese el tipo de viaje ('carga'(c) o 'descarga'(d)): ").strip().lower()
        while tipo_viaje not in ['carga', 'descarga', 'c', 'd']:
            print("Error: Tipo de viaje no válido. Debe ser 'carga', 'descarga', 'c' o 'd'.")
            tipo_viaje = input("Ingrese el tipo de viaje ('carga' o 'descarga'): ").strip().lower()

        # Convertir 'c' y 'd' a 'carga' y 'descarga'
        if tipo_viaje == 'c':
            tipo_viaje = 'carga'
        elif tipo_viaje == 'd':
            tipo_viaje = 'descarga'

        camiones[patente_camion] = {
            'patente': patente_camion,
            'nombre_transportista': nombre_transportista,
            'material': material_transportar,
            'cantidad': cantidad_material,
            'tipo_viaje': tipo_viaje,
            'rutas': {}
        }

        continuar = input("¿Desea ingresar otro camión? (s/n): ").lower()
        bandera = continuar != 'n'
    
    return camiones  # Devuelve el diccionario actualizado con los camiones ingresados

def verificar_rutas_duplicadas(camiones):
    """Verifica si hay camiones con rutas duplicadas en el mismo día."""
    rutas_duplicadas = {}
    
    for camion in camiones.values():
        for dia, ruta in camion['rutas'].items():
            if ruta != "Sin viaje":  
                if ruta not in rutas_duplicadas:
                    rutas_duplicadas[ruta] = []
                rutas_duplicadas[ruta].append((camion['patente'], dia))
    
    # Filtrar rutas duplicadas
    rutas_duplicadas = {ruta: dias for ruta, dias in rutas_duplicadas.items() if len(dias) > 1}
    
    return rutas_duplicadas


def manejar_rutas_duplicadas(rutas_duplicadas, camiones):
    """Maneja las rutas duplicadas pidiendo al usuario que modifique las rutas."""
    for ruta, camiones_con_ruta in rutas_duplicadas.items():
        print(f"\n¡ALERTA! La ruta {ruta} está asignada a los siguientes camiones en los siguientes días:")
        for patente, dia in camiones_con_ruta:
            print(f"  - Camión {patente} en {dia}")
        
        cambiar = input("¿Desea cambiar alguna ruta asignada a esta ruta? (s/n): ").lower()
        if cambiar == 's':
            for patente, dia in camiones_con_ruta:
                print(f"\nCamión {patente} tiene la ruta {ruta} asignada el día {dia}.")
                nueva_ruta = input(f"¿Qué ruta desea asignar a este camión? (deje vacío para no cambiar): ").strip()
                if nueva_ruta:
                    camiones[patente]['rutas'][dia] = nueva_ruta
                    print(f"La ruta para el camión {patente} en {dia} ha sido cambiada a {nueva_ruta}.")
    
    return camiones

def cargar_rutas(camiones, rutas_disponibles):
    """Carga las rutas para cada camión para cada día de la semana y verifica rutas duplicadas."""
    dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    
    for codigo_camion, datos_camion in camiones.items(): 
        print(f"\nCargando rutas para el camión {codigo_camion} ({datos_camion['nombre_transportista']}):")

        for dia in dias_semana:
            ruta = input(f"Ingrese la ruta para el {dia} (o deje vacío si no hay ruta): ").strip().lower()
            if ruta in rutas_disponibles.keys() or not ruta:
                datos_camion['rutas'][dia] = ruta if ruta else "Sin viaje"
            else:
                print(f"La ruta {ruta} no es válida.")
    
    rutas_duplicadas = verificar_rutas_duplicadas(camiones)
    if rutas_duplicadas:
        camiones = manejar_rutas_duplicadas(rutas_duplicadas, camiones)
    else:
        print("No se encontraron rutas duplicadas.")
    
    return camiones

def gestionar_stock(camiones, stock_actual):
    """Calcula el total de material transportado y verifica si hay faltante para los próximos viajes."""
    for camion in camiones.values():
        material = camion['material']
        cantidad = camion['cantidad']
        tipo_viaje = camion['tipo_viaje']
        if material in stock_actual:
            if tipo_viaje == 'carga':
                stock_actual[material] += cantidad
            elif tipo_viaje == 'descarga':
                if stock_actual[material] >= cantidad:
                    stock_actual[material] -= cantidad
                else:
                    print(f"Alerta: No hay suficiente {material} para descargar {cantidad} kg. Solo hay {stock_actual[material]} kg disponibles.")
        else:
            if tipo_viaje == 'carga':
                stock_actual[material] = cantidad
            else:
                print(f"Error: No se puede descargar {material} ya que no existe en el stock.")

    stock_total = sum(stock_actual.values())
    print(f"Stock actualizado: {stock_actual}")
    guardar_materiales(materiales)
    
    return materiales

def gestionar_materiales(materiales):
    """Permite al usuario gestionar los materiales disponibles."""
    continuar = True
    while continuar:
        print("\n--- Gestión de Materiales ---")
        print("1. Mostrar materiales actuales")
        print("2. Agregar nuevo material")
        print("3. Modificar cantidad de material existente")
        print("4. Eliminar material")
        print("5. Volver al menú principal")

        opcion = input("Seleccione una opción (1-5): ")

        if opcion == '1':
            print("\nMateriales actuales:")
            for nombre, cantidad in materiales.items():
                print(f"{nombre}: {cantidad} unidades")
        elif opcion == '2':
            nombre = input("Ingrese el nombre del nuevo material: ").strip().lower()
            cantidad = int(input("Ingrese la cantidad del nuevo material: ").strip())
            if nombre not in materiales:
                materiales[nombre] = cantidad
                print(f"Material {nombre} agregado correctamente con {cantidad} unidades.")
            else:
                print("Error: El material ya existe.")
        elif opcion == '3':
            nombre = input("Ingrese el nombre del material a modificar: ").strip().lower()
            if nombre in materiales:
                cantidad = int(input(f"Ingrese la nueva cantidad de {nombre}: ").strip())
                materiales[nombre] = cantidad
                print(f"Cantidad de {nombre} modificada correctamente.")
            else:
                print("Error: El material no existe.")
        elif opcion == '4':
            nombre = input("Ingrese el nombre del material a eliminar: ").strip().lower()
            if nombre in materiales:
                confirmacion = input(f"¿Está seguro de eliminar el material {nombre}? (s/n): ").lower()
                if confirmacion == 's':
                    del materiales[nombre]
                    print(f"Material {nombre} eliminado correctamente.")
                else:
                    print("Eliminación cancelada.")
            else:
                print("Error: El material no existe.")

        elif opcion == '5':
            continuar = False
        else:
            print("Opción no válida. Por favor, intente de nuevo.")
    
    return materiales


def mostrar_datos_camiones(camiones):
    """Muestra todos los datos de los camiones en formato de tabla."""
    print("\nDatos de los camiones:")
    print(f"{'Patente':<15} {'Transportista':<20} {'Material':<15} {'Cantidad (kg)':<15} {'Tipo de Viaje':<15}")
    print("-" * 80)

    for camion in camiones.values():
        print(f"{camion['patente']:<15} {camion['nombre_transportista']:<20} {camion['material']:<15} {camion['cantidad']:<15} {camion['tipo_viaje']:<15}")

def gestionar_rutas(rutas):
    """Permite al usuario gestionar las rutas disponibles."""
    continuar = True
    while continuar:
        print("\n--- Gestión de Rutas ---")
        print("1. Mostrar rutas actuales")
        print("2. Agregar nueva ruta")
        print("3. Modificar ruta existente")
        print("4. Eliminar ruta")
        print("5. Volver al menú principal")

        opcion = input("Seleccione una opción (1-5): ")

        if opcion == '1':
            print("\nRutas actuales:")
            for codigo, datos in rutas.items():
                print(f"{codigo}: Origen - {datos['origen']}, Destino - {datos['destino']}")
        elif opcion == '2':
            codigo = input("Ingrese el código de la nueva ruta: ").strip().lower()
            origen = input("Ingrese el origen de la nueva ruta: ").strip()
            destino = input("Ingrese el destino de la nueva ruta: ").strip()
            if codigo not in rutas:
                rutas[codigo] = {'origen': origen, 'destino': destino}
                print(f"Ruta {codigo} agregada correctamente.")
            else:
                print("Error: El código de ruta ya existe.")
        elif opcion == '3':
            codigo = input("Ingrese el código de la ruta a modificar: ").strip().lower()
            if codigo in rutas:
                origen = input("Ingrese el nuevo origen de la ruta: ").strip()
                destino = input("Ingrese el nuevo destino de la ruta: ").strip()
                rutas[codigo] = {'origen': origen, 'destino': destino}
                print(f"Ruta {codigo} modificada correctamente.")
            else:
                print("Error: El código de ruta no existe.")
        elif opcion == '4':
            codigo = input("Ingrese el código de la ruta a eliminar: ").strip().lower()
            if codigo in rutas:
                    confirmacion = input(f"¿Está seguro de eliminar la ruta {codigo}? (s/n): ").lower()
                    if confirmacion == 's':
                        del rutas[codigo]
                        print(f"Ruta {codigo} eliminada correctamente.")
                    else:
                        print("Eliminación cancelada.")
        elif opcion == '5':
            continuar = False
        else:
            print("Opción no válida. Por favor, intente de nuevo.")
    return rutas

def menu_principal():
    rutas = cargar_rutas_json()
    camiones = cargar_camiones_json()
    materiales = cargar_materiales()
    

    continuar = True

    while continuar:
        print("\n--- Menú Principal ---")
        print("1. Gestionar rutas")
        print("2. Cargar datos de camiones")
        print("3. Cargar rutas para camiones")
        print("4. Gestionar stock de materiales")
        print("5. Mostrar datos de los camiones")
        print("6. Salir")

        opcion = input("Seleccione una opción (1-6): ")

        if opcion == '1':
            rutas = gestionar_rutas(rutas)
            guardar_rutas_json(rutas) 
        elif opcion == '2':
            camiones = cargar_datos_camiones(camiones)
            guardar_camiones_json(camiones)  
        elif opcion == '3':
            camiones = cargar_rutas(camiones, rutas)
            guardar_camiones_json(camiones)  
        elif opcion == '4':
            materiales = gestionar_materiales(materiales)
            guardar_materiales(materiales)    
        elif opcion == '5':
            mostrar_datos_camiones(camiones)
        elif opcion == '6':
            print("Saliendo del programa.")
            guardar_rutas_json(rutas)  
            guardar_camiones_json(camiones)
            guardar_materiales(materiales)
            continuar = False
        else:
            print("Opción no válida. Por favor, intente de nuevo.")


menu_principal() 
