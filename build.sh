#!/bin/bash

# Yüklemeler
pip install -r requirements.txt

# yt-dlp yükle
pip install yt-dlp

# whisper için ffmpeg bağımlılığı
apt-get update && apt-get install -y ffmpeg

# flask başlat
python app.py
