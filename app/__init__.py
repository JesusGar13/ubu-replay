# app/__init__.py
from flask import Flask

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def home():
        return "¡Bienvenido a mi aplicación Flask!"

    return app
