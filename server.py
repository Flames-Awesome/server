from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from yt_dlp import YoutubeDL
import os

app = Flask(__name__)
CORS(app)  # This enables CORS for all routes

def download_video(url, format):
    ydl_opts = {
        'format': 'bestvideo+bestaudio' if format == 'mp4' else 'bestaudio',
        'outtmpl': '%(id)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }] if format == 'mp3' else []
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_name = f"{info['id']}.{format}"
        return file_name

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    url = data.get('url')
    format = data.get('format', 'mp4')  # 'mp4' or 'mp3'

    if format not in ['mp4', 'mp3']:
        return jsonify({'error': 'Invalid format. Choose mp4 or mp3'}), 400

    try:
        file_name = download_video(url, format)
        return send_file(file_name, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Clean up the downloaded file after sending it
        if os.path.exists(file_name):
            os.remove(file_name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
