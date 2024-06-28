import pytest
from flask import Flask
from productos import app, db, Producto

@pytest.fixture(scope='module')
def test_app():
    """Fixture para inicializar la aplicación Flask en modo de prueba."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

def test_create_producto(test_app):
    """Prueba la creación de un producto."""
    client = test_app.test_client()
    response = client.post('/productos', json={'nombre': 'Martillo', 'descripcion': 'Martillo de acero'})
    assert response.status_code == 200
    assert response.json['nombre'] == 'Martillo'

def test_get_productos(test_app):
    """Prueba la obtención de todos los productos."""
    client = test_app.test_client()
    response = client.get('/productos')
    assert response.status_code == 200
    assert len(response.json) > 0

def test_get_producto(test_app):
    """Prueba la obtención de un producto específico."""
    client = test_app.test_client()
    response = client.post('/productos', json={'nombre': 'Destornillador', 'descripcion': 'Destornillador plano'})
    producto_id = response.json['id']

    response = client.get(f'/productos/{producto_id}')
    assert response.status_code == 200
    assert response.json['nombre'] == 'Destornillador'

def test_update_producto(test_app):
    """Prueba la actualización de un producto."""
    client = test_app.test_client()
    response = client.post('/productos', json={'nombre': 'Llave inglesa', 'descripcion': 'Llave inglesa ajustable'})
    producto_id = response.json['id']

    response = client.put(f'/productos/{producto_id}', json={'nombre': 'Llave ajustable', 'descripcion': 'Llave inglesa ajustable'})
    assert response.status_code == 200
    assert response.json['nombre'] == 'Llave ajustable'

def test_delete_producto(test_app):
    """Prueba la eliminación de un producto."""
    client = test_app.test_client()
    response = client.post('/productos', json={'nombre': 'Sierra eléctrica', 'descripcion': 'Sierra circular eléctrica'})
    producto_id = response.json['id']

    response = client.delete(f'/productos/{producto_id}')
    assert response.status_code == 200
    assert response.json['nombre'] == 'Sierra eléctrica'

