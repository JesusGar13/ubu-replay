from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from app.utils.SingleConexionBD import SingleConexionBD
from app.utils.autenticacion.plantillaAutenticacion import Login, Registro, Logout
from app.utils.models import Session
from flask import flash


def create_app():

    app = Flask(__name__)
    app.secret_key = 'your_secret_key'

    db = SingleConexionBD()
    db.create_tablas()

    @app.route('/')
    def home():
        return render_template('app_main.html')


    @app.route('/login', methods=['GET', 'POST'])
    def login():
        manejador = Login()
        return manejador.manejar_solicitud()


    @app.route('/register', methods=['GET', 'POST'])
    def register():
        manejador = Registro()
        return manejador.manejar_solicitud()   


    @app.route('/logout', methods=['GET', 'POST'])
    def logout():
        manejador = Logout()
        return manejador.manejar_solicitud()

    @app.route('/user_main')
    def user_main():
        if 'logged_in' not in session:
            return redirect(url_for('login')) 

        user_id = session.get('user_id')
        siteCounts = db.selectAll_countSession_from_SitioWeb(user_id)
        webs = []
        counts = []

        for web, count in siteCounts.items():
            webs.append(web)
            counts.append(count)
        webs_counts = zip(webs, counts)

        tracking_enabled = session.get('tracking_enabled', True)
            
        return render_template('user_main.html', webs_counts=webs_counts, user_id=user_id)   


    @app.route('/track_session')
    def track_session():
        user_id = session.get('user_id')

        sesiones = db.selectAll_session_from_user(user_id)

        if not sesiones:
            flash("No hay sesiones disponibles para este usuario.", "info")
            return render_template('track_session.html', sessions=[])

        session_list = []
        for sesion in sesiones:
            session_list.append({
                "id": sesion[0].id,
                "sitio_web": sesion[1].main_url if sesion[1].main_url is not None else "Desconocido",
                "time_start": sesion[0].time_start.strftime("%Y-%m-%d %H:%M:%S"),
                "time_end": sesion[0].time_end.strftime("%Y-%m-%d %H:%M:%S"),
            })

        return render_template('track_session.html', sessions=session_list)


    @app.route('/api/track', methods=['POST'])
    def track_interactions():
        data = request.json
        if not session.get('tracking_enabled', True):
            return jsonify({'message': 'Tracking está desactivado. No se registrarán interacciones.'}), 200

        webDenegadas = db.get_denied_sites_by_user(user_id=session.get('user_id'))
        lista_denegadas = [site.sitio_web.main_url for site in webDenegadas]

        try:
            user_id = session.get('user_id')
            time_start = data.get("timeStart")
            time_end = data.get("timeEnd")
            main_url = data.get('recorrido')[0]
            urls_web = data.get('recorrido')[1:] 

            if main_url in lista_denegadas:
                return jsonify({'error': 'La página web principal está denegada'}), 400

            db.insert_newSession(user_id=user_id,
                                time_start=time_start,
                                time_end=time_end,
                                main_url=main_url,
                                urls_web=urls_web)
            
            return jsonify({'message': 'Interacciones registradas correctamente'}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 400


    @app.route('/denied_web', methods=['GET', 'POST'])
    def denied_web():
        user_id = session.get('user_id')

        if request.method == 'POST':
            data = request.json
            url = data.get('url')
            sitio_web = db.select_SitioWeb(main_url=url)
            if not sitio_web:
                db.insert_newSitioWeb(main_url=url)
                sitio_web = db.select_SitioWeb(main_url=url)
            existing_denied_site = db.selectBool_sitioWeb_denegado(sitioWeb_id=sitio_web.id)
            if not existing_denied_site:
                db.insert_sitioWeb_denegado(sitioWeb_id=sitio_web.id, user_id=user_id)
                return jsonify({'message': 'Pagina web denegada correctamente', 'site_id': sitio_web.id}), 201
            else:
                return jsonify({'error': 'La págia web ya ha sido denegada'}), 400

        denied_sites = db.get_denied_sites_by_user(user_id=user_id)
        return render_template('denied_web.html', denied_sites=denied_sites)


    @app.route('/denied_web/<int:site_id>', methods=['DELETE'])
    def remove_denied_web(site_id):
        db.remove_sitioWeb_denegado(site_id=site_id)
        return jsonify({'message': 'Pagina web eliminada correctamente'}), 200    
        
    
    @app.route('/session/<int:session_id>')
    def view_session(session_id):

        session_data = db.get_sesion().query(Session).filter_by(id=session_id).first()

        if not session_data:
            flash('Sesión no encontrada')
            return redirect(url_for('track_session'))
        interactions = db.get_interactions_by_session(session_id)

        session_info = {
            "sitio_web": session_data.sitio_web.main_url if session_data.sitio_web else "Desconocido",
            "time_start": session_data.time_start.strftime("%Y-%m-%d %H:%M:%S"),
            "time_end": session_data.time_end.strftime("%Y-%m-%d %H:%M:%S"),
        }
        return render_template('view_session.html', interactions=interactions)


    @app.route('/toggle_tracking', methods=['POST'])
    def toggle_tracking():
        try:

            data = request.json
            enable = data.get('enable')

            session['tracking_enabled'] = enable

            message = "Tracking activado" if enable else "Tracking desactivado"
            return jsonify({'message': message}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400
        

    return app