import main

def menu_camiones(camiones):
    """Gestión de datos de los camiones en un diccionario."""
    while True:
        print("\n--- Gestión de Camiones ---")
        print("1. Mostrar camiones actuales")
        print("2. Agregar camión nuevo")
        print("3. Modificar camión existente")
        print("4. Eliminar camión")
        print("5. Volver al menú principal")
        
        opcion = input("Seleccione una opción (1-5): ").strip()
        
        if opcion == '5':
            break
        
        camiones = main.cargar_datos_camiones(camiones, opcion)

    return camiones


def menu_rutas(rutas):
    """Permite al usuario gestionar las rutas disponibles."""
    while True:
        print("\n--- Gestión de Rutas ---")
        print("1. Mostrar rutas actuales")
        print("2. Agregar nueva ruta")
        print("3. Modificar ruta existente")
        print("4. Eliminar ruta")
        print("5. Volver al menú principal")

        opcion = input("Seleccione una opción (1-5): ").strip()

        rutas = main.gestionar_rutas(rutas, opcion)
        if opcion == '5':
            break

    return rutas

def menu_materiales(materiales):
    """Permite al usuario gestionar los materiales disponibles."""
    while True:
        print("\n--- Gestión de Materiales ---")
        print("1. Mostrar materiales actuales")
        print("2. Agregar nuevo material")
        print("3. Modificar cantidad de material existente")
        print("4. Eliminar material")
        print("5. Volver al menú principal")

        opcion = input("Seleccione una opción (1-5): ").strip()
        
        materiales = main.gestionar_materiales(materiales, opcion)
        if opcion == '5':
            break

    return materiales

rutas = main.cargar_rutas_json()
camiones = main.cargar_camiones_json()
materiales = main.cargar_materiales()

continuar = True
while continuar:
    print("\n--- Menú Principal ---")
    print("1. Gestionar rutas")
    print("2. Gestionar camiones")
    print("3. Cargar rutas para camiones")
    print("4. Gestionar stock de materiales")
    print("5. Mostrar datos de los camiones")
    print("6. Salir")

    opcion = input("Seleccione una opción (1-6): ").strip()

    if opcion == '1':
        rutas = menu_rutas(rutas)
        main.guardar_rutas_json(rutas)
    elif opcion == '2':
        camiones = menu_camiones(camiones)
        main.cargar_camiones_json(camiones)
        main.guardar_camiones_json(camiones)
    elif opcion == '3':
        camiones = main.cargar_datos_camiones(camiones)
        main.guardar_camiones_json(camiones)
    elif opcion == '4':
        materiales = menu_materiales(materiales)
        main.guardar_materiales(materiales)
    elif opcion == '5':
        main.mostrar_datos_camiones(camiones)
    elif opcion == '6':
        print("Saliendo del programa. ¡Hasta luego!")
        main.guardar_rutas_json(rutas)
        main.guardar_camiones_json(camiones)
        main.guardar_materiales(materiales)
        continuar = False
    else:
        print("Opción no válida. Por favor, intente de nuevo.")
