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


import re

def cargar_datos_camiones(camiones, opcion):
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
        agregar_camion = True
        while agregar_camion:
            patente_camion = input("Ingrese la patente del camión (formato 'AB123CD') o ingrese -1 para volver: ").strip().upper()
            if patente_camion == '-1':
                return camiones
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
            print("Error: El nombre debe ser solo letras.")
            nombre_transportista = input("Ingrese el nombre del transportista: ").strip()

        material_transportar = input("Ingrese el material a transportar: ").strip()
        while not material_transportar.isalpha():
            print("Error: El material debe ser solo letras.")
            material_transportar = input("Ingrese el material a transportar: ").strip()

        # Validar cantidad de material
        cantidad_material = -1
        while cantidad_material <= 0:
            try:
                cantidad_material = int(input("Cuántos kg se van a transportar de ese material? "))
                if cantidad_material <= 0:
                    print("Error: La cantidad debe ser un número positivo.")
            except ValueError:
                print("Error: Debe ingresar un número válido.")

        # Validar tipo de viaje
        tipo_viaje = input("Ingrese el tipo de viaje ('carga'(c) o 'descarga'(d)): ").strip().lower()
        while tipo_viaje not in ['carga', 'descarga', 'c', 'd']:
            print("Error: Tipo de viaje no válido.")
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
        print(f"Camión con patente {patente_camion} agregado correctamente.")

        continuar_cargando = input("¿Desea seguir cargando datos de camiones? (s/n): ").strip().lower()
        if continuar_cargando == 'n':
            return camiones

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
                print("Cantidad no modificada por entrada inválida.")

            nuevo_tipo_viaje = input("Nuevo tipo de viaje ('carga' o 'descarga'): ").strip().lower()
            if nuevo_tipo_viaje in ['carga', 'descarga', 'c', 'd']:
                camiones[patente_modificar]['tipo_viaje'] = 'carga' if nuevo_tipo_viaje in ['c', 'carga'] else 'descarga'
            
            print(f"Camión con patente {patente_modificar} modificado correctamente.")
        else:
            print("Error: No se encontró un camión con esa patente.")

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
                print("Eliminación cancelada.")
        else:
            print("Error: No se encontró un camión con esa patente.")

    elif opcion == '5':
        # Volver al menú principal
        print("Regresando al menú principal...")
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

    while True:
        opcion = input("¿Desea cargar rutas para un camión en particular? (s/n): ").strip().lower()
        if opcion == 's':
            codigo_camion = input("Ingrese el código del camión (o ingrese '-1' para volver al menú): ").strip().upper()
            if codigo_camion == '-1':
                print("Volviendo al menú principal...")
                break
            elif codigo_camion in camiones:
                cargar_rutas_para_camion(codigo_camion, camiones[codigo_camion], dias_semana, rutas_disponibles)
            else:
                print(f"Error: El camión con código {codigo_camion} no existe.")
        elif opcion == 'n':
            break  # Salir del bucle y volver al menú principal
        else:
            print("Opción no válida. Por favor, ingrese 's' o 'n'.")

    rutas_duplicadas = verificar_rutas_duplicadas(camiones)
    if rutas_duplicadas:
        camiones = manejar_rutas_duplicadas(rutas_duplicadas, camiones)
    else:
        print("No se encontraron rutas duplicadas.")

    return camiones

def cargar_rutas_para_camion(codigo_camion, datos_camion, dias_semana, rutas_disponibles):
    """Carga rutas para un camión en particular."""
    print(f"\nCargando rutas para el camión {codigo_camion} ({datos_camion['nombre_transportista']}):")
    for dia in dias_semana:
        ruta = input(f"Ingrese la ruta para el {dia} (o deje vacío si no hay ruta): ").strip().lower()
        if ruta in rutas_disponibles.keys() or not ruta:
            datos_camion['rutas'][dia] = ruta if ruta else "Sin viaje"
        else:
            print(f"La ruta {ruta} no es válida.")


