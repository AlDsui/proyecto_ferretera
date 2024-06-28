import pytest
from flask import Flask
from pagos import app, db, Pagos

@pytest.fixture(scope='module')
def test_client():
    flask_app = app
    testing_client = flask_app.test_client()

    # Establece el contexto de la aplicación
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # Pruebas aquí

    ctx.pop()

def test_create_pago(test_client):
    response = test_client.post('/pagos', json={
        'id_orden': 1,
        'monto': 100.0,
        'fecha': '2023-06-28',
        'met_pago': 'tarjeta',
        'estatus': 'pagado',
        'tarjeta': '1234567812345678'
    })
    assert response.status_code == 201
    assert 'id' in response.json
    assert response.json['monto'] == 100.0
    assert response.json['met_pago'] == 'tarjeta'
    assert response.json['estatus'] == 'pagado'

def test_get_pagos(test_client):
    response = test_client.get('/pagos')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_get_pago(test_client):
    response = test_client.get('/pagos/1')
    assert response.status_code == 200
    assert 'id' in response.json

def test_update_pago(test_client):
    response = test_client.put('/pagos/1', json={
        'id_orden': 1,
        'monto': 150.0,
        'fecha': '2023-06-28',
        'met_pago': 'tarjeta',
        'estatus': 'pendiente',
        'tarjeta': '1234567812345678'
    })
    assert response.status_code == 200
    assert response.json['monto'] == 150.0
    assert response.json['estatus'] == 'pendiente'

def test_delete_pago(test_client):
    response = test_client.delete('/pagos/1')
    assert response.status_code == 200
    assert 'id' in response.json

def test_create_pago_invalid_data(test_client):
    response = test_client.post('/pagos', json={
        'id_orden': 1,
        'monto': -100.0,
        'fecha': '2023-06-28',
        'met_pago': '',
        'estatus': 'pagado',
        'tarjeta': '12345678'
    })
    assert response.status_code == 400
    assert 'error' in response.json

def test_update_pago_invalid_data(test_client):
    response = test_client.put('/pagos/1', json={
        'id_orden': 1,
        'monto': 150.0,
        'fecha': '2023-06-28',
        'met_pago': 'tarjeta',
        'estatus': 'unknown',
        'tarjeta': '1234567812345678'
    })
    assert response.status_code == 400
    assert 'error' in response.json
