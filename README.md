# UBU Replay 📀

## Descripción del Proyecto 📋

**UBU Replay** es una aplicación diseñada para analizar cómo los usuarios interactúan con diferentes sitios web utilizando la técnica conocida como **Session Replay**. Esta técnica permite capturar y reproducir las interacciones de los usuarios, lo que proporciona una visión detallada de su comportamiento en un sitio web.

Este proyecto implementa una versión minimalista de una solución de Session Replay. La aplicación consta de dos componentes principales:

1. **Extensión de Chrome**:  
   Es el punto de entrada de la aplicación. Una vez instalada en el navegador, la extensión captura las interacciones del usuario con los sitios web. Estas interacciones se agrupan en sesiones, que posteriormente se envían para su almacenamiento y análisis.

2. **Aplicación Web**:  
   La aplicación web es responsable de recibir los datos enviados por la extensión, almacenarlos de forma organizada y ofrecer una interfaz para visualizar las sesiones capturadas.

## Flujo de Funcionamiento 🔀

1. El usuario instala la extensión de Chrome en su navegador.
2. La extensión captura las interacciones realizadas en los sitios web, como clics, desplazamientos y formularios.
3. Estas interacciones se agrupan en sesiones y se envían a la aplicación web.
4. La aplicación web almacena las sesiones y permite su visualización a través de una interfaz gráfica.

## Instalación y Configuración 💾

### Extensión de Chrome
1. Descarga o clona este repositorio.
2. Ve a `chrome://extensions/` en tu navegador.
3. Activa el "Modo de desarrollador".
4. Haz clic en "Cargar descomprimida" y selecciona la carpeta de la extensión.

### Aplicación Web
1. Asegúrate de tener docker instalado.
2. Maneja la creacion del container de docker con ***make***, mediante los comandos:
- Limpia el entorno y el conetenedor de docker:
   ```bash
   make clean 
- Crea el contenedor de docker y lo deja listo para la ejecucion de la app:
    ```bash
   make run
- Ejecuta la app mediante el contenedor docker:
    ```bash
   make run 


## Tecnologías Utilizadas 🛠️

- **Frontend**: Extensión de Chrome (JavaScript, HTML, CSS).
- **Backend**: Aplicación web desarrollada con Flask.
- **Base de datos**: SQLite para almacenar las sesiones capturadas.
- **ORM**: SQLAlchemy para gestionar la base de datos.



