from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from moldels import *


app = Flask (__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root@localhost/Ferreteria'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class ClienteSchema(ma.Schema):
    class Meta:
        fields = ('run','nombre','apellido','direccion','telefono','correo')
    
cliente_schema = ClienteSchema()
clientes_schema = ClienteSchema(many=True)

@app.route('/cliente', methods=['POST'])
def create_cliente():
    run = request.json['run']
    nombre= request.json['nombre']
    apellido = request.json['apellido']
    direccion = request.json['direccion']
    telefono = request.json['telefono']
    correo = request.json['correo']
    
    new_cliente =  Cliente(run, nombre, apellido, direccion, telefono, correo)
    db.session.add(new_cliente)
    db.session.commit()
    
    return cliente_schema.jsonify(new_cliente)

@app.route('/cliente', methods=['GET'])
def get_cliente():
    all_cliente = Cliente.query.all()
    result = clientes_schema.dump(all_cliente)
    return jsonify(result)

@app.route('/cliente/<id>', methods=['GET'])
def get_cliente(id):
    cliente = Cliente.query.get(id)
    return cliente_schema.jsonify(cliente)

@app.route('/cliente/<id>', methods=['PUT'])
def update_cliente(id):
    cliente = Cliente.query.get(id)
    
    run = request.json['run']
    nombre= request.json['nombre']
    apellido = request.json['apellido']
    direccion = request.json['direccion']
    telefono = request.json['telefono']
    correo = request.json['correo']
    
    cliente.run = run
    cliente.nombre = nombre
    cliente.apellido = apellido
    cliente.direccion = direccion
    cliente.telefono = telefono
    cliente.correo = correo
    
    db.session.commit()
    return cliente_schema.jsonify(cliente)

@app.route('/cliente/<id>', methods=['DELETE'])
def delete_cliente(id):
    cliente = Cliente.query.get(id)
    db.session.delete(cliente)
    db.session.commit()
    
    return cliente_schema.jsonify(cliente)


@app.route('/ppp', methods=['GET'])
def index():
    return jsonify({'message': 'welcome to my API baby'})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
