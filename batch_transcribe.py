import os
import re
import requests
from dotenv import load_dotenv
import torch
from moviepy import VideoFileClip
import whisper
from concurrent.futures import ThreadPoolExecutor


# Carregar variáveis do .env
load_dotenv()

# Obter o token da API do .env
API_TOKEN = os.getenv("PANDA_API_TOKEN")
HEADERS = {
    "accept": "application/json",
    "Authorization": f"{API_TOKEN}"
}

# Solicita o ID do folder ao usuário
folder_id = input("Digite o ID da pasta: ").strip()

# Monta a URL de listagem de vídeos
LIST_URL = f"https://api-v2.pandavideo.com.br/videos?folder_id={folder_id}"


def sanitize_filename(name):
    """Remove caracteres inválidos para nomes de arquivo"""
    return re.sub(r'[\\/*?:"<>|]', "", name)


def list_videos():
    """Obtém a lista de vídeos da pasta."""
    response = requests.get(LIST_URL, headers=HEADERS)
    if response.status_code == 200:
        return response.json().get("videos", [])
    else:
        print(f"Erro ao listar vídeos: {response.status_code} - {response.text}")
        return []


def download_video(video):
    """Faz o download de um vídeo específico."""
    video_id = video.get("id")
    title = video.get("title")
    if not video_id:
        print(f"ID não disponível para vídeo {title}")
        return None

    download_folder = os.path.join("download_panda", folder_id)
    os.makedirs(download_folder, exist_ok=True)

    safe_title = sanitize_filename(title) + ".mp4"
    file_path = os.path.join(download_folder, safe_title)

    download_url = f"https://download-us01.pandavideo.com:7443/videos/{video_id}/sd/download"

    response = requests.post(download_url, headers=HEADERS)
    if response.status_code == 200:
        with open(file_path, "wb") as f:
            f.write(response.content)
        print(f"Vídeo '{title}' baixado com sucesso!")
        return file_path  # Retorna o caminho do arquivo baixado
    else:
        print(f"Erro ao baixar {title}: {response.status_code} - {response.text}")
        return None


def load_whisper_model():
    """Carrega o modelo Whisper uma única vez."""
    try:
        print("Carregando modelo Whisper...")
        return whisper.load_model("small", device="cuda")
    except RuntimeError:
        print("CUDA não disponível. Carregando no CPU...")
        return whisper.load_model("small", device="cpu")


def format_timestamp(seconds):
    """Formata o timestamp para o formato SRT (hh:mm:ss,ms)."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def generate_whisper_srt(video_path, model):
    """Gera o arquivo de legendas SRT a partir do vídeo."""
    try:
        print(f"Processando: {video_path}")
        video = VideoFileClip(video_path)
        audio_path = video_path.rsplit(".", 1)[0] + '.wav'
        srt_path = video_path.rsplit(".", 1)[0] + '.srt'
        video.audio.write_audiofile(audio_path, codec="pcm_s16le")

        # Transcrição com o Whisper
        result = model.transcribe(audio_path, language="pt")
        subtitles = []
        for i, segment in enumerate(result["segments"], start=1):
            subtitles.append(
                f"{i}\n"
                f"{format_timestamp(segment['start'])} --> {format_timestamp(segment['end'])}\n"
                f"{segment['text'].strip()}\n"
            )

        with open(srt_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(subtitles))

        print(f"Legenda gerada: {srt_path}")
        os.remove(audio_path)  # Remove o arquivo de áudio temporário

    except Exception as e:
        print(f"Erro ao processar {video_path}: {e}")
    try:
        os.remove(video_path)  # Remove o vídeo após gerar a legenda
        print(f"Arquivo removido :{video_path}")
    except Exception as e:
        print(f"Erro ao remover arquivo {e}")

def process_videos(video_paths, model):
    """Processa os vídeos em múltiplos threads"""
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(lambda video_path: generate_whisper_srt(video_path, model), video_paths)


def main():
    """Função principal para gerenciar o fluxo de trabalho."""
    # Obter a lista de vídeos
    videos = list_videos()
    if videos:
        print(f"Foram encontrados {len(videos)} vídeos na pasta {folder_id}. Iniciando downloads...")

        # Baixar todos os vídeos primeiro
        video_paths = []
        for video in videos:
            video_path = download_video(video)
            if video_path:
                video_paths.append(video_path)

        # Carregar o modelo uma única vez
        torch.cuda.empty_cache()
        model = load_whisper_model()
        if model is None:
            print("Falha ao carregar o modelo Whisper.")
            return

        # Gerar as legendas para cada vídeo
        for video_path in video_paths:
            generate_whisper_srt(video_path, model)

    else:
        print("Nenhum vídeo encontrado ou ocorreu um erro na listagem.")


if __name__ == "__main__":
    main()
