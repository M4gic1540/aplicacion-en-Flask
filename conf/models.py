from flask_sqlalchemy import SQLAlchemy
from flask import Flask


app = Flask(__name__)

# Configurar la conexión a la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost/bd_flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 's0p0rt3s0p0rt3'

db = SQLAlchemy(app)


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    rut = db.Column(db.String(12), unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Usuario {self.nombre}>'


# Crear la tabla en la base de datos
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        usuario1 = Usuario(nombre='Juan', apellido='gonzalez',
                           rut='19.277.589-2', email='juan@example.com', password='123456')
        db.session.add(usuario1)
        db.session.commit()