def cargar_rutas_para_camion(codigo_camion, datos_camion, dias_semana, rutas_disponibles):
    """Carga rutas para un camión en particular."""
    print(f"\nCargando rutas para el camión {codigo_camion} ({datos_camion['nombre_transportista']}):")
    for dia in dias_semana:
        ruta = input(f"Ingrese la ruta para el {dia} (o deje vacío si no hay ruta): ").strip().lower()
        if ruta in rutas_disponibles.keys() or not ruta:
            datos_camion['rutas'][dia] = ruta if ruta else "Sin viaje"
        else:
            print(f"La ruta {ruta} no es válida.")


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


def gestionar_materiales(materiales,opcion):

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
    
    for patente, datos in camiones.items(): 
        try: 
            print(f"{datos['patente']:<15} {datos['nombre_transportista']:<20} {datos['material']:<15} {datos['cantidad']:<15} {datos['tipo_viaje']:<15}") 
        except KeyError as e: 
            print(f"Error: Clave {e} no encontrada en el camión con patente {patente}")


import re

def gestionar_rutas(rutas, opcion):
    if opcion == '1':
        print("\nRutas actuales:")
        for codigo, datos in rutas.items():
            print(f"{codigo}: Origen - {datos['origen']}, Destino - {datos['destino']}")
    
    elif opcion == '2':
        while True:
            codigo = input("Ingrese el código de la nueva ruta (formato 'rutaX', donde X es un número, o ingrese '-1' para volver al menú principal): ").strip().lower()
            if codigo == '-1':
                print("Volviendo al menú principal...")
                break
            # Validar formato de código de ruta
            if re.match(r"^ruta\d+$", codigo):
                if codigo not in rutas:
                    while True:
                        origen = input("Ingrese el origen de la nueva ruta: ").strip()
                        if re.match(r"^[a-zA-Z\s]+$", origen):
                            break
                        else:
                            print("Error: El origen debe ser una cadena de caracteres. Intente nuevamente.")
                    
                    while True:
                        destino = input("Ingrese el destino de la nueva ruta: ").strip()
                        if re.match(r"^[a-zA-Z\s]+$", destino):
                            break
                        else:
                            print("Error: El destino debe ser una cadena de caracteres. Intente nuevamente.")
                    
                    rutas[codigo] = {'origen': origen, 'destino': destino}
                    print(f"Ruta {codigo} agregada correctamente.")
                    break
                else:
                    print("Error: El código de ruta ya existe. Intente nuevamente.")
            else:
                print("Error: El código de la ruta debe tener el formato 'rutaX' (ej. 'ruta1'). Intente nuevamente.")
    
    elif opcion == '3':
        codigo = input("Ingrese el código de la ruta a modificar: ").strip().lower()
        if codigo == '-1':
            print("Volviendo al menú principal...")
            return rutas
        if codigo in rutas:
            while True:
                origen = input("Ingrese el nuevo origen de la ruta: ").strip()
                if re.match(r"^[a-zA-Z\s]+$", origen):
                    break
                else:
                    print("Error: El origen debe ser una cadena de caracteres. Intente nuevamente.")
            
            while True:
                destino = input("Ingrese el nuevo destino de la ruta: ").strip()
                if re.match(r"^[a-zA-Z\s]+$", destino):
                    break
                else:
                    print("Error: El destino debe ser una cadena de caracteres. Intente nuevamente.")
            
            rutas[codigo] = {'origen': origen, 'destino': destino}
            print(f"Ruta {codigo} modificada correctamente.")
        else:
            print("Error: El código de ruta no existe.")
    
    elif opcion == '4':
        codigo = input("Ingrese el código de la ruta a eliminar: ").strip().lower()
        if codigo == '-1':
            print("Volviendo al menú principal...")
            return rutas
        if codigo in rutas:
            confirmar = input(f"¿Está seguro de que desea eliminar la ruta {codigo}? (s/n): ").strip().lower()
            if confirmar == 's':
                del rutas[codigo]
                print(f"Ruta {codigo} eliminada correctamente.")
            else:
                print("Eliminación cancelada.")
        else:
            print("Error: El código de ruta no existe.")
    
    elif opcion == '5':
        print("Volviendo al menú principal...")
    
    else:
        print("Opción no válida. Por favor, intente de nuevo.")

    return rutas




    
