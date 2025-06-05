from flask import Flask, request, send_file, jsonify
import subprocess, os
from utils import download_video, transcribe_audio, find_best_segment, edit_video

app = Flask(__name__)

@app.route("/create-short", methods=["POST"])
def create_short():
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"error": "Missing URL"}), 400

    try:
        video_path = download_video(url)
        transcript = transcribe_audio(video_path)
        start, duration = find_best_segment(transcript)
        final_path = edit_video(video_path, start, duration)
        return jsonify({"status": "ok", "download_url": request.url_root + "download"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/download", methods=["GET"])
def download():
    return send_file("final.mp4", as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
