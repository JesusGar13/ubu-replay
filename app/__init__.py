from flask import Flask, render_template
from flask import request, flash, redirect, url_for 
from app.utils.SingleConexionBD import SingleConexionBD 

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
            
            if db.insert_newUser(username, email, password):
                flash('Usuario registrado correctamente. ¡Bienvenid@! Inicia sesión para continuar')
                return redirect(url_for('login'))
            else:
                flash('Error al registrar el usuario')
                return render_template('register.html')
        
        return render_template('register.html')

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

    return app

