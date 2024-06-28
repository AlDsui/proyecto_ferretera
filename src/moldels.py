from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/Ferreteria'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(70), unique=True)
    descripcion = db.Column(db.String(100))
    
    carritos = db.relationship('Carrito', back_populates='producto')
    
    def __init__(self, nombre, descripcion):
        self.nombre = nombre
        self.descripcion = descripcion


class Precio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Integer)
    moneda = db.Column(db.String(30))
    estado = db.Column(db.Boolean, default=True)
    
    def __init__(self, valor, moneda, estado):
        self.valor = valor
        self.moneda = moneda
        self.estado = estado


class Orden(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_cli = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    id_carrito = db.Column(db.Integer, db.ForeignKey('carrito.id'))
    fecha = db.Column(db.Date)
    direccion = db.Column(db.String(70))
    total = db.Column(db.Integer)
    
    cliente = db.relationship('Cliente', back_populates='ordenes')
    carrito = db.relationship('Carrito', back_populates='ordenes')
    pagos = db.relationship('Pagos', back_populates='orden')
    
    def __init__(self, id_cli, id_carrito, fecha, direccion, total):
        self.id_cli = id_cli
        self.id_carrito = id_carrito
        self.fecha = fecha
        self.direccion = direccion
        self.total = total


class Inventario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(70), unique=True)
    descripcion = db.Column(db.String(100))
    categoria = db.Column(db.String(50))
    precio_unit = db.Column(db.Integer)
    cant_disp = db.Column(db.Integer)
    cant_minima = db.Column(db.Integer)
    f_adqu = db.Column(db.Date)
    f_venc = db.Column(db.Date)
    
    def __init__(self, nombre, descripcion, categoria, precio_unit, cant_disp, cant_minima, f_adqu, f_venc):
        self.nombre = nombre
        self.descripcion = descripcion
        self.categoria = categoria
        self.precio_unit = precio_unit
        self.cant_disp = cant_disp
        self.cant_minima = cant_minima
        self.f_adqu = f_adqu
        self.f_venc = f_venc


class Delivery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_orden = db.Column(db.Integer)
    f_entrega = db.Column(db.Date)
    direccion = db.Column(db.String(100))
    est_entrega = db.Column(db.String(50))
    conductor = db.Column(db.String(70))
    patente_transp = db.Column(db.String(6))
    costo_envio = db.Column(db.Integer)
    
    def __init__(self, id_orden, f_entrega, direccion, est_entrega, conductor, patente_transp, costo_envio):
        self.id_orden = id_orden
        self.f_entrega = f_entrega
        self.direccion = direccion
        self.est_entrega = est_entrega
        self.conductor = conductor
        self.patente_transp = patente_transp
        self.costo_envio = costo_envio


class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    run = db.Column(db.Integer, unique=True)
    nombre = db.Column(db.String(50))
    apellido = db.Column(db.String(50))
    direccion = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    correo = db.Column(db.String(100))
    
    carritos = db.relationship('Carrito', back_populates='cliente')
    ordenes = db.relationship('Orden', back_populates='cliente')
    
    def __init__(self, run, nombre, apellido, direccion, telefono, correo):
        self.run = run
        self.nombre = nombre
        self.apellido = apellido
        self.direccion = direccion
        self.telefono = telefono
        self.correo = correo


class Carrito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_producto = db.Column(db.Integer, db.ForeignKey('producto.id'))
    id_cli = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    nombre = db.Column(db.String(70), unique=True)
    descripcion = db.Column(db.String(100))
    costo = db.Column(db.String(100))
    cantidad = db.Column(db.String(100))
    
    producto = db.relationship('Producto', back_populates='carritos')
    cliente = db.relationship('Cliente', back_populates='carritos')
    ordenes = db.relationship('Orden', back_populates='carrito')
    
    def __init__(self, id_producto, id_cli, nombre, descripcion, costo, cantidad):
        self.id_producto = id_producto
        self.id_cli = id_cli
        self.nombre = nombre
        self.descripcion = descripcion
        self.costo = costo
        self.cantidad = cantidad


class Pagos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_orden = db.Column(db.Integer, db.ForeignKey('orden.id'))
    monto = db.Column(db.Integer)
    fecha = db.Column(db.Date)
    met_pago = db.Column(db.Integer)
    estatus = db.Column(db.Boolean, default=True)
    tarjeta = db.Column(db.Integer)
    
    orden = db.relationship('Orden', back_populates='pagos')
    
    def __init__(self, id_orden, monto, fecha, met_pago, estatus, tarjeta):
        self.id_orden = id_orden
        self.monto = monto
        self.fecha = fecha
        self.met_pago = met_pago
        self.estatus = estatus
        self.tarjeta = tarjeta


# Esquemas de Marshmallow
class ProductoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Producto


class PrecioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Precio


class OrdenSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Orden


class InventarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inventario


class DeliverySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Delivery


class ClienteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Cliente


class CarritoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Carrito


class PagosSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pagos


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Esto creará todas las tablas definidas en la base de datos
    app.run(debug=True)
