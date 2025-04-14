import os
import torch
from moviepy import VideoFileClip
import whisper



# Função para liberar memória da GPU após o processamento
def clear_gpu_memory():
    torch.cuda.empty_cache()



# Função para formatar timestamp no formato SRT (hh:mm:ss,ms)
def format_timestamp(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

# Função para tentar carregar o modelo Whisper com configurações de GPU
def load_whisper_model():
    try:
        print("Tentando carregar modelo Whisper...")
        model = whisper.load_model("base", device="cuda")
        return model
    except RuntimeError as e:
        print(f"Erro ao carregar modelo com CUDA: {e}")
        print("Tentando carregar modelo no CPU...")
        model = whisper.load_model("small", device="cpu")
        return model
    except Exception as e:
        print(f"Erro inesperado ao carregar o modelo: {e}")
        return None

# Função principal para gerar legendas SRT usando o Whisper
def generate_whisper_srt(video_path, model):
    try:
        print(f"Processando: {video_path}")
        # Extrair áudio do vídeo e salvar como WAV
        video = VideoFileClip(video_path)
        audio_path = video_path.rsplit(".", 1)[0] + '.wav'
        srt_path = video_path.rsplit(".", 1)[0] + '.srt'
        video.audio.write_audiofile(audio_path, codec="pcm_s16le")

        # Transcrever o áudio com Whisper
        print("Transcrevendo áudio...")
        result = model.transcribe(audio_path, language="pt")

        # Gerar o arquivo SRT a partir dos segmentos retornados
        subtitles = []
        for i, segment in enumerate(result["segments"], start=1):
            start = segment["start"]
            end = segment["end"]
            text = segment["text"].strip()
            subtitles.append(
                f"{i}\n"
                f"{format_timestamp(start)} --> {format_timestamp(end)}\n"
                f"{text}\n"
            )

        with open(srt_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(subtitles))

        print(f"Legenda gerada: {srt_path}")
        os.remove(audio_path)
        os.remove(video_path)
        # Liberar memória da GPU após cada transcrição
        clear_gpu_memory()

    except Exception as e:
        print(f"[Erro] Ao processar {video_path}: {e}")

# Função para gerar legendas em lote para uma pasta de vídeos
def batch_generate_srts(folder_path):
    if not os.path.isdir(folder_path):
        print(f"[Erro] Pasta não encontrada: {folder_path}")
        return

    video_extensions = ['.mp4', '.avi', '.mov', '.mkv']
    processed_files = 0

    # Carregar o modelo Whisper uma única vez
    model = load_whisper_model()
    if model is None:
        print("Não foi possível carregar o modelo Whisper. Abortando o processo.")
        return

    # Processar todos os vídeos na pasta
    for filename in os.listdir(folder_path):
        if any(filename.lower().endswith(ext) for ext in video_extensions):
            video_path = os.path.join(folder_path, filename)
            generate_whisper_srt(video_path, model)
            processed_files += 1

    print(f"✅ {processed_files} arquivos processados com sucesso!")

# Executar o script para a pasta com os vídeos
batch_generate_srts(r"caminho da pasta")
