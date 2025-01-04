from flask import Flask, render_template
from flask import request, flash, redirect, url_for 
from app.utils.SingleConexionBD import SingleConexionBD 
import re



def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'  

    db = SingleConexionBD()
    db.create_tablas()
    db.delete_all_users()

    @app.route('/')
    def home():
        return render_template('app_main.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            
            user = db.verify_user(username, password)
            if user:
                return redirect(url_for('user_main'))
            else:
                flash('Usuario o contraseña incorrectos')
                return render_template('login.html')
        return render_template('login.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']

            if not validate_password(password):
                flash('La contraseña debe tener entre 6 y 12 caracteres, al menos una letra mayúscula, una minúscula y un número')
                return render_template('register.html')

            if not validate_email(email):
                flash('Email incorrecto. Debe ser de la forma: ----@----.es o ----@----.com')
                return render_template('register.html')    
            
            if db.insert_newUser(username, email, password):
                flash('Usuario registrado correctamente. ¡Bienvenid@! Inicia sesión para continuar')
                return redirect(url_for('login'))
            else:
                flash('Error al registrar el usuario')
                return render_template('register.html')
        
        return render_template('register.html')


    def validate_email(email):
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(es|com)$'
            return re.match(pattern, email) is not None


    def validate_password(password):
        if len(password) < 6 or len(password) > 12:
            return False
        if not re.search("[a-z]", password):
            return False
        if not re.search("[A-Z]", password):
            return False
        if not re.search("[0-9]", password):
            return False
        return True

    @app.route('/user_main')
    def user_main():
        return render_template('user_main.html')    


    @app.route('/tracking')
    def tracking():
        return render_template('tracking.html')

    @app.route('/tracking/track_session')
    def track_session():
        return render_template('track_session.html')

    @app.route('/denied_web')
    def denied_web():
        return render_template('denied_web.html')

    @app.route('/logout', methods=['GET', 'POST'])
    def logout():
        if request.method == 'POST':
            # Aquí puedes agregar la lógica para cerrar la sesión del usuario
            flash('Sesión cerrada correctamente')
            return redirect(url_for('home'))
        return render_template('logout.html')

    return app

