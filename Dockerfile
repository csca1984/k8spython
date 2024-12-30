# Usar una imagen base de Python
FROM python:3.11.4-slim-buster

# Copiar el archivo de requerimientos a la imagen de Docker
COPY requirements.txt /app/requirements.txt

# Instalar las dependencias de Python
RUN pip install -r /app/requirements.txt

# Copiar el script de Python a la imagen de Docker
COPY label_nodes.py /app/label_nodes.py

# Establecer el directorio de trabajo
WORKDIR /app

# Comando por defecto para ejecutar el script
#CMD ["python", "label_nodes.py"]
