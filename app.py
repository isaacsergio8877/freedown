import os
import yt_dlp as youtube_dl
from flask import Flask, request, render_template, send_from_directory

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    video_info = None
    file_path = None
    if request.method == 'POST':
        video_url = request.form.get('video_url')
        if video_url:
            try:
                ydl_opts = {
                    'format': 'bestaudio/best',  # Escolhe o melhor formato de áudio disponível
                    'outtmpl': 'downloads/%(title)s.%(ext)s',  # Modelo de nome do arquivo de saída
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',  # Usa o FFmpeg para extrair apenas o áudio
                        'preferredcodec': 'mp3',  # Define o formato de saída para MP3
                        'preferredquality': '192',  # Qualidade de áudio em kbps
                    }],
                    'ffmpeg_location': r'C:\Users\zackg\Desktop\ffmpeg-7.0.1-essentials_build\ffmpeg-7.0.1-essentials_build\bin',  # Caminho para o FFmpeg
                    'quiet': False,  # Modo detalhado para ver o progresso
                }

                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(video_url, download=True)
                    video_info = {
                        "title": info_dict.get('title', 'Título não disponível'),
                        "views": info_dict.get('view_count', 'Visualizações não disponíveis'),
                        "duration": info_dict.get('duration', 'Duração não disponível'),
                    }
                    file_path = os.path.join('downloads/', f"{video_info['title']}.mp3")  # Garante que é .mp3

            except youtube_dl.DownloadError as e:
                video_info = {"error": f"Erro ao processar vídeo: {str(e)}"}
            except Exception as e:
                video_info = {"error": f"Erro inesperado: {str(e)}"}

    return render_template('index.html', video_info=video_info, file_path=file_path)

@app.route('/downloads/<filename>')
def download_file(filename):
    return send_from_directory('downloads', filename)

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    app.run(debug=True)
