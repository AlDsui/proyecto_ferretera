from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from moldels import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/Ferreteria'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class PagoSchema(ma.Schema):
    class Meta:
        fields = ('id_orden', 'monto', 'fecha', 'met_pago', 'estatus', 'tarjeta')

pago_schema = PagoSchema()
pagos_schema = PagoSchema(many=True)

@app.route('/pagos', methods=['POST'])
def create_pago():
    try:
        id_orden = request.json.get('id_orden')
        monto = request.json.get('monto')
        fecha = request.json.get('fecha')
        met_pago = request.json.get('met_pago')
        estatus = request.json.get('estatus')
        tarjeta = request.json.get('tarjeta')

        if not id_orden or not isinstance(id_orden, int):
            return jsonify({"error": "id_orden es requerido y debe ser un entero"}), 400
        if not monto or not isinstance(monto, float):
            return jsonify({"error": "Monto es requerido y debe ser un número flotante"}), 400
        if not fecha:
            return jsonify({"error": "Fecha es requerida"}), 400
        if not met_pago or not isinstance(met_pago, str):
            return jsonify({"error": "Método de pago es requerido y debe ser una cadena"}), 400
        if not estatus or not isinstance(estatus, str):
            return jsonify({"error": "Estatus es requerido y debe ser una cadena"}), 400
        if not tarjeta or not isinstance(tarjeta, str):
            return jsonify({"error": "Tarjeta es requerida y debe ser una cadena"}), 400

        new_pago = Pagos(id_orden, monto, fecha, met_pago, estatus, tarjeta)
        db.session.add(new_pago)
        db.session.commit()

        return pago_schema.jsonify(new_pago), 201

    except KeyError as e:
        return jsonify({"error": f"Campo faltante: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/pagos', methods=['GET'])
def get_pagos():
    try:
        all_pagos = Pagos.query.all()
        result = pagos_schema.dump(all_pagos)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/pagos/<id>', methods=['GET'])
def get_pago(id):
    try:
        pago = Pagos.query.get(id)
        if pago is None:
            return jsonify({"error": "Pago no encontrado"}), 404
        return pago_schema.jsonify(pago), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/pagos/<id>', methods=['PUT'])
def update_pago(id):
    try:
        pago = Pagos.query.get(id)
        if pago is None:
            return jsonify({"error": "Pago no encontrado"}), 404

        id_orden = request.json.get('id_orden')
        monto = request.json.get('monto')
        fecha = request.json.get('fecha')
        met_pago = request.json.get('met_pago')
        estatus = request.json.get('estatus')
        tarjeta = request.json.get('tarjeta')

        if not id_orden or not isinstance(id_orden, int):
            return jsonify({"error": "id_orden es requerido y debe ser un entero"}), 400
        if not monto or not isinstance(monto, float):
            return jsonify({"error": "Monto es requerido y debe ser un número flotante"}), 400
        if not fecha:
            return jsonify({"error": "Fecha es requerida"}), 400
        if not met_pago or not isinstance(met_pago, str):
            return jsonify({"error": "Método de pago es requerido y debe ser una cadena"}), 400
        if not estatus or not isinstance(estatus, str):
            return jsonify({"error": "Estatus es requerido y debe ser una cadena"}), 400
        if not tarjeta or not isinstance(tarjeta, str):
            return jsonify({"error": "Tarjeta es requerida y debe ser una cadena"}), 400

        pago.id_orden = id_orden
        pago.monto = monto
        pago.fecha = fecha
        pago.met_pago = met_pago
        pago.estatus = estatus
        pago.tarjeta = tarjeta

        db.session.commit()
        return pago_schema.jsonify(pago), 200

    except KeyError as e:
        return jsonify({"error": f"Campo faltante: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/pagos/<id>', methods=['DELETE'])
def delete_pago(id):
    try:
        pago = Pagos.query.get(id)
        if pago is None:
            return jsonify({"error": "Pago no encontrado"}), 404

        db.session.delete(pago)
        db.session.commit()

        return pago_schema.jsonify(pago), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ppp', methods=['GET'])
def index():
    return jsonify({'message': 'welcome to my API baby'}), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
