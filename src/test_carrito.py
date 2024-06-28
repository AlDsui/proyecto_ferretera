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

def test_create_carrito(test_client):
    response = test_client.post('/carritos', json={
        'id_producto': 1,
        'id_cli': 1,
        'nombre': 'Martillo',
        'descripcion': 'Martillo de acero',
        'costo': 15.99,
        'cantidad': 2
    })
    assert response.status_code == 200
    assert 'id' in response.json
    assert response.json['nombre'] == 'Martillo'

def test_get_carritos(test_client):
    response = test_client.get('/carritos')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_get_single_carrito(test_client):
    response = test_client.get('/carritos/1')
    assert response.status_code == 200
    assert 'id' in response.json

def test_update_carrito(test_client):
    response = test_client.put('/carritos/1', json={
        'id_producto': 1,
        'id_cli': 1,
        'nombre': 'Martillo Actualizado',
        'descripcion': 'Martillo de acero inoxidable',
        'costo': 17.99,
        'cantidad': 3
    })
    assert response.status_code == 200
    assert response.json['nombre'] == 'Martillo Actualizado'

def test_delete_carrito(test_client):
    response = test_client.delete('/carritos/1')
    assert response.status_code == 200
    assert 'id' in response.json

def test_create_carrito_invalid_data(client):
    response = client.post('/carritos', json={
        'id_producto': -1,
        'id_cli': 1,
        'nombre': 'Producto',
        'descripcion': 'Descripción',
        'costo': -10.0,
        'cantidad': 5
    })
    assert response.status_code == 400

def test_update_carrito_invalid_data(client):
    response = client.put('/carritos/1', json={
        'id_producto': 1,
        'id_cli': 1,
        'nombre': 'Producto',
        'descripcion': 'Descripción',
        'costo': 10.0,
        'cantidad': -5
    })
    assert response.status_code == 400