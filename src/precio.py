from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from moldels import *

app = Flask (__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root@localhost/Ferreteria'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class PrecioSchema(ma.Schema):
    class Meta:
        fields = ('id','valor','moneda','estado')
    
precio_schema = PrecioSchema()
precios_schema = PrecioSchema(many=True)

@app.route('/precio', methods=['POST'])
def create_precio():
    
    valor = request.json['valor']
    moneda = request.json['moneda']
    estado = request.json['estado']
    
    new_precio =  Precio(valor, moneda, estado)
    db.session.add(new_precio)
    db.session.commit()
    
    return precio_schema.jsonify(new_precio)

@app.route('/precio', methods=['GET'])
def get_precio():
    all_precio = Precio.query.all()
    result = precio_schema.dump(all_precio)
    return jsonify(result)

@app.route('/precio/<id>', methods=['GET'])
def get_precios(id):
    precio = Precio.query.get(id)
    return precio_schema.jsonify(precio)

@app.route('/precio/<id>', methods=['PUT'])
def update_precio(id):
    precio = Precio.query.get(id)
    
    valor = request.json['valor']
    moneda = request.json['moneda']
    estado = request.json['estado']
    
    precio.valor = valor
    precio.moneda = moneda
    precio.estado = estado
    
    db.session.commit()
    return precio_schema.jsonify(precio)

@app.route('/precio/<id>', methods=['DELETE'])
def delete_precio(id):
    precio = Precio.query.get(id)
    db.session.delete(precio)
    db.session.commit()
    
    return precio_schema.jsonify(precio)


@app.route('/ppp', methods=['GET'])
def index():
    return jsonify({'message': 'welcome to my API baby'})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
