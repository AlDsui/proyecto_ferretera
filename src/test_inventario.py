import pytest
from flask import Flask
from pagos import app, db, Producto
@pytest.fixture(scope='module')
def test_client():
    flask_app = app
    testing_client = flask_app.test_client()

    # Establece el contexto de la aplicación
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # Pruebas aquí

    ctx.pop()

def test_create_inventario(test_client):
    response = test_client.post('/inventario', json={
        'nombre': 'Producto A', 'descripcion': 'Descripción del producto A',
        'categoria': 'Categoría A', 'precio_unit': 10.0, 'cant_disp': 100,
        'cant_minima': 10, 'f_adqu': '2024-01-01', 'f_venc': '2024-12-31'
    })
    assert response.status_code == 200
    assert 'id' in response.json
    assert response.json['nombre'] == 'Producto A'

def test_get_inventario(test_client):
    response = test_client.get('/inventario')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_get_single_inventario(test_client):
    response = test_client.get('/inventario/1')
    assert response.status_code == 200
    assert 'id' in response.json

def test_update_inventario(test_client):
    response = test_client.put('/inventario/1', json={
        'nombre': 'Producto B', 'descripcion': 'Descripción del producto B',
        'categoria': 'Categoría B', 'precio_unit': 20.0, 'cant_disp': 200,
        'cant_minima': 20, 'f_adqu': '2024-01-01', 'f_venc': '2024-12-31'
    })
    assert response.status_code == 200
    assert response.json['nombre'] == 'Producto B'

def test_delete_inventario(test_client):
    response = test_client.delete('/inventario/1')
    assert response.status_code == 200
    assert 'id' in response.json
    

def test_create_inventario_invalid_data(client):
    response = client.post('/inventario', json={
        'nombre': 'Producto',
        'descripcion': 'Descripción',
        'categoria': '',
        'precio_unit': -5.0,
        'cant_disp': 10,
        'cant_minima': 2,
        'f_adqu': '2024-01-01',
        'f_venc': '2023-12-31'  # Fecha de vencimiento antes que fecha de adquisición
    })
    assert response.status_code == 400

def test_update_inventario_invalid_data(client):
    response = client.put('/inventario/1', json={
        'nombre': '',
        'descripcion': 'Descripción',
        'categoria': 'Categoría',
        'precio_unit': 10.0,
        'cant_disp': -5,
        'cant_minima': 2,
        'f_adqu': '2024-01-01',
        'f_venc': '2023-12-31'  # Fecha de vencimiento antes que fecha de adquisición
    })
    assert response.status_code == 400

