from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from moldels import *

app = Flask (__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root@localhost/Ferreteria'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class PagoSchema(ma.Schema):
    class Meta:
        fields = ('id','nombre','descripcion')
    
producto_schema = ProductoSchema()
productos_schema = ProductoSchema(many=True)

@app.route('/productos', methods=['POST'])
def create_producto():
    
    nombre= request.json['nombre']
    descripcion = request.json['descripcion']
    
    new_producto =  Producto(nombre, descripcion)
    db.session.add(new_producto)
    db.session.commit()
    
    return producto_schema.jsonify(new_producto)

@app.route('/productos', methods=['GET'])
def get_productos():
    all_productos = Producto.query.all()
    result = productos_schema.dump(all_productos)
    return jsonify(result)

@app.route('/productos/<id>', methods=['GET'])
def get_producto(id):
    producto = Producto.query.get(id)
    return producto_schema.jsonify(producto)

@app.route('/productos/<id>', methods=['PUT'])
def update_productos(id):
    producto = Producto.query.get(id)
    
    nombre = request.json['nombre']
    descripcion = request.json['descripcion']
    
    producto.nombre = nombre
    producto.descripcion = descripcion
    
    db.session.commit()
    return producto_schema.jsonify(producto)

@app.route('/producto/<id>', methods=['DELETE'])
def delete_producto(id):
    producto = Producto.query.get(id)
    db.session.delete(producto)
    db.session.commit()
    
    return producto_schema.jsonify(producto)


@app.route('/ppp', methods=['GET'])
def index():
    return jsonify({'message': 'welcome to my API baby'})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
