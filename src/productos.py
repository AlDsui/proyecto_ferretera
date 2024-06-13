from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask (__name__)
app.config['SQL_ALCHEMY_DATABASE_URI']='mysql+pymysql://root@localhost/flaskmysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Producto(db.Model):
    id = db.Column(db.Interger, primary_key=True)
    nombre = db.Column(db.String(70), unique=True)
    descripcion = db.Column(db.String(100))
    
    def __init__(self, nombre, descripcion):
        self.nombre = nombre
        self.descripcion = descripcion

db.create_all()

class ProductoSchema(ma.Schema):
    class Meta:
        fields = ('id','nombre','descripcion')
    
Producto_Schema = ProductoSchema()
Producto_Schema = ProductoSchema(many=True)

@app.route('/producto', methods=['POST'])
def create_producto():
    
    print (request.json)
    return 'received'

    
if __name__ == "__main__":
    app.run(debug=True)