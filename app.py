from flask import Flask, request, send_file, jsonify
import subprocess, os
from utils import transcribe_audio, find_best_segment, edit_video

app = Flask(__name__)

@app.route("/upload", methods=["POST"])
def upload():
    file = None

    # Her ihtimali kontrol et
    if "file" in request.files:
        file = request.files["file"]
    elif "file" in request.form:
        file = request.form["file"]
    elif request.data:
        return jsonify({"error": "Request body exists but no valid file"}), 400
    else:
        return jsonify({"error": "No file part in the request"}), 400

    # Dosya kontrolü
    if not file:
        return jsonify({"error": "No selected file"}), 400

    # Dosyayı kaydet
    filepath = "video.mp4"
    file.save(filepath)

    try:
        transcript = transcribe_audio(filepath)
        start, duration = find_best_segment(transcript)
        final_path = edit_video(filepath, start, duration)
        return jsonify({"status": "ok", "download_url": request.url_root + "download"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/download", methods=["GET"])
def download():
    return send_file("final.mp4", as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
