from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from moldels import *

app = Flask (__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root@localhost/Ferreteria'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class OrdenSchema(ma.Schema):
    class Meta:
        fields = ('id','id_cli','id_carrito','fecha','direccion','total')
    
orden_schema = OrdenSchema()
ordenes_schema = OrdenSchema(many=True)

@app.route('/orden', methods=['POST'])
def create_orden():
    
    id_cli = request.json['id_cli']
    id_carrito = request.json['id_carrito']
    fecha = request.json['fecha']
    direccion = request.json['direccion']
    total = request.json['total']
    
    
    new_orden =  Orden(id_cli, id_carrito, fecha, direccion, total)
    db.session.add(new_orden)
    db.session.commit()
    
    return orden_schema.jsonify(new_orden)

@app.route('/orden', methods=['GET'])
def get_ordenes():
    all_orden = Orden.query.all()
    result = ordenes_schema.dump(all_orden)
    return jsonify(result)

@app.route('/orden/<id>', methods=['GET'])
def get_orden(id):
    orden = Orden.query.get(id)
    return orden_schema.jsonify(orden)

@app.route('/orden/<id>', methods=['PUT'])
def update_orden(id):
    orden = Orden.query.get(id)
    
    id_cli = request.json['id_cli']
    id_carrito = request.json['id_carrito']
    fecha = request.json['fecha']
    direccion = request.json['direccion']
    total = request.json['total']
    
    orden.id_cli = id_cli
    orden.id_carrito = id_carrito
    orden.fecha = fecha
    orden.direccion = direccion
    orden.total = total
    
    db.session.commit()
    return orden_schema.jsonify(orden)

@app.route('/orden/<id>', methods=['DELETE'])
def delete_orden(id):
    orden = Orden.query.get(id)
    db.session.delete(orden)
    db.session.commit()
    
    return orden_schema.jsonify(orden)


@app.route('/ppp', methods=['GET'])
def index():
    return jsonify({'message': 'welcome to my API baby'})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
