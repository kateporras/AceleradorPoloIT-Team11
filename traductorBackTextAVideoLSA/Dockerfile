#python
FROM python:3.10-slim

#direcctorio de trabajo
WORKDIR /app

#copiar dependencias (para aprovechar cache)
COPY requirements.txt .

#Instalar dependencias del sistema necesarias para spacy pandas, etc

RUN apt-get update && apt-get install -y \
    build-essential \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*


#Instalar las dependencias de python
RUN pip install --no-cache-dir -r requirements.txt

#Descargamos modelo spacy en espaniol
RUN python -m spacy download es_core_news_sm

#Copiar el resto del codigo al contenedor
COPY . .

#Exponer el puerto de FastAPI(por defecto)
EXPOSE 8000

#Comando para ejecutar la app con uvicorn
CMD [ "uvicorn","app.main:app","--host","0.0.0.0","--port","8000" ]

