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

def test_create_producto(test_client):
    response = test_client.post('/productos', json={'nombre': 'Producto1', 'descripcion': 'Descripción del Producto1'})
    assert response.status_code == 200
    assert 'id' in response.json
    assert response.json['nombre'] == 'Producto1'
    assert response.json['descripcion'] == 'Descripción del Producto1'

def test_get_productos(test_client):
    response = test_client.get('/productos')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_get_producto(test_client):
    response = test_client.get('/productos/1')
    assert response.status_code == 200
    assert 'id' in response.json

def test_update_producto(test_client):
    response = test_client.put('/productos/1', json={'nombre': 'Producto Actualizado', 'descripcion': 'Descripción Actualizada'})
    assert response.status_code == 200
    assert response.json['nombre'] == 'Producto Actualizado'
    assert response.json['descripcion'] == 'Descripción Actualizada'

def test_delete_producto(test_client):
    response = test_client.delete('/productos/1')
    assert response.status_code == 200
    assert 'id' in response.json
