FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivo de dependencias
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el archivo de la aplicación
COPY web.py .

# Exponer el puerto de Gradio
EXPOSE 7860

# Por defecto ejecutar la versión web
CMD ["python", "web.py"]
