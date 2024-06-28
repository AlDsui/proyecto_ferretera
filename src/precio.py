from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from moldels import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/Ferreteria'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class PrecioSchema(ma.Schema):
    class Meta:
        fields = ('id', 'valor', 'moneda', 'estado')

precio_schema = PrecioSchema()
precios_schema = PrecioSchema(many=True)

@app.route('/precio', methods=['POST'])
def create_precio():
    try:
        valor = request.json['valor']
        moneda = request.json['moneda']
        estado = request.json['estado']
        
        if not isinstance(valor, (int, float)) or valor <= 0:
            return jsonify({"error": "Valor debe ser un número positivo"}), 400
        
        if not moneda or not isinstance(moneda, str):
            return jsonify({"error": "Moneda es requerida y debe ser una cadena"}), 400
        
        if not estado or not isinstance(estado, str):
            return jsonify({"error": "Estado es requerido y debe ser una cadena"}), 400
        
        new_precio = Precio(valor, moneda, estado)
        db.session.add(new_precio)
        db.session.commit()
        
        return precio_schema.jsonify(new_precio), 201

    except KeyError as e:
        return jsonify({"error": f"Campo faltante: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/precio', methods=['GET'])
def get_precio():
    try:
        all_precio = Precio.query.all()
        result = precios_schema.dump(all_precio)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/precio/<id>', methods=['GET'])
def get_precio_by_id(id):
    try:
        precio = Precio.query.get(id)
        if precio is None:
            return jsonify({"error": "Precio no encontrado"}), 404
        return precio_schema.jsonify(precio), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/precio/<id>', methods=['PUT'])
def update_precio(id):
    try:
        precio = Precio.query.get(id)
        if precio is None:
            return jsonify({"error": "Precio no encontrado"}), 404

        valor = request.json['valor']
        moneda = request.json['moneda']
        estado = request.json['estado']
        
        if not isinstance(valor, (int, float)) or valor <= 0:
            return jsonify({"error": "Valor debe ser un número positivo"}), 400
        
        if not moneda or not isinstance(moneda, str):
            return jsonify({"error": "Moneda es requerida y debe ser una cadena"}), 400
        
        if not estado or not isinstance(estado, str):
            return jsonify({"error": "Estado es requerido y debe ser una cadena"}), 400
        
        precio.valor = valor
        precio.moneda = moneda
        precio.estado = estado
        
        db.session.commit()
        return precio_schema.jsonify(precio), 200

    except KeyError as e:
        return jsonify({"error": f"Campo faltante: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/precio/<id>', methods=['DELETE'])
def delete_precio(id):
    try:
        precio = Precio.query.get(id)
        if precio is None:
            return jsonify({"error": "Precio no encontrado"}), 404

        db.session.delete(precio)
        db.session.commit()
        
        return precio_schema.jsonify(precio), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ppp', methods=['GET'])
def index():
    return jsonify({'message': 'welcome to my API baby'}), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
