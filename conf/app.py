# Importar librerías y módulos
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from form import AgregarForm
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin


# Crear instancia de Flask y configurarla
app = Flask(__name__, template_folder='../templates',
            static_folder='../static')
app.config['SECRET_KEY'] = 's0p0rt3s0p0rt3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost/bd_flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)
csrf = CSRFProtect(app)

# Crear instancia de SQLAlchemy
db = SQLAlchemy(app)

# Definimos el objeto LoginManager
login_manager = LoginManager()

# Definir modelos


class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    rut = db.Column(db.String(12), unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Usuario {self.nombre}>'


# Crear la tabla en la base de datos
@app.before_first_request
def crear_tabla():
    db.create_all()


# Definir rutas
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/')
def index():
    usuarios = Usuario.query.all()
    return render_template('index.html', usuarios=usuarios)


@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    form = AgregarForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        apellido = form.apellido.data
        rut = form.rut.data
        email = form.email.data
        password = generate_password_hash(
            request.form['password'], method='pbkdf2:sha1')
        usuario = Usuario(nombre=nombre, apellido=apellido,
                          rut=rut, email=email, password=password)
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('agregar.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


@login_manager.request_loader
def load_user_from_request(request):
    rut = request.form.get('rut')
    if not rut:
        return None

    user = Usuario.query.filter_by(rut=rut).first()
    if user:
        return user

    return None


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = AgregarForm()
    if form.validate_on_submit():
        # Verificar si el usuario y la contraseña son correctos
        username = form.username.data
        password = form.password.data
        if username == 'usuario' and password == 'contraseña':
            session.permanent = True
            session['username'] = username
            return redirect(url_for('index'))
        else:
            form.username.errors.append('Usuario o contraseña incorrectos')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/usuarios')
def obtener_usuarios():
    # Obtenemos todos los usuarios de la base de datos
    usuarios = Usuario.query.all()
    resultado = [{'id': usuario.id, 'nombre': usuario.nombre, 'apellido': usuario.apellido,
                 'rut': usuario.rut, 'email': usuario.email, 'password': usuario.password} for usuario in usuarios]
    return jsonify(resultado)


@app.route('/login_ajax', methods=['POST'])
def login_ajax():
    username = request.form.get('username')
    password = request.form.get('password')
    if username == 'usuario' and password == 'contraseña':
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Usuario o contraseña incorrectos'})


@app.route('/login/restablecer_contra')
def restablecer_contra():
    return render_template('restablecer_contra.html')


if __name__ == '__main__':
    app.run(debug=True)
