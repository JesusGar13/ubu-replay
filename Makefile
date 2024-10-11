IMAGE_NAME = app_image
CONTAINER_NAME = app_container
PORT = 5000

build:
	@echo "Construyendo la imagen Docker..."
	docker build --no-cache -t $(IMAGE_NAME) .

# Ejecución de pruebas (asumiendo que tienes tests configurados, ajustar según sea necesario)
test:
	@echo "Ejecutando pruebas..."
	docker run --rm $(IMAGE_NAME) pytest

clean:
	@echo "Limpiando el entorno Docker..."
	-docker stop $(CONTAINER_NAME)
	-docker rm $(CONTAINER_NAME)
	-docker rmi $(IMAGE_NAME)

run:
	@echo "Ejecutando la aplicación..."
	docker run --name $(CONTAINER_NAME) -p $(PORT):$(PORT) $(IMAGE_NAME)

# Ayuda
help:
	@echo "Comandos disponibles:"
	@echo "  make build    - Construye la imagen Docker"
	@echo "  make test     - Ejecuta las pruebas dentro del contenedor Docker"
	@echo "  make clean    - Elimina contenedor e imagen de Docker"
	@echo "  make run      - Ejecuta la aplicación en modo desarrollo"
