import pytest
import json
from unittest.mock import patch, mock_open
from main import (
    guardar_rutas_json, cargar_rutas_json, guardar_camiones_json, cargar_camiones_json,
    cargar_materiales, guardar_materiales, verificar_rutas_duplicadas, gestionar_stock
)

@pytest.fixture
def rutas():
    return {
        'ruta1': {'origen': 'Buenos Aires', 'destino': 'Mendoza'},
        'ruta2': {'origen': 'Buenos Aires', 'destino': 'Córdoba'},
        'ruta3': {'origen': 'Buenos Aires', 'destino': 'Entre Ríos'}
    }

@pytest.fixture
def materiales():
    return {
        "arena": 100,
        "ladrillos": 200,
        "tierra": 150,
        "piedras": 100,
    }

@pytest.fixture
def camiones():
    return {
        "AB 123 CD": {
            'patente': 'AB 123 CD',
            'nombre_transportista': 'Juan Perez',
            'material': 'arena',
            'cantidad': 50,
            'tipo_viaje': 'carga',
            'rutas': {}
        }
    }

@patch("builtins.open", new_callable=mock_open)
def test_guardar_rutas_json(mock_file, rutas):
    guardar_rutas_json(rutas, 'rutas_test.json')
    mock_file.assert_called_once_with('rutas_test.json', 'w', encoding='utf-8')
    mock_file().write.assert_called_once_with(json.dumps(rutas, indent=4, ensure_ascii=False))

@patch("builtins.open", new_callable=mock_open, read_data=json.dumps({'ruta1': {'origen': 'Buenos Aires', 'destino': 'Mendoza'}}))
def test_cargar_rutas_json(mock_file):
    rutas = cargar_rutas_json('rutas_test.json')
    assert rutas == {'ruta1': {'origen': 'Buenos Aires', 'destino': 'Mendoza'}}

@patch("builtins.open", new_callable=mock_open)
def test_guardar_camiones_json(mock_file, camiones):
    guardar_camiones_json(camiones, 'camiones_test.json')
    mock_file.assert_called_once_with('camiones_test.json', 'w', encoding='utf-8')
    mock_file().write.assert_called_once_with(json.dumps(camiones, indent=4, ensure_ascii=False))

@patch("builtins.open", new_callable=mock_open, read_data=json.dumps({"AB 123 CD": {'patente': 'AB 123 CD', 'nombre_transportista': 'Juan Perez', 'material': 'arena', 'cantidad': 50, 'tipo_viaje': 'carga', 'rutas': {}}}))
def test_cargar_camiones_json(mock_file):
    camiones = cargar_camiones_json('camiones_test.json')
    assert camiones == {"AB 123 CD": {'patente': 'AB 123 CD', 'nombre_transportista': 'Juan Perez', 'material': 'arena', 'cantidad': 50, 'tipo_viaje': 'carga', 'rutas': {}}}

@patch("builtins.open", new_callable=mock_open, read_data=json.dumps({"arena": 100, "ladrillos": 200}))
def test_cargar_materiales(mock_file):
    materiales = cargar_materiales('materiales_test.json')
    assert materiales == {"arena": 100, "ladrillos": 200}

@patch("builtins.open", new_callable=mock_open)
def test_guardar_materiales(mock_file, materiales):
    guardar_materiales(materiales, 'materiales_test.json')
    mock_file.assert_called_once_with('materiales_test.json', 'w', encoding='utf-8')
    mock_file().write.assert_called_once_with(json.dumps(materiales, indent=4, ensure_ascii=False))

def test_verificar_rutas_duplicadas():
    camiones = {
        "AB 123 CD": {
            'patente': 'AB 123 CD',
            'nombre_transportista': 'Juan Perez',
            'material': 'arena',
            'cantidad': 50,
            'tipo_viaje': 'carga',
            'rutas': {'Lunes': 'ruta1', 'Martes': 'ruta1'}
        },
        "EF 456 GH": {
            'patente': 'EF 456 GH',
            'nombre_transportista': 'Carlos Lopez',
            'material': 'ladrillos',
            'cantidad': 100,
            'tipo_viaje': 'carga',
            'rutas': {'Lunes': 'ruta1'}
        }
    }
    rutas_duplicadas = verificar_rutas_duplicadas(camiones)
    assert rutas_duplicadas == {'ruta1': [('AB 123 CD', 'Lunes'), ('EF 456 GH', 'Lunes'), ('AB 123 CD', 'Martes')]}

def test_gestionar_stock(camiones):
    stock_actual = {"arena": 100}
    stock_actualizado = gestionar_stock(camiones, stock_actual)
    assert stock_actualizado == {"arena": 150}
