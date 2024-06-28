from sqlite3 import IntegrityError
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/Ferreteria'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(70), unique=True)
    descripcion = db.Column(db.String(100))

    def __init__(self, nombre, descripcion):
        self.nombre = nombre
        self.descripcion = descripcion

class ProductoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Producto
        load_instance = True

producto_schema = ProductoSchema()
productos_schema = ProductoSchema(many=True)

@app.route('/productos', methods=['POST'])
def create_producto():
    try:
        nombre = request.json['nombre']
        descripcion = request.json['descripcion']

        new_producto = Producto(nombre=nombre, descripcion=descripcion)
        db.session.add(new_producto)
        db.session.commit()

        return producto_schema.jsonify(new_producto), 201  # 201: Created
    except KeyError as e:
        return jsonify({'message': 'Falta el campo requerido: ' + str(e)}), 400  # 400: Bad Request
    except Exception as e:
        return jsonify({'message': 'Error al procesar la solicitud: ' + str(e)}), 500  # 500: Internal Server Error

@app.route('/productos', methods=['GET'])
def get_productos():
    try:
        all_productos = Producto.query.all()
        result = productos_schema.dump(all_productos)
        return jsonify(result)
    except Exception as e:
        return jsonify({'message': 'Error al obtener los productos: ' + str(e)}), 500

@app.route('/productos/<int:id>', methods=['GET'])
def get_producto(id):
    try:
        producto = Producto.query.get(id)
        if producto:
            return producto_schema.jsonify(producto)
        else:
            return jsonify({'message': 'Producto no encontrado'}), 404  # 404: Not Found
    except Exception as e:
        return jsonify({'message': 'Error al obtener el producto: ' + str(e)}), 500

@app.route('/productos/<int:id>', methods=['PUT'])
def update_producto(id):
    try:
        producto = Producto.query.get(id)
        if producto:
            nombre = request.json['nombre']
            descripcion = request.json['descripcion']
            
            producto.nombre = nombre
            producto.descripcion = descripcion
            
            db.session.commit()
            return producto_schema.jsonify(producto)
        else:
            return jsonify({'message': 'Producto no encontrado'}), 404
    except KeyError as e:
        return jsonify({'message': 'Falta el campo requerido: ' + str(e)}), 400
    except Exception as e:
        return jsonify({'message': 'Error al actualizar el producto: ' + str(e)}), 500

@app.route('/productos/<int:id>', methods=['DELETE'])
def delete_producto(id):
    try:
        producto = Producto.query.get(id)
        if producto:
            db.session.delete(producto)
            db.session.commit()
            return jsonify({'message': 'Producto eliminado correctamente'})
        else:
            return jsonify({'message': 'Producto no encontrado'}), 404
    except IntegrityError as e:
        db.session.rollback()  # Revertir cualquier cambio pendiente en la transacción
        return jsonify({'error': 'No se puede eliminar el producto debido a restricciones de integridad'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ppp', methods=['GET'])
def index():
    return jsonify({'message': 'Welcome to my API'})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
