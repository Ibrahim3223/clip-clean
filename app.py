from flask import Flask, request, jsonify, send_file
import subprocess, os, requests
from utils import transcribe_audio, find_best_segment, edit_video

app = Flask(__name__)

@app.before_request
def debug_request():
    print("RAILWAY DEBUG - Headers:", dict(request.headers))
    print("RAILWAY DEBUG - Raw Body:", request.get_data())

@app.route("/upload-url", methods=["POST"])
def upload_url():
    print("RAILWAY DEBUG - Raw Data:", request.data)

    try:
        data = request.get_json(force=True)
        print("RAILWAY DEBUG - Parsed JSON:", data)
    except Exception as e:
        return jsonify({"error": f"JSON parse error: {str(e)}"}), 400

    if not data or "url" not in data:
        return jsonify({"error": "Missing URL"}), 400

    video_url = data["url"]
    try:
        response = requests.get(video_url)
        if response.status_code != 200:
            return jsonify({"error": "Failed to download video"}), 400

        with open("video.mp4", "wb") as f:
            f.write(response.content)

        transcript = transcribe_audio("video.mp4")
        start, duration = find_best_segment(transcript)
        final_path = edit_video("video.mp4", start, duration)

        return jsonify({"status": "ok", "download_url": request.url_root + "download"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/download", methods=["GET"])
def download():
    return send_file("final.mp4", as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
