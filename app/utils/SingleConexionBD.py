from app.utils.models import Base, User, Session, SitioWeb, Webs, SitioWebSession, WebDenegadas
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

class SingleConexionBD:
    _instance = None

    def __new__(cls, db_url="sqlite:///base_de_datos.db"):
        if cls._instance is None:
            cls._instance = super(SingleConexionBD, cls).__new__(cls)
            cls._instance._initialize(db_url)
        return cls._instance

    def _initialize(self, db_url):
        self.db_url = db_url
        self.engine = create_engine(self.db_url, connect_args={"check_same_thread": False})
        self.Session = sessionmaker(bind=self.engine)

    def delete_all(self):
        try:
            Base.metadata.drop_all(self.engine)
            print("Todas las tablas han sido eliminadas.")
        except Exception as e:
            print(f"Error al eliminar: {e}")

    def create_tablas(self):
        try:
            Base.metadata.create_all(self.engine)
            print("Las tablas se han creado correctamente.")
        except Exception as e:
            print(f"Error al crear tablas: {e}")

    def get_sesion(self):
        try:
            return self.Session()
        except Exception as e:
            print(f"Error al obtener la sesión: {e}")
            return None
    def close_sesion(self, sesion):
        try:
            sesion.close()
        except Exception as e:
            print(f"Error al cerrar la sesión: {e}")

    ############################################################################################################

    def insert_newUser(self, username, email, password):
        sesion = self.get_sesion()
        insercion = None
        try:
            consultaUser = self.select_user(email=email)
            if consultaUser is None: # Si no existe el usuario podemos insertarlo
                newUser = User(username=username, email=email)
                newUser.set_password(password=password)
                sesion.add(newUser)
                sesion.commit()
                insercion = True
            else:
                insercion = False
                
        except Exception as e:
            print(f"Error al insertar un nuevo usuario {e}")
        except SQLAlchemyError as e:
            print(f"Error de SQLAlchemy: {e}")
        finally:
            self.close_sesion(sesion=sesion)
            return insercion             


    def select_user(self, email):
        sesion = self.get_sesion()
        user = None
        try:
            user = sesion.query(User).filter_by(email=email).first()
        except Exception as e:
            print(f"Error al consultar un usuario por su email: {e}")
        except SQLAlchemyError as e:
            print(f"Error de SQLAlchemy: {e}")
        finally:
            self.close_sesion(sesion)
            return user


    def get_user_id(self, username):
        sesion = self.get_sesion()
        user_id = None
        try:
            user = sesion.query(User).filter_by(username=username).first()
            if user:
                user_id = user.id
        except Exception as e:
            print(f"Error al obtener el user_id: {e}")
        finally:
            self.close_sesion(sesion)
        return user_id

    def delete_all_users(self):
        sesion = self.get_sesion()
        try:
            sesion.query(User).delete()
            sesion.commit()
            print("Todos los usuarios han sido eliminados.")
        except Exception as e:
            print(f"Error al eliminar todos los usuarios: {e}")
        except SQLAlchemyError as e:
            print(f"Error de SQLAlchemy: {e}")
        finally:
            self.close_sesion(sesion)
        
    def verify_user(self, username, password):
        sesion = self.get_sesion()
        user = None
        try:
            user = sesion.query(User).filter_by(username=username).first()
            if user and user.check_password(password):
                return user
        except Exception as e:
            print(f"Error al verificar el usuario: {e}")
        finally:
            self.close_sesion(sesion)
        return None 


    def insert_newSitioWeb(self, main_url):
        sesion = self.get_sesion()
        try:
            new_sitioWeb = SitioWeb(main_url=main_url)
            sesion.add(new_sitioWeb)
            sesion.commit()
        except Exception as e:
            print(f"Error al insertar un nuevo Sitio Web: {e}")
        except SQLAlchemyError as e:
            print(f"Error de SQLAlchemy: {e}")
        finally:
            self.close_sesion(sesion)

    def select_SitioWeb(self, main_url):
        sesion = self.get_sesion()
        sitio_web = None
        try:
            sitio_web = sesion.query(SitioWeb).filter_by(main_url=main_url).first()
        except Exception as e:
            print(f"Error al consultar un sitio web por su main_url: {e}")
        except SQLAlchemyError as e:
            print(f"Error de SQLAlchemy: {e}")
        finally:
            self.close_sesion(sesion)
            return sitio_web


    def insert_newsWebs(self, sitio_web_id, urls_web:list):
        sesion = self.get_sesion()
        try:
            for url in urls_web:
                new_web = Webs(sitio_web_id=sitio_web_id, url=url)
                sesion.add(new_web)
            sesion.commit()
        except Exception as e:
            print(f"Error al insertar una nueva web: {e}")
        except SQLAlchemyError as e:
            print(f"Error de SQLAlchemy: {e}")
        finally:
            self.close_sesion(sesion)


    def insert_newSession(self, user_id, time_start, time_end, main_url, urls_web):
        sesion = self.get_sesion()
        try:
            # Comprobamos si existe el sitio web
            sitio_web = self.select_SitioWeb(main_url=main_url)
            if sitio_web is None:
                # Inserta el sitio web si no existe
                self.insert_newSitioWeb(main_url=main_url)
                sitio_web = self.select_SitioWeb(main_url=main_url)

            sitio_Web_id = sitio_web.id

            # Insertamos las webs asociadas al sitio web
            self.insert_newsWebs(sitio_web_id=sitio_Web_id, urls_web=urls_web)

            # Creamos la nueva sesión
            new_session = Session(
                user_id=user_id,            
                time_start=datetime.strptime(time_start, '%Y-%m-%dT%H:%M:%S.%fZ'),  # Convertimos a objeto datetime
                time_end=datetime.strptime(time_end, '%Y-%m-%dT%H:%M:%S.%fZ')       # Convertimos a objeto datetime
            )
            sesion.add(new_session)
            sesion.commit()  # Guardamos la sesión para obtener su ID

            # Relacionamos la sesión con el sitio web
            new_session_id = new_session.id
            new_sitioWebSession = SitioWebSession(
                session_id=new_session_id,
                sitio_web_id=sitio_Web_id
            )
            sesion.add(new_sitioWebSession)
            sesion.commit()

        except Exception as e:
            print(f"Error al insertar una nueva sesión: {e}")
            sesion.rollback()  # Revertir cualquier cambio en caso de error
        except SQLAlchemyError as e:
            print(f"Error de SQLAlchemy: {e}")
            sesion.rollback()
        finally:
            self.close_sesion(sesion)

            
    def selectAll_countSession_from_SitioWeb(self, user_id):
        sesion = self.get_sesion()
        sitioWeb_countSession = {}

        try:
            # Definimos explícitamente la tabla base y las uniones necesarias
            sessionSitioWeb = (
                sesion.query(Session, SitioWeb)
                .join(SitioWebSession, Session.id == SitioWebSession.session_id)
                .join(SitioWeb, SitioWebSession.sitio_web_id == SitioWeb.id)
                .filter(Session.user_id == user_id)
                .all()
            )

            # Contamos las sesiones por cada sitio web
            for session, sitioWeb in sessionSitioWeb:
                if sitioWeb.main_url in sitioWeb_countSession:
                    sitioWeb_countSession[sitioWeb.main_url] += 1
                else:
                    sitioWeb_countSession[sitioWeb.main_url] = 1

        except Exception as e:
            print(f"Error al contar las sesiones por sitio web: {e}")
        finally:
            self.close_sesion(sesion)
            return sitioWeb_countSession


    def selectAll_session_from_sitioWeb(self, user_id, sitioWeb_id):
        sesion = self.get_sesion()
        sessions = None

        try:
            # Consulta las sesiones del usuario para el sitio web específico
            sessions = (
                sesion.query(Session)
                .join(SitioWebSession, Session.id == SitioWebSession.session_id)
                .filter(
                    Session.user_id == user_id,
                    SitioWebSession.sitio_web_id == sitioWeb_id
                )
                .all()
            )
        except Exception as e:
            print(f"Error al consultar las sesiones por sitio web: {e}")
        finally:
            self.close_sesion(sesion)
        return sessions


    def insert_sitioWeb_denegado(self, sitioWeb_id, user_id):
        sesion = self.get_sesion()
        try:
            existe_sitioWeb = sesion.query(SitioWeb).filter_by(id=sitioWeb_id).first()
            if existe_sitioWeb is not None:
                new_webDenegada = WebDenegadas(sitio_web_id=sitioWeb_id, user_id=user_id)
                sesion.add(new_webDenegada)
                sesion.commit()
        except Exception as e:
            print(f"Error al insertar un sitio web denegado: {e}")
            sesion.rollback()
        except SQLAlchemyError as e:
            print(f"Error de SQLAlchemy: {e}")
        finally:
            self.close_sesion(sesion) 


    def get_denied_sites_by_user(self, user_id):
        sesion = self.get_sesion()
        try:
            denied_sites = sesion.query(WebDenegadas).options(joinedload(WebDenegadas.sitio_web)).filter_by(user_id=user_id).all()
            print(denied_sites)
            return denied_sites
        except Exception as e:
            print(f"Error al obtener sitios web denegados por usuario: {e}")
            return []
        finally:
            self.close_sesion(sesion)

    def remove_sitioWeb_denegado(self, site_id):
        sesion = self.get_sesion()
        try:
            sitio_web = sesion.query(WebDenegadas).filter_by(id=site_id).first()
            if sitio_web:
                sesion.delete(sitio_web)
                sesion.commit()
        except Exception as e:
            print(f"Error al eliminar sitio denegado: {e}")
            sesion.rollback()
        finally:
            self.close_sesion(sesion)

    
    def get_all_denied_sites(self):
        sesion = self.get_sesion()
        denied_sites = None
        try:
            denied_sites = sesion.query(WebDenegadas).all()
        except Exception as e:
            print(f"Error al consultar los sitios web denegados: {e}")
        finally:
            self.close_sesion(sesion)
            return denied_sites              
    

    def selectBool_sitioWeb_denegado(self, sitioWeb_id):
        sesion = self.get_sesion()
        denegado = False
        try:
            denegado = sesion.query(WebDenegadas).filter_by(sitio_web_id=sitioWeb_id).first() is not None
        except Exception as e:
            print(f"Error al consultar si un sitio web está denegado: {e}")
        finally:
            self.close_sesion(sesion)
            return denegado 

    def remove_sitioWeb_denegado(self, site_id):
        sesion = self.get_sesion()
        try:
            sitio_web = sesion.query(WebDenegadas).filter_by(sitio_web_id=site_id).first()
            if sitio_web:
                sesion.delete(sitio_web)
                sesion.commit()
        except Exception as e:
            print(f"Error al eliminar sitio denegado: {e}")
        finally:
            self.close_sesion(sesion)

        

