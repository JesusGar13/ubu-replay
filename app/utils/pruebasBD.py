from SingleConexionBD import SingleConexionBD  

# 1. Verificar que la instancia de SingleConexion es única
def test_singleton_instance():
    print("\nProbando Singleton...")
    
    # Crear dos instancias de SingleConexion
    instancia_1 = SingleConexionBD()
    instancia_2 = SingleConexionBD()
    
    # Verificar que ambas instancias son la misma
    if instancia_1 is instancia_2:
        print("El patrón Singleton funciona correctamente.")
    else:
        print("¡Las instancias no son iguales! El patrón Singleton no está funcionando correctamente.")


# 2. Verificar que la inicialización de la base de datos y la sesión funciona
def test_initialize_and_session():
    print("\nProbando inicialización y obtención de sesión...")
    
    # Crear una instancia de SingleConexion
    db = SingleConexionBD()
    db.delete_all()
    db.create_tablas()
    
    # Verificar que la sesión se pueda obtener
    sesion = db.get_sesion()
    if sesion is not None:
        print("Se obtuvo una sesión correctamente.")
        db.close_sesion(sesion)
    else:
        print("No se pudo obtener una sesión.")


# 3. Probar insercion de una usuario
def test_insert_newUser():
    db = SingleConexionBD()

    username = "usuario1"
    email = "emailPrueba1@gmail.com"
    password = "1234"
    insercion = db.insert_newUser(username=username, email=email, password=password)

    if insercion:
        print(f"Se ha añadido el usuario1.")
    else:
        print(f"Ya fue añadido, hay un usuario con ese email.")


# 4. probar la consulta de un usuario
def test_select_user():
    db = SingleConexionBD()

    email = "emailPrueba1@gmail.com"
    usuario = db.select_user(email)
    print(f"Se ha hecho una colsulta de usuario con email: {email}:")
    print(f"Consulta: {usuario.id} - {usuario.username} - {email}")

# 5. porbar la insercion de una session a un sitioWeb y sus webs
def test_insert_newSession():
    db = SingleConexionBD()

    user_id = 1
    time_start = "2021-10-10 8:00:00"
    time_end = "2021-10-10 9:00:00"
    main_url = "https://drive.google.com/drive/u/0/home"
    urls = ["https://drive.google.com/drive/u/0/home", "https://drive.google.com/drive/u/0/shared-with-me", "https://drive.google.com/drive/u/0/recent"]

    db.insert_newSession(user_id, time_start, time_end, main_url, urls)
    print(f"Se ha añadido una session a un usuario con id: {user_id}.")

# 6. probar la consulta en numero de sesiones de un sitioWeb
def test_selectAll_countSession_from_SitioWeb():
    db = SingleConexionBD()

    user_id = 1
    sitioWeb_countSession = db.selectAll_countSession_from_SitioWeb(user_id)
    print(f"Se ha hecho una colsulta de las sesiones de un usuario con id: {user_id}:")
    print(f"Consulta: ")
    for k,v in sitioWeb_countSession.items():
        print(f"{k} - {v}")

# 7. probar insercion de varias sesiones a un sitioWeb y sus webs
def test_insert_newSessions():
    db = SingleConexionBD()

    user_id = 1
    times_start = ["2021-10-10 10:00:00", "2021-10-10 11:00:00", "2021-10-10 12:00:00"]
    times_end = ["2021-10-10 10:30:00", "2021-10-10 11:30:00", "2021-10-10 12:30:00"]
    main_url = "https://drive.google.com/drive/u/0/home"
    urls =[["https://drive.google.com/drive/u/0/home1", "https://drive.google.com/drive/u/0/shared-with-me1", "https://drive.google.com/drive/u/0/recent1"],
            ["https://drive.google.com/drive/u/0/home2", "https://drive.google.com/drive/u/0/shared-with-me2", "https://drive.google.com/drive/u/0/recent2"],
            ["https://drive.google.com/drive/u/0/home3", "https://drive.google.com/drive/u/0/shared-with-me3", "https://drive.google.com/drive/u/0/recent3"]]

    for i in range(3):
        db.insert_newSession(user_id, times_start[i], times_end[i], main_url, urls[i])
        print(f"Se ha añadido una session a un usuario con id: {user_id}.")

