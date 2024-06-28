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

def test_create_delivery(test_client):
    response = test_client.post('/delivery', json={
        'id_orden': 1, 'f_entrega': '2024-01-01', 'direccion': '123 Calle Falsa',
        'est_entrega': 'En camino', 'conductor': 'Juan Pérez', 'patente_transp': 'ABC123',
        'costo_envio': 15.0
    })
    assert response.status_code == 200
    assert 'id_orden' in response.json
    assert response.json['direccion'] == '123 Calle Falsa'

def test_get_deliveries(test_client):
    response = test_client.get('/delivery')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_get_single_delivery(test_client):
    response = test_client.get('/delivery/1')
    assert response.status_code == 200
    assert 'id_orden' in response.json

def test_update_delivery(test_client):
    response = test_client.put('/delivery/1', json={
        'id_orden': 1, 'f_entrega': '2024-02-01', 'direccion': '456 Calle Verdadera',
        'est_entrega': 'Entregado', 'conductor': 'Pedro Gómez', 'patente_transp': 'XYZ789',
        'costo_envio': 20.0
    })
    assert response.status_code == 200
    assert response.json['direccion'] == '456 Calle Verdadera'

def test_delete_delivery(test_client):
    response = test_client.delete('/delivery/1')
    assert response.status_code == 200
    assert 'id_orden' in response.json
