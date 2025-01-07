import re
from flask import flash, session, redirect, url_for
from app.utils.SingleConexionBD import SingleConexionBD

class UserManager:
    """
    Clase que se encarga de gestionar las operaciones de autenticación de los usuarios
    """
    def __init__(self):
        self.db = SingleConexionBD()

    def login_user(self, username, password):
        user = self.db.verify_user(username, password)
        if user:
            session['logged_in'] = True
            session['user_id'] = user.id  
            flash('Inicio de sesión exitoso')
            return True
        else:
            flash('Usuario o contraseña incorrectos')
            return False

    def register_user(self, username, email, password):
        if not self.validate_password(password):
            flash('La contraseña debe tener entre 6 y 12 caracteres, al menos una letra mayúscula, una minúscula y un número')
            return False

        if not self.validate_email(email):
            flash('Email incorrecto. Debe ser de la forma: ----@----.es o ----@----.com')
            return False

        if self.db.insert_newUser(username, email, password):
            flash('Usuario registrado correctamente. ¡Bienvenid@! Inicia sesión para continuar')
            return True
        else:
            flash('Error al registrar el usuario')
            return False

    def logout_user(self):
        session.pop('logged_in', None)
        session.pop('username', None)
        flash('Sesión cerrada correctamente')


    @staticmethod
    def validate_email(email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(es|com)$'
        return re.match(pattern, email) is not None

    @staticmethod
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
