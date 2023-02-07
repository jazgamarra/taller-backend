from flask import Flask, render_template 
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

# Crear el servidor 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' 
app.config['SECRET_KEY'] = 'jamin'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
# Si no esta logeado, le referencia a esta ruta
login_manager.login_view = 'login' 


# ----------------------------------------------------------------------
# MODELOS
# ----------------------------------------------------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

class ToDo (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, description, user_id):
        self.title = title
        self.description = description
        self.user_id = user_id

# ----------------------------------------------------------------------
# FORMULARIOS
# ----------------------------------------------------------------------
class RegisterForm(FlaskForm): 
    username = StringField('Username')
    email = StringField('Email')
    password = PasswordField('Password')
    submit = SubmitField('Sign Up')

class LoginForm (FlaskForm):
    email = EmailField('Email')
    password = PasswordField('Password')
    submit = SubmitField('Sign In')

# ----------------------------------------------------------------------
# RUTAS
# ----------------------------------------------------------------------

# Crear la sesion del usuario 
# Hace un query a la base de datos y busca el usuario con el email que se ingreso 
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Crear tablas en sql alchemy 
with app.app_context():
    db.create_all()

@app.route ('/', methods=['GET', 'POST'])
def register ():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(name=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return f'SE CREO EL USUARIO {user}'
    return render_template('register.html', form=form)

@app.route ('/login', methods=['GET', 'POST'])
def login ():
    form = LoginForm()
    return render_template('login.html', form=form)

if __name__ == '__main__':
    app.run(debug=True, port=8080)