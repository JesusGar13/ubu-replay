from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from app.utils.autenticacion.userManager import UserManager

class Autenticacion:
    """
    Clase abstracta que define el comportamiento de las clases Login, Registro y Logout
    """
    def __init__(self):
        self.user_manager = UserManager()

    def manejar_solicitud(self):
        if request.method == 'POST':
            return self.ejecutar_autenticacion()
        return self.renderizar_plantilla()

    def ejecutar_autenticacion(self):
        pass

    def renderizar_plantilla(self):
        pass

class Login(Autenticacion):
    """
    Clase que se encarga de la autenticación de un usuario en el sistema
    """
    def __init__(self):
        super().__init__()

    def ejecutar_autenticacion(self):
        username = request.form['username']
        password = request.form['password']
        if self.user_manager.login_user(username, password):
            session['username'] = username
            return redirect(url_for('user_main'))
        return self.renderizar_plantilla()

    def renderizar_plantilla(self):
        return render_template('login.html')


class Registro(Autenticacion):
    """
    Clase que se encarga del registro de un usuario en el sistema
    """
    def __init__(self):
        super().__init__()

    def ejecutar_autenticacion(self):
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if self.user_manager.register_user(username, email, password):
            session['username'] = username
            return redirect(url_for('login'))
        return self.renderizar_plantilla()

    def renderizar_plantilla(self):
        return render_template('register.html')
    

class Logout(Autenticacion):
    """
    Clase que se encarga de cerrar la sesión de un usuario en el sistema
    """
    def __init__(self):
        super().__init__()

    def ejecutar_autenticacion(self):
        self.user_manager.logout_user()
        return redirect(url_for('home'))

    def renderizar_plantilla(self):
        return render_template('logout.html')
