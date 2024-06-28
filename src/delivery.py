from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from moldels import *

app = Flask (__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root@localhost/Ferreteria'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class DeliverySchema(ma.Schema):
    class Meta:
        fields = ('id_orden','f_entrega','direccion','est_entrega','conductor','patente_transp','costo_envio')
    
delivery_schema = DeliverySchema()
deliverys_schema = DeliverySchema(many=True)

@app.route('/delivery', methods=['POST'])
def create_delivery():
    
    id_orden= request.json['id_orden']
    f_entrega = request.json['f_entrega']
    direccion = request.json['direccion']
    est_entrega = request.json['est_entrega']
    conductor = request.json['conductor']
    patente_transp = request.json['patente_transp']
    costo_envio = request.json['costo_envio']
    
    new_delivery =  Delivery(id_orden, f_entrega, direccion,  est_entrega, conductor, patente_transp, costo_envio)
    db.session.add(new_delivery)
    db.session.commit()
    
    return delivery_schema.jsonify(new_delivery)

@app.route('/delivery', methods=['GET'])
def get_delivery():
    all_deliverys = Delivery.query.all()
    result = deliverys_schema.dump(all_deliverys)
    return jsonify(result)

@app.route('/delivery/<id>', methods=['GET'])
def get_delivery(id):
    delivery = Delivery.query.get(id)
    return delivery_schema.jsonify(delivery)

@app.route('/delivery/<id>', methods=['PUT'])
def update_delivery(id):
    delivery = Delivery.query.get(id)
    
    id_orden = request.json['id_orden']
    f_entrega = request.json['f_entrega']
    direccion = request.json['direccion']
    est_entrega = request.json['est_entrega']
    conductor = request.json['conductor']
    patente_transp = request.json['patente_transp']
    costo_envio = request.json['costo_envio']
    
    delivery.id_orden = id_orden
    delivery.f_entrega = f_entrega
    delivery.direccion = direccion
    delivery.est_entrega = est_entrega
    delivery.conductor = conductor
    delivery.patente_transp = patente_transp
    delivery.costo_envio = costo_envio
    
    db.session.commit()
    return delivery_schema.jsonify(delivery)

@app.route('/delivery/<id>', methods=['DELETE'])
def delete_delivery(id):
    delivery = Delivery.query.get(id)
    db.session.delete(delivery)
    db.session.commit()
    
    return delivery_schema.jsonify(delivery)


@app.route('/ppp', methods=['GET'])
def index():
    return jsonify({'message': 'welcome to my API baby'})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
