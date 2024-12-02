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
    """Gestión de datos de los camiones en un diccionario."""
    continuar=True
    while True:
        print("\n--- Gestión de Camiones ---")
        print("1. Mostrar camiones actuales")
        print("2. Agregar camión nuevo")
        print("3. Modificar camión existente")
        print("4. Eliminar camión")
        print("5. Volver al menú principal")
        
        opcion = input("Seleccione una opción (1-5): ").strip()
        
        if opcion == '1':
            # Mostrar camiones actuales
            if not camiones:
                print("\nNo hay camiones registrados.")
            else:
                print("\nCamiones registrados:")
                for patente, datos in camiones.items():
                    print(f"Patente: {patente}, Transportista: {datos['nombre_transportista']}, "
                          f"Material: {datos['material']}, Cantidad: {datos['cantidad']} kg, "
                          f"Tipo de viaje: {datos['tipo_viaje']}")


        elif opcion == '2':
        # Agregar camión nuevo
            print("\n--- Agregar Nuevo Camión ---")
            agregar_camion = True  # Bandera para controlar el ciclo
            while agregar_camion:
                patente_camion = input("Ingrese la patente del camión (formato 'AB123CD'): ").strip().upper()
                # Eliminar espacios antes de la validación
                patente_camion = re.sub(r"\s+", "", patente_camion)
        
                # Validar formato de patente
                if re.match(r"^[A-Z]{2}\d{3}[A-Z]{2}$", patente_camion):
                    # Verificar si ya existe la patente
                    if patente_camion in camiones:
                        print("Error: Ya existe un camión con esta patente. Intente nuevamente.")
                    else:
                        print(f"Patente '{patente_camion}' registrada correctamente.")
                        agregar_camion = False  # Salir del ciclo si la patente es válida y no duplicada
                else:
                    print("Error: La patente debe tener el formato 'AB123CD' sin espacios. Intente nuevamente.")

            
            nombre_transportista = input("Ingrese el nombre del transportista: ").strip()
            while not nombre_transportista.isalpha():
                print(" Error: El nombre debe ser solo letras.")
                nombre_transportista = input("Ingrese el nombre del transportista: ").strip()

            material_transportar = input("Ingrese el material a transportar: ").strip()
            while not material_transportar.isalpha():
                print(" Error: El material debe ser solo letras.")
                material_transportar = input("Ingrese el material a transportar: ").strip()

            # Validar cantidad de material
            cantidad_material = -1
            while cantidad_material <= 0:
                try:
                    cantidad_material = int(input("Cuántos kg se van a transportar de ese material? "))
                    if cantidad_material <= 0:
                        print(" Error: La cantidad debe ser un número positivo.")
                except ValueError:
                    print(" Error: Debe ingresar un número válido.")

            # Validar tipo de viaje
            tipo_viaje = input("Ingrese el tipo de viaje ('carga'(c) o 'descarga'(d)): ").strip().lower()
            while tipo_viaje not in ['carga', 'descarga', 'c', 'd']:
                print(" Error: Tipo de viaje no válido.")
                tipo_viaje = input("Ingrese el tipo de viaje ('carga' o 'descarga'): ").strip().lower()

            tipo_viaje = 'carga' if tipo_viaje in ['c', 'carga'] else 'descarga'

            camiones[patente_camion] = {
                'patente': patente_camion,
                'nombre_transportista': nombre_transportista,
                'material': material_transportar,
                'cantidad': cantidad_material,
                'tipo_viaje': tipo_viaje,
                'rutas': {}
            }
            print(f" Camión con patente {patente_camion} agregado correctamente.")


            continuar_cargando = input("¿Desea seguir cargando datos de camiones? (s/n): ").strip().lower() 
            if continuar_cargando == 'n': 
                continue

        elif opcion == '3':
            # Modificar camión existente
            print("\n--- Modificar Camión Existente ---")
            patente_modificar = input("Ingrese la patente del camión a modificar: ").strip().upper()
            patente_modificar = re.sub(r"\s+", "", patente_modificar)
            if patente_modificar in camiones:
                print(f"Datos actuales: {camiones[patente_modificar]}")
                print("Ingrese los nuevos datos (deje en blanco para no modificar):")
                
                nuevo_transportista = input("Nuevo nombre del transportista: ").strip()
                if nuevo_transportista:
                    camiones[patente_modificar]['nombre_transportista'] = nuevo_transportista
                
                nuevo_material = input("Nuevo material a transportar: ").strip()
                if nuevo_material.isalpha():
                    camiones[patente_modificar]['material'] = nuevo_material
                
                try:
                    nueva_cantidad = input("Nueva cantidad a transportar: ").strip()
                    if nueva_cantidad:
                        nueva_cantidad = int(nueva_cantidad)
                        if nueva_cantidad > 0:
                            camiones[patente_modificar]['cantidad'] = nueva_cantidad
                except ValueError:
                    print(" Cantidad no modificada por entrada inválida.")

                nuevo_tipo_viaje = input("Nuevo tipo de viaje ('carga' o 'descarga'): ").strip().lower()
                if nuevo_tipo_viaje in ['carga', 'descarga', 'c', 'd']:
                    camiones[patente_modificar]['tipo_viaje'] = 'carga' if nuevo_tipo_viaje in ['c', 'carga'] else 'descarga'
                
                print(f" Camión con patente {patente_modificar} modificado correctamente.")
            else:
                print(" Error: No se encontró un camión con esa patente.")

        elif opcion == '4':
            # Eliminar camión
            print("\n--- Eliminar Camión ---")
            patente_eliminar = input("Ingrese la patente del camión a eliminar: ").strip().upper()
            patente_eliminar = re.sub(r"\s+", "", patente_eliminar)
            if patente_eliminar in camiones:
                confirmar = input(f"¿Está seguro de eliminar el camión {patente_eliminar}? (s/n): ").strip().lower()
                if confirmar == 's':
                    del camiones[patente_eliminar]
                    print(f"Camión con patente {patente_eliminar} eliminado correctamente.")
                else:
                    print(" Eliminación cancelada.")
            else:
                print(" Error: No se encontró un camión con esa patente.")

        elif opcion == '5':
            # Volver al menú principal
            print("Regresando al menú principal...")
            continuar = False  # Esto sale del ciclo y vuelve al menú principal
        else:
            print("Opción no válida. Intente nuevamente.")

        return camiones

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

        continuar_cargando = input("¿Desea seguir cargando datos de camiones? (s/n): ").strip().lower() 
        if continuar_cargando == 'n': 
            break
    
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
        
        # Validar si el material existe en el stock actual
        if material in stock_actual:
            if tipo_viaje == 'carga':
                # Incrementar el stock del material cargado
                stock_actual[material] += cantidad
                print(f"{cantidad} kg de {material} añadidos al stock.")
            elif tipo_viaje == 'descarga':
                # Verificar si hay suficiente material para descargar
                if stock_actual[material] >= cantidad:
                    stock_actual[material] -= cantidad
                    print(f"{cantidad} kg de {material} descargados del stock.")
                else:
                    print(f"Alerta: No hay suficiente {material} para descargar {cantidad} kg. Solo hay {stock_actual[material]} kg disponibles.")
        else:
            if tipo_viaje == 'carga':
                # Crear un nuevo material si no existía previamente
                stock_actual[material] = cantidad
                print(f"{material} no existía en el stock. Ahora hay {cantidad} kg disponibles.")
            else:
                # Error si se intenta descargar un material inexistente
                print(f"Error: No se puede descargar {material} ya que no existe en el stock.")
    
    # Mostrar el stock actualizado
    print("\n--- Stock Actualizado ---")
    for material, cantidad in stock_actual.items():
        print(f"{material.capitalize()}: {cantidad} kg")
    
    return stock_actual


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
                confirmar = input(f"¿Está seguro de que desea eliminar el material {nombre}? (s/n): ").strip().lower() 
                if confirmar == 's': 
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
                confirmar = input(f"¿Está seguro de que desea eliminar la ruta {codigo}? (s/n): ").strip().lower() 
                if confirmar == 's': 
                    del rutas[codigo] 
                    print(f"Ruta {codigo} eliminada correctamente.") 
                else:
                    print("Eliminación cancelada.") 
            else: print("Error: El código de ruta no existe.") 
        
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
        print("2. Gestionar camiones")
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
            print("Saliendo del programa. ¡Hasta luego!")
            guardar_rutas_json(rutas)  
            guardar_camiones_json(camiones)
            guardar_materiales(materiales)
            continuar = False
        else:
            print("Opción no válida. Por favor, intente de nuevo.")


menu_principal()
