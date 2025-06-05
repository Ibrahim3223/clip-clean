FROM python:3.10-slim

WORKDIR /app

# ffmpeg yükle
RUN apt-get update && apt-get install -y ffmpeg git && apt-get clean

# bağımlılıkları yükle
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# uygulama dosyaları
COPY . .

CMD ["python", "app.py"]
