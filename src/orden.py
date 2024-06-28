from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from moldels import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/Ferreteria'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class OrdenSchema(ma.Schema):
    class Meta:
        fields = ('id', 'id_cli', 'id_carrito', 'fecha', 'direccion', 'total')

orden_schema = OrdenSchema()
ordenes_schema = OrdenSchema(many=True)

@app.route('/orden', methods=['POST'])
def create_orden():
    try:
        id_cli = request.json.get('id_cli')
        id_carrito = request.json.get('id_carrito')
        fecha = request.json.get('fecha')
        direccion = request.json.get('direccion')
        total = request.json.get('total')

        if not id_cli or not isinstance(id_cli, int):
            return jsonify({"error": "id_cli es requerido y debe ser un entero"}), 400
        if not id_carrito or not isinstance(id_carrito, int):
            return jsonify({"error": "id_carrito es requerido y debe ser un entero"}), 400
        if not fecha:
            return jsonify({"error": "fecha es requerida"}), 400
        if not direccion or not isinstance(direccion, str):
            return jsonify({"error": "direccion es requerida y debe ser una cadena"}), 400
        if not total or not isinstance(total, float):
            return jsonify({"error": "total es requerido y debe ser un número flotante"}), 400

        new_orden = Orden(id_cli, id_carrito, fecha, direccion, total)
        db.session.add(new_orden)
        db.session.commit()

        return orden_schema.jsonify(new_orden), 201

    except KeyError as e:
        return jsonify({"error": f"Campo faltante: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/orden', methods=['GET'])
def get_ordenes():
    try:
        all_orden = Orden.query.all()
        result = ordenes_schema.dump(all_orden)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/orden/<id>', methods=['GET'])
def get_orden(id):
    try:
        orden = Orden.query.get(id)
        if orden is None:
            return jsonify({"error": "Orden no encontrada"}), 404
        return orden_schema.jsonify(orden), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/orden/<id>', methods=['PUT'])
def update_orden(id):
    try:
        orden = Orden.query.get(id)
        if orden is None:
            return jsonify({"error": "Orden no encontrada"}), 404

        id_cli = request.json.get('id_cli')
        id_carrito = request.json.get('id_carrito')
        fecha = request.json.get('fecha')
        direccion = request.json.get('direccion')
        total = request.json.get('total')

        if not id_cli or not isinstance(id_cli, int):
            return jsonify({"error": "id_cli es requerido y debe ser un entero"}), 400
        if not id_carrito or not isinstance(id_carrito, int):
            return jsonify({"error": "id_carrito es requerido y debe ser un entero"}), 400
        if not fecha:
            return jsonify({"error": "fecha es requerida"}), 400
        if not direccion or not isinstance(direccion, str):
            return jsonify({"error": "direccion es requerida y debe ser una cadena"}), 400
        if not total or not isinstance(total, float):
            return jsonify({"error": "total es requerido y debe ser un número flotante"}), 400

        orden.id_cli = id_cli
        orden.id_carrito = id_carrito
        orden.fecha = fecha
        orden.direccion = direccion
        orden.total = total

        db.session.commit()
        return orden_schema.jsonify(orden), 200

    except KeyError as e:
        return jsonify({"error": f"Campo faltante: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/orden/<id>', methods=['DELETE'])
def delete_orden(id):
    try:
        orden = Orden.query.get(id)
        if orden is None:
            return jsonify({"error": "Orden no encontrada"}), 404

        db.session.delete(orden)
        db.session.commit()

        return orden_schema.jsonify(orden), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ppp', methods=['GET'])
def index():
    return jsonify({'message': 'welcome to my API baby'}), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
