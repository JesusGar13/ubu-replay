from flask import Flask, render_template

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def home():
        return render_template('main.html')

    @app.route('/login')
    def login():
        return render_template('login.html')

    @app.route('/register')
    def register():
        return render_template('register.html')

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
