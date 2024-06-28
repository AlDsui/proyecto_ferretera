import pytest
from flask import Flask
from precio import app, db, Producto

@pytest.fixture(scope='module')
def test_client():
    flask_app = app
    testing_client = flask_app.test_client()

    # Establece el contexto de la aplicación
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # Pruebas aquí

    ctx.pop()

def test_create_precio(test_client):
    response = test_client.post('/precio', json={'valor': 100.0, 'moneda': 'USD', 'estado': 'activo'})
    assert response.status_code == 200
    assert 'id' in response.json
    assert response.json['valor'] == 100.0
    assert response.json['moneda'] == 'USD'
    assert response.json['estado'] == 'activo'

def test_get_precio(test_client):
    response = test_client.get('/precio')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_get_precios(test_client):
    response = test_client.get('/precio/1')
    assert response.status_code == 200
    assert 'id' in response.json

def test_update_precio(test_client):
    response = test_client.put('/precio/1', json={'valor': 150.0, 'moneda': 'USD', 'estado': 'inactivo'})
    assert response.status_code == 200
    assert response.json['valor'] == 150.0
    assert response.json['estado'] == 'inactivo'

def test_delete_precio(test_client):
    response = test_client.delete('/precio/1')
    assert response.status_code == 200
    assert 'id' in response.json
    
    
def test_create_precio_invalid_data(client):
    response = client.post('/precio', json={
        'valor': -10.0,
        'moneda': '',
        'estado': 'Activo'
    })
    assert response.status_code == 400

def test_update_precio_invalid_data(client):
    response = client.put('/precio/1', json={
        'valor': 10.0,
        'moneda': 'USD',
        'estado': ''
    })
    assert response.status_code == 400
