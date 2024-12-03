import pytest
import json
import os
from main import (
    guardar_rutas_json, cargar_rutas_json, guardar_camiones_json, cargar_camiones_json,
    cargar_materiales, guardar_materiales, cargar_datos_camiones, gestionar_stock,
    mostrar_datos_camiones, 
)

def test_guardar_y_cargar_rutas_json():
    rutas = {
        'ruta1': {'origen': 'Buenos Aires', 'destino': 'Mendoza'},
        'ruta2': {'origen': 'Buenos Aires', 'destino': 'Córdoba'}
    }
    archivo = 'test_rutas.json'
    guardar_rutas_json(rutas, archivo)
    rutas_cargadas = cargar_rutas_json(archivo)
    assert rutas == rutas_cargadas
    os.remove(archivo)

def test_guardar_y_cargar_camiones_json():
    camiones = {
        'AB123CD': {'nombre_transportista': 'Juan', 'material': 'arena', 'cantidad': 100, 'tipo_viaje': 'carga'}
    }
    archivo = 'test_camiones.json'
    guardar_camiones_json(camiones, archivo)
    camiones_cargados = cargar_camiones_json(archivo)
    assert camiones == camiones_cargados
    os.remove(archivo)

def test_cargar_materiales():
    archivo = 'test_materiales.json'
    materiales = {'arena': 100, 'ladrillos': 200}
    guardar_materiales(materiales, archivo)
    materiales_cargados = cargar_materiales(archivo)
    assert materiales == materiales_cargados
    os.remove(archivo)


def test_gestionar_stock():
    camiones = {
        'AB123CD': {'material': 'arena', 'cantidad': 100, 'tipo_viaje': 'carga'},
        'EF456GH': {'material': 'arena', 'cantidad': 50, 'tipo_viaje': 'descarga'}
    }
    stock_actual = {'arena': 50}
    stock_actualizado = gestionar_stock(camiones, stock_actual)
    assert stock_actualizado == {'arena': 100}

