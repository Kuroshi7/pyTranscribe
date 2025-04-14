import os
import re

import requests
import subprocess
from dotenv import load_dotenv


# Carregar variáveis do .env
load_dotenv()

# Obter o token da API do .env
API_TOKEN = os.getenv("PANDA_API_TOKEN")
HEADERS = {
    "accept": "application/json",
    "Authorization": f"{API_TOKEN}"  # Usa o token do .env
}

# Solicita o ID do folder ao usuário
folder_id = input("Digite o ID da pasta: ").strip()

# Monta a URL de listagem de videos
LIST_URL = f"https://api-v2.pandavideo.com.br/videos?folder_id={folder_id}"

def sanitize_filename(name):
    """Remove caracteres inválidos para nomes de arquivo"""
    return re.sub(r'[\\/*?:"<>|]', "", name)

def list_videos():
    """Obtém a lista de vídeos do da pasta."""
    response = requests.get(LIST_URL, headers=HEADERS)
    if response.status_code == 200:
        return response.json().get("videos", [])
    else:
        print(f"Erro ao listar vídeos: {response.status_code} - {response.text}")
        return []

def download_video(video):
    video_id = video.get("id")
    title = video.get("title")
    if not video_id:
        print(f"ID nao disponivel para video {title}")
        return
    #cria pasta para os videos
    download_folder = os.path.join("download_panda", folder_id)
    os.makedirs(download_folder, exist_ok=True)
    #limpa nome do video aplicando ext .mp4
    safe_title = sanitize_filename(title) + ".mp4"
    file_path = os.path.join(download_folder, safe_title)

    download_url = f"https://download-us01.pandavideo.com:7443/videos/{video_id}/sd/download"

    #Request POST para download
    response = requests.post(download_url, headers=HEADERS)
    if response.status_code == 200:
        with open(file_path, "wb") as f:
            f.write(response.content)
        print(f"Vídeo '{title}' baixado com sucesso!")
    else:
        print(f"Erro ao baixar {title}: {response.status_code} - {response.text}")


def main():
    videos = list_videos()
    if videos:
        print(f"Foram encontrados {len(videos)} vídeos na pasta {folder_id}. Iniciando downloads...")
        for video in videos:
            download_video(video)
    else:
        print("Nenhum vídeo encontrado ou ocorreu um erro na listagem.")


if __name__ == "__main__":
    main()