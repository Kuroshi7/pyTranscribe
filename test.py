import whisper

model = whisper.load_model("large")  # Para CPU
# Ou, se quiser rodar na GPU:
# model = whisper.load_model("large", device="cuda")

print("Modelo carregado:", model.model_name)
