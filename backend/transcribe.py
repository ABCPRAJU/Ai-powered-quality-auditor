import whisper
import os
import sys
import subprocess
import urllib.request
import zipfile
import shutil

# Setup ffmpeg path
ffmpeg_dir = os.path.expanduser("~/.ffmpeg")
ffmpeg_bin = os.path.join(ffmpeg_dir, "ffmpeg.exe")

# Check if we need to download ffmpeg
if not os.path.exists(ffmpeg_bin):
    print("Downloading FFmpeg...")
    os.makedirs(ffmpeg_dir, exist_ok=True)
    try:
        # Download a portable ffmpeg build
        url = "https://github.com/GyanD/codexffmpeg/releases/download/8.0.1/ffmpeg-8.0.1-essentials_build.zip"
        zip_path = os.path.join(ffmpeg_dir, "ffmpeg.zip")
        urllib.request.urlretrieve(url, zip_path)
        print("Extracting FFmpeg...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(ffmpeg_dir)
        # Find and copy ffmpeg.exe to the right location
        for root, dirs, files in os.walk(ffmpeg_dir):
            if "ffmpeg.exe" in files:
                src = os.path.join(root, "ffmpeg.exe")
                shutil.copy(src, ffmpeg_bin)
                break
        os.remove(zip_path)
        print("FFmpeg installed successfully!")
    except Exception as e:
        print(f"Error downloading FFmpeg: {e}")
        print("Continuing with existing FFmpeg if available...")

# Add ffmpeg to PATH
if os.path.exists(ffmpeg_bin):
    os.environ['PATH'] = ffmpeg_dir + os.pathsep + os.environ.get('PATH', '')

model = whisper.load_model("base")
print("Transcribing... please wait.")
result = model.transcribe("../sample.mp3", fp16=False) 

# SAVE THE BATON: Write to a file so the Notebook can find it
output_path = os.path.join("../data", "1_raw_transcript.txt")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(result["text"])

print(f"Step 1 Complete: {output_path} created.")

print("Step 1 Complete: 1_raw_transcript.txt created.")