from flask import Flask, request, jsonify
from models1 import db, User, create_user, authenticate_user, update_user, delete_user
from moldels import *

# Configuración de la base de datos
app = Flask (__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root@localhost/Ferreteria'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db.init_app(app)

# Crear las tablas de la base de datos antes de la primera solicitud
@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/users', methods=['POST'])
def create_new_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({'mensaje': 'Username o Email ya se encuentra registrado'}), 400

    create_user(username, email, password)
    return jsonify({'mensaje': 'User creado exitosamente'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if authenticate_user(username, password):
        return jsonify({'mensaje': 'Autenticado exitosamente'}), 200
    return jsonify({'mensaje': 'Username o password invalidos'}), 400

@app.route('/users/<username>', methods=['PUT'])
def update_existing_user(username):
    data = request.get_json()
    new_email = data.get('email')
    new_password = data.get('password')

    update_user(username, new_email, new_password)
    return jsonify({'mensaje': 'User actualizado exitosamente'}), 200

@app.route('/users/<username>', methods=['DELETE'])
def delete_existing_user(username):
    delete_user(username)
    return jsonify({'message': 'User eliminado exitosamente'}), 200

if __name__ == '__main__':
    app.run(debug=True)
