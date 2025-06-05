FROM python:3.10-slim

# Sistemi güncelle ve ffmpeg gibi bağımlılıkları yükle
RUN apt-get update && apt-get install -y ffmpeg git

# Python bağımlılıklarını yükle
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyala
COPY . .

# Flask sunucusunu başlat
CMD ["python", "app.py"]
