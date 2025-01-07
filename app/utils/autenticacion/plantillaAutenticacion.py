from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from app.utils.autenticacion.userManager import UserManager

# Método plantilla para Login y Registro
class Autenticacion:
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
    def __init__(self):
        super().__init__()

    def ejecutar_autenticacion(self):
        username = request.form['username']
        password = request.form['password']
        if self.user_manager.login_user(username, password):
            session['username'] = username
            return redirect(url_for('user_main'))  # Redirige a 'user_main' si login es exitoso
        return self.renderizar_plantilla()

    def renderizar_plantilla(self):
        return render_template('login.html')


class Registro(Autenticacion):
    def __init__(self):
        super().__init__()

    def ejecutar_autenticacion(self):
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if self.user_manager.register_user(username, email, password):
            session['username'] = username
            return redirect(url_for('login'))  # Redirige al login después del registro
        return self.renderizar_plantilla()

    def renderizar_plantilla(self):
        return render_template('register.html')


class Logout(Autenticacion):
    def __init__(self):
        super().__init__()

    def ejecutar_autenticacion(self):
        # Lógica para cerrar sesión
        self.user_manager.logout_user()
        return redirect(url_for('home'))  # Redirige a la página de inicio después de cerrar sesión

    def renderizar_plantilla(self):
        # Este método no es necesario si solo rediriges, pero si quieres hacer algo en el logout, puedes usarlo aquí
        return render_template('logout.html')
