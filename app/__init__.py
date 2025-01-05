from flask import Flask, render_template, request, redirect, url_for, jsonify
from app.utils.userManager import UserManager
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
        db = SingleConexionBD()
        user_id = 1  # Cambiar según el usuario autenticado

        # Obtener el conteo de sesiones por sitio web
        tracked_sites = []
        site_sessions = db.selectAll_countSession_from_SitioWeb(user_id)

        # Formatear los datos para el template
        for site_url, num_sessions in site_sessions.items():
            sitio_web = db.select_SitioWeb(site_url)  # Obtener el objeto SitioWeb
            tracked_sites.append({
                "id": sitio_web.id,
                "main_url": site_url,
                "num_sessions": num_sessions
            })

        return render_template('tracking.html', tracked_sites=tracked_sites)

    @app.route('/tracking/track_session')
    def track_session():
        # Crear una instancia de la conexión a la base de datos
        db = SingleConexionBD()
        user_id = 1  # Puedes usar el ID del usuario autenticado en lugar de este valor fijo.
        global redo_history
        
        # Obtener las sesiones del usuario
        sesiones = db.selectAll_session_from_sitioWeb(user_id, sitioWeb_id=None)

        # Formatear los datos para enviarlos al template
        session_list = []
        for sesion in sesiones:
            session_list.append({
                "id": sesion.id,
                "sitio_web": sesion.sitio_web.main_url if sesion.sitio_web else "Desconocido",
                "sitio_web_id": sesion.sitio_web.id if sesion.sitio_web else None,
                "time_start": sesion.time_start.strftime("%Y-%m-%d %H:%M:%S"),
                "time_end": sesion.time_end.strftime("%Y-%m-%d %H:%M:%S"),
            })

        # Renderizar el template con las sesiones
        return render_template('track_session.html', sessions=session_list)
    
    @app.route('/api/track', methods=['POST'])
    def track_interactions():
        data = request.json
        db = SingleConexionBD()
        
        # Aquí debes procesar y guardar las interacciones en la base de datos
        try:
            user_id = data['user_id']
            sitio_web = data['site_url']
            interactions = data['interactions']  # Lista de interacciones
            
            # Inserta las interacciones en la base de datos
            for interaction in interactions:
                # Guardar interacción (ejemplo)
                db.insert_interaction(user_id, sitio_web, interaction)
            
            return jsonify({'message': 'Interacciones registradas correctamente'}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 400


    @app.route('/denied_web', methods=['GET', 'POST'])
    def denied_web():
        db = SingleConexionBD()

        if request.method == 'POST':
            site_url = request.json.get('url')
            if site_url:
                # Inserta la URL en la base de datos
                db.insert_sitioWeb_denegado(site_url)
                return jsonify({'message': 'URL denegada agregada correctamente'}), 201
            return jsonify({'error': 'URL no válida'}), 400

        # Obtener la lista de URLs denegadas desde la base de datos
        denied_sites = db.get_all_denied_sites()
        denied_sites_list = [{'id': site.id, 'main_url': site.main_url} for site in denied_sites]

        return render_template('denied_web.html', denied_sites=denied_sites_list)

    
    @app.route('/session/<int:session_id>')
    def view_session(session_id):
        db = SingleConexionBD()
        interactions = db.get_interactions_by_session(session_id)
        
        return render_template('view_session.html', interactions=interactions)


    @app.route('/api', methods=['POST']) # Esto no funciona todavia 
    def api():
        data = request.get_json()
        
        tabId = data.get('tabId')
        recorrido = data.get('recorrido')
        timeStart = data.get('timeStart')
        timeEnd = data.get('timeEnd')

        db = SingleConexionBD()
        db.insert_newSession(1, time_start=timeStart, time_end=timeEnd, main_url=recorrido[0], urls_web=recorrido[1:])

        return jsonify({'status': 'success', 'message': 'Data received successfully'}),200


    return app
