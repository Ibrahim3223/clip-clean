import subprocess, os
import whisper
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def download_video(url):
    output = "video.mp4"
    subprocess.run(["yt-dlp", "-f", "mp4", "-o", output, url], check=True)
    return output

def transcribe_audio(video_path):
    model = whisper.load_model("base")
    result = model.transcribe(video_path)
    return result["text"]

def find_best_segment(transcript):
    prompt = f"Analyze this transcript and return the start second of the most interesting 20-second segment:\n\n{transcript}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    content = response["choices"][0]["message"]["content"]
    return 0, 20  # Simplified static return for now

def edit_video(video_path, start, duration):
    final_path = "final.mp4"
    subprocess.run([
        "ffmpeg", "-y",
        "-ss", str(start), "-t", str(duration),
        "-i", video_path,
        "-vf",
        "crop=ih*9/16:ih,scale=720:1280,drawtext=text='Best Moment':x=10:y=H-th-10:fontsize=24:fontcolor=white",
        "-c:v", "libx264",
        "-preset", "fast",
        "-an",
        final_path
    ], check=True)
    return final_path