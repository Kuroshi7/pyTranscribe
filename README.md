# 🛠️ **Panda Video Automation Tool**

**Panda Video Automation Tool** é uma ferramenta desenvolvida para automatizar o processo de download de vídeos da plataforma Panda Video, transcrição automática de áudio usando o modelo Whisper e upload de legendas em lote. A ferramenta foi projetada para ser eficiente, escalável e de fácil uso, especialmente para tarefas de legendagem em massa.

---

## 🚀 **Funcionalidades**

- 🔁 **Download em lote** de vídeos da plataforma Panda Video.
- 🎤 **Transcrição automática de áudio** com o modelo **Whisper** da OpenAI.
- 📝 **Geração de legendas** no formato **.srt**.
- 🧩 **Upload em lote** das legendas geradas para a plataforma Panda Video.
- ⚡ **Interface gráfica simples** para fácil controle do processo.
- 💻 **Multiplataforma**: Compatível com Windows e Linux.
- 🧃 Ideal para legendagem, mas pode ser adaptado para outras necessidades de processamento de vídeo.

---

## 📦 **Como Funciona**

A ferramenta realiza as seguintes etapas:

1. **Download de vídeos**: Baixa múltiplos vídeos em lote de uma pasta específica no Panda Video.
2. **Transcrição de áudio**: Extrai o áudio do vídeo e utiliza o modelo **Whisper** para gerar a transcrição.
3. **Geração de legendas**: Cria arquivos de legendas **.srt** baseados na transcrição.
4. **Upload de legendas**: Envia as legendas geradas para a plataforma Panda Video, associando-as aos vídeos correspondentes.

---

## 💡 **Exemplo de Caso Real (Case de Sucesso)**

Durante os testes, a ferramenta foi capaz de processar **5 vídeos** de uma vez, cada um com cerca de **30 minutos** de duração.

### 🔹 **Configuração utilizada**:
- **Número de vídeos**: 5
- **Modelo de transcrição**: Whisper
- **Tempo médio de transcrição por vídeo**: 5 minutos
- **Formato de legendas**: .srt

### 🔹 **Resultado**:
- **Tempo total de transcrição e upload**: Aproximadamente 20 minutos
- **Qualidade das legendas**: Alta precisão nas transcrições, com resultados satisfatórios para legendagem automática.
- **Processamento em lote**: Todos os vídeos foram processados sem falhas e as legendas enviadas corretamente.

✅ **Conclusão**: A ferramenta mostrou-se eficiente para o processo de transcrição e upload de legendas, permitindo o processamento em lote de múltiplos vídeos de forma rápida e precisa.

---

## 🧪 **Requisitos**

- Python 3.x
- **Whisper** para transcrição
- **MoviePy** para manipulação de vídeo
- Acesso à plataforma **Panda Video** (API)
  
Instale as dependências com:

```bash
pip install -r requirements.txt
