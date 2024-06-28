from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from moldels import *

app = Flask (__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root@localhost/Ferreteria'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class InventarioSchema(ma.Schema):
    class Meta:
        fields = ('id','nombre','descripcion','categoria','precio_unit','cant_disp','cant_minima','f_adqu','f_venc')
    
inventario_schema = InventarioSchema()
inventarios_schema = InventarioSchema(many=True)

@app.route('/inventario', methods=['POST'])
def create_inventario():
    
    nombre= request.json['nombre']
    descripcion = request.json['descripcion']
    categoria = request.json['categoria']
    precio_unit = request.json['precio_unit']
    cant_disp = request.json['cant_disp']
    cant_minima = request.json['cant_minima']
    f_adqu = request.json['f_adqu']
    f_venc = request.json['f_venc']
    
    new_inventario =  Inventario(nombre, descripcion, categoria, precio_unit, cant_disp, cant_minima, f_adqu, f_venc)
    db.session.add(new_inventario)
    db.session.commit()
    
    return inventario_schema.jsonify(new_inventario)

@app.route('/inventario', methods=['GET'])
def get_inventario():
    all_inventario = Inventario.query.all()
    result = inventarios_schema.dump(all_inventario)
    return jsonify(result)

@app.route('/inventario/<id>', methods=['GET'])
def get_inventario(id):
    inventario = Inventario.query.get(id)
    return inventario_schema.jsonify()

@app.route('/inventario/<id>', methods=['PUT'])
def update_inventario(id):
    inventario = Inventario.query.get(id)
    
    nombre = request.json['nombre']
    descripcion = request.json['descripcion']
    categoria = request.json['categoria']
    precio_unit = request.json['precio_unit']
    cant_disp = request.json['cant_disp']
    f_adqu = request.json['f_adqu']
    f_venc = request.json['f_venc']
    
    inventario.nombre = nombre
    inventario.descripcion = descripcion
    inventario.categoria = categoria
    inventario.precio_unit = precio_unit
    inventario.cant_disp = cant_disp
    inventario.f_adqu = f_adqu
    inventario.f_venc = f_venc
    
    db.session.commit()
    return inventario_schema.jsonify(inventario)

@app.route('/inventario/<id>', methods=['DELETE'])
def delete_inventario(id):
    inventario = Inventario.query.get(id)
    db.session.delete(inventario)
    db.session.commit()
    
    return inventario_schema.jsonify(inventario)


@app.route('/ppp', methods=['GET'])
def index():
    return jsonify({'message': 'welcome to my API baby'})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
