FROM python:3.11.4-slim

WORKDIR /app

COPY requirements.txt ./

# Crea el entorno virtual en la carpeta "virtual-env" y activa el entorno virtual
RUN python -m venv ./virtual-env/myenv && \
    . ./virtual-env/myenv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

CMD ["bash", "-c", ". ./virtual-env/myenv/bin/activate && python run.py"]


