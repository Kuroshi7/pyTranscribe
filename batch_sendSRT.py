import os
import requests
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

# Obter o token da API do .env
API_TOKEN = os.getenv("PANDA_API_TOKEN")
HEADERS = {
    "accept": "application/json",
    "Authorization": f"{API_TOKEN}"
}

folder_id = input("Digite o ID da pasta: ").strip()
LIST_URL = f"https://api-v2.pandavideo.com.br/videos?folder_id={folder_id}"

upload_folder = os.path.join("download_panda", folder_id)


def list_videos():
    """Obtém a lista de vídeos da pasta no Panda Video e retorna um dicionário {titulo_video: id_video}."""
    response = requests.get(LIST_URL, headers=HEADERS)
    if response.status_code == 200:
        videos = response.json().get("videos", [])
        return {os.path.splitext(video["title"])[0]: video["id"] for video in videos}
    else:
        print(f"❌ Erro ao listar vídeos: {response.status_code} - {response.text}")
        return {}


def map_srt_files():
    """
    Mapeia os arquivos .srt na pasta, associando ao nome do vídeo (sem extensão .mp4).
    Retorna um dicionário {titulo_video: caminho_srt}.
    """
    srt_map = {}
    for filename in os.listdir(upload_folder):
        if filename.endswith(".srt"):
            video_base_name = os.path.splitext(filename)[0]  # Remove .srt
            srt_map[video_base_name] = os.path.join(upload_folder, filename)
    return srt_map


def send_subtitle(video_title, video_id, srt_map):
    """
    Envia a legenda correta para o vídeo correspondente usando o ID correto.
    """
    srt_path = srt_map.get(video_title)  # Encontra a legenda correta

    if not srt_path:
        print(f"⚠️ Nenhuma legenda encontrada para '{video_title}'. Pulando...")
        return

    # URL para envio de legendas
    upload_url = f"https://api-v2.pandavideo.com.br/subtitles/{video_id}"

    # Fazer o upload da legenda correta
    with open(srt_path, "rb") as file:
        files = {"file": file}
        data = {
            "label": "Português",
            "srclang": "pt-br"
        }

        response = requests.post(upload_url, headers=HEADERS, files=files, data=data)

    if response.status_code == 200:
        print(f"✅ Legenda '{srt_path}' enviada com sucesso para vídeo ID '{video_id}' ({video_title}).")
    else:
        print(f"❌ Erro ao enviar legenda para '{video_title}': {response.status_code} - {response.text}")


def main():
    """
    Lista vídeos e envia as legendas correspondentes.
    """
    if not os.path.exists(upload_folder):
        print(f"❌ Erro: Pasta '{upload_folder}' não encontrada. Verifique o caminho.")
        return

    video_map = list_videos()  # Obtém {titulo_video: id_video}
    srt_map = map_srt_files()  # Obtém {titulo_video: caminho_srt}

    if video_map:
        print(f"📂 Foram encontrados {len(video_map)} vídeos na pasta {folder_id}. Iniciando uploads...")
        for title, video_id in video_map.items():
            send_subtitle(title, video_id, srt_map)
    else:
        print("❌ Nenhum vídeo encontrado ou ocorreu um erro na listagem.")


if __name__ == "__main__":
    main()
