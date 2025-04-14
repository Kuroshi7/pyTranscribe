import os
import requests
import json
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

# Obter o token do ambiente
API_TOKEN = os.getenv("PANDA_API_TOKEN")

# URL da API
url = "https://api-v2.pandavideo.com.br/videos"

# Cabeçalhos da requisição
headers = {
    "accept": "application/json",
    "Authorization": f"{API_TOKEN}"  # Usa o token do .env
}

# Fazer a requisição GET
response = requests.get(url, headers=headers)

# Verificar se a resposta foi bem-sucedida
if response.status_code == 200:
    data = response.json()
    print(json.dumps(data, indent=4, ensure_ascii=False))
else:
    print(f"Erro {response.status_code}: {response.text}")