# 7. probar insercion de varias sesiones a un nuevo sitioWeb y sus web
def test_insert_newSessionsOtherSitioWeb():
    db = SingleConexionBD()

    user_id = 1
    times_start = ["2021-10-10 10:00:00", "2021-10-10 11:00:00", "2021-10-10 12:00:00"]
    times_end = ["2021-10-10 10:30:00", "2021-10-10 11:30:00", "2021-10-10 12:30:00"]
    main_url = "https://ubuVirtual.com"
    urls = [["https://ubuVirtual.com/home1", "https://ubuVirtual.com/shared-with-me1", "https://ubuVirtual.com/recent1"],
            ["https://ubuVirtual.com/home2", "https://ubuVirtual.com/shared-with-me2", "https://ubuVirtual.com/recent2"],
            ["https://ubuVirtual.com/home3", "https://ubuVirtual.com/shared-with-me3", "https://ubuVirtual.com/recent3"]]

    for i in range(3):
        db.insert_newSession(user_id, times_start[i], times_end[i], main_url, urls[i])
        print(f"Se ha añadido una session a un usuario con id: {user_id}.")

# 8. probar la consulta de las sesiones de un sitio web de un usuario
def test_selectAll_session_from_sitioWeb():
    db = SingleConexionBD()

    user_id = 1
    sitoWeb_id = 1
    sitioWeb_sessions = db.selectAll_session_from_sitioWeb(user_id, sitoWeb_id)
    print(f"Se ha hecho una colsulta de las sesiones de un usuario con id: {user_id} a un sitio web id: {sitoWeb_id}:")
    print(f"Consulta: num sesiones: {len(sitioWeb_sessions)}")
    for sitoWeb_session in sitioWeb_sessions:
        print(f"{sitoWeb_session.id} - {sitoWeb_session.time_start} - {sitoWeb_session.time_end}")

# 9. insertar un sitioWeb denegado
def test_insert_sitioWeb_denegado():
    db = SingleConexionBD()

    sitioWeb_id = 2
    db.insert_sitioWeb_denegado(sitioWeb_id=sitioWeb_id)
    print(f"El sitio web con id {sitioWeb_id} ha sido denegada")

# 10. probamos si un sitioWeb esta denegada
def test_selectBool_sitioWeb_denegado():
    db = SingleConexionBD()

    sitioWeb_id = 2
    denegado = db.selectBool_sitioWeb_denegado(sitioWeb_id=sitioWeb_id)

    if denegado:
        print(f"El sitio web con id {sitioWeb_id} esta denegado")
    else:
        print(f"El sitio web con id {sitioWeb_id} NO esta denegado")


# Ejecutar todas las pruebas
if __name__ == "__main__":
    print("Ejecutando las pruebas...\n")
    test_singleton_instance()
    print("-----------------------------------------------------------------------")
    test_initialize_and_session()
    print("-----------------------------------------------------------------------")
    test_insert_newUser()
    print("-----------------------------------------------------------------------")
    test_select_user()
    print("-----------------------------------------------------------------------")
    test_insert_newSession()
    print("-----------------------------------------------------------------------")
    test_selectAll_countSession_from_SitioWeb()
    print("-----------------------------------------------------------------------")
    test_insert_newSessions()
    print("-----------------------------------------------------------------------")    
    test_selectAll_countSession_from_SitioWeb()
    print("-----------------------------------------------------------------------")
    test_insert_newSessionsOtherSitioWeb()
    print("-----------------------------------------------------------------------")
    test_selectAll_countSession_from_SitioWeb()
    print("-----------------------------------------------------------------------")
    test_selectAll_session_from_sitioWeb()
    print("-----------------------------------------------------------------------")
    test_insert_sitioWeb_denegado()
    print("-----------------------------------------------------------------------")
    test_selectBool_sitioWeb_denegado()
    print("\nLas pruebas se han ejecutado.")
