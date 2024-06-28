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

def test_create_orden(test_client):
    response = test_client.post('/orden', json={'id_cli': 1, 'id_carrito': 1, 'fecha': '2024-06-27T12:00:00Z', 'direccion': '123 Calle Falsa', 'total': 100.0})
    assert response.status_code == 200
    assert 'id' in response.json
    assert response.json['id_cli'] == 1
    assert response.json['id_carrito'] == 1

def test_get_ordenes(test_client):
    response = test_client.get('/orden')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_get_orden(test_client):
    response = test_client.get('/orden/1')
    assert response.status_code == 200
    assert 'id' in response.json

def test_update_orden(test_client):
    response = test_client.put('/orden/1', json={'id_cli': 2, 'id_carrito': 2, 'fecha': '2024-07-27T12:00:00Z', 'direccion': '456 Calle Verdadera', 'total': 200.0})
    assert response.status_code == 200
    assert response.json['id_cli'] == 2
    assert response.json['id_carrito'] == 2

def test_delete_orden(test_client):
    response = test_client.delete('/orden/1')
    assert response.status_code == 200
    assert 'id' in response.json
