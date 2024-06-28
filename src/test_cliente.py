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

def test_create_cliente(test_client):
    response = test_client.post('/cliente', json={
        'run': '12345678-9', 'nombre': 'Juan', 'apellido': 'Pérez',
        'direccion': '123 Calle Falsa', 'telefono': '123456789',
        'correo': 'juan.perez@example.com'
    })
    assert response.status_code == 200
    assert 'run' in response.json
    assert response.json['nombre'] == 'Juan'

def test_get_clientes(test_client):
    response = test_client.get('/cliente')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_get_single_cliente(test_client):
    response = test_client.get('/cliente/1')
    assert response.status_code == 200
    assert 'run' in response.json

def test_update_cliente(test_client):
    response = test_client.put('/cliente/1', json={
        'run': '12345678-9', 'nombre': 'Juan', 'apellido': 'Gómez',
        'direccion': '456 Calle Verdadera', 'telefono': '987654321',
        'correo': 'juan.gomez@example.com'
    })
    assert response.status_code == 200
    assert response.json['apellido'] == 'Gómez'

def test_delete_cliente(test_client):
    response = test_client.delete('/cliente/1')
    assert response.status_code == 200
    assert 'run' in response.json
