from flask import Flask, render_template, request, redirect, url_for
from app.utils.UserManager import UserManager
from app.utils.SingleConexionBD import SingleConexionBD

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'

    db = SingleConexionBD()
    db.create_tablas()
    db.delete_all_users()
    user_manager = UserManager()

    @app.route('/')
    def home():
        return render_template('app_main.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if user_manager.login_user(username, password):
                return redirect(url_for('user_main'))
        return render_template('login.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            if user_manager.register_user(username, email, password):
                return redirect(url_for('login'))
        return render_template('register.html')

    @app.route('/logout')
    def logout():
        user_manager.logout_user()
        return redirect(url_for('home'))

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
