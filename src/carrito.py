from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from productos import Producto
from moldels import *

app = Flask (__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root@localhost/Ferreteria'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
ma = Marshmallow(app)



class CarritoSchema(ma.Schema):
    class Meta:
        fields = ('id','id_producto', 'id_cli','nombre','descripcion','costo','cantidad')
    
carrito_schema = CarritoSchema()
carritos_schema = CarritoSchema(many=True)

@app.route('/carritos', methods=['POST'])
def create_carrito():
    
    id_producto = request.json['id_producto']
    id_cli = request.json['id_cli']
    nombre= request.json['nombre']
    descripcion = request.json['descripcion']
    costo = request.json['costo']
    cantidad = request.json['cantidad']
    
    new_carrito =  Carrito(id_producto, id_cli, nombre, descripcion, costo, cantidad)
    db.session.add(new_carrito)
    db.session.commit()
    
    return carrito_schema.jsonify(new_carrito)

@app.route('/carritos', methods=['GET'])
def get_carritos():
    all_productos = Producto.query.all()
    result = carritos_schema.dump(all_productos)
    return jsonify(result)

@app.route('/carritos/<id>', methods=['GET'])
def get_carrito(id):
    carrito = Carrito.query.get(id)
    return carrito_schema.jsonify(carrito)

@app.route('/carritos/<id>', methods=['PUT'])
def update_carrito(id):
    carrito = Carrito.query.get(id)
    
    id_producto = request.json['id_producto']
    id_cli = request.json['id_cli']
    nombre = request.json['nombre']
    descripcion = request.json['descripcion']
    costo = request.json['costo']
    cantidad = request.json['cantidad']
    
    carrito.id_producto = id_producto
    carrito.id_cli = id_cli
    carrito.nombre = nombre
    carrito.descripcion = descripcion
    carrito.costo = costo
    carrito.cantidad = cantidad
    
    db.session.commit()
    return carrito_schema.jsonify(carrito)

@app.route('/carrito/<id>', methods=['DELETE'])
def delete_carrito(id):
    carrito = Carrito.query.get(id)
    db.session.delete(carrito)
    db.session.commit()
    
    return carrito_schema.jsonify(carrito)


@app.route('/ppp', methods=['GET'])
def index():
    return jsonify({'message': 'welcome to my API baby'})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)