from flask import Flask, request, render_template, jsonify
import requests
import json
import os
import re
import pdfminer.high_level
from werkzeug.utils import secure_filename
from dotenv import load_dotenv  # Importa dotenv para carregar variáveis de ambiente

# Carregar variáveis de ambiente do .env
load_dotenv()

# Configuração da API Gemini
GEMINI_API_KEY = os.getenv("AIzaSyBswUz3euWllZchQpwJ5oocnkteNIN73p0")  # Obtém a chave do ambiente
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

# Inicialização do Flask
app = Flask(__name__, static_folder="static")
app.secret_key = os.getenv("FLASK_SECRET_KEY", "chave_secreta_flask")

# Configuração para upload
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"txt", "pdf"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Criar a pasta de uploads se não existir
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Nome do arquivo de histórico
HISTORICO_FILE = "historico.json"

# Função para verificar extensão de arquivo
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Função para extrair texto de arquivos .txt
def extract_text_from_txt(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read().strip()
    except Exception as e:
        return f"Erro ao ler arquivo TXT: {str(e)}"

# Função para extrair texto de arquivos .pdf
def extract_text_from_pdf(file_path):
    try:
        return pdfminer.high_level.extract_text(file_path).strip()
    except Exception as e:
        return f"Erro ao extrair texto do PDF: {str(e)}"

# Função para extrair o assunto automaticamente
def extract_subject(text):
    match = re.search(r"(?i)assunto:\s*(.*)", text)
    return match.group(1).strip() if match else "Sem Assunto"

# Função para carregar histórico do arquivo JSON
def carregar_historico():
    if os.path.exists(HISTORICO_FILE):
        with open(HISTORICO_FILE, "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

# Função para salvar histórico no arquivo JSON
def salvar_historico(historico):
    with open(HISTORICO_FILE, "w", encoding="utf-8") as file:
        json.dump(historico, file, ensure_ascii=False, indent=4)

# Página inicial
@app.route('/')
def home():
    historico = carregar_historico()
    return render_template('index.html', historico=historico)

# Rota para limpar o histórico
@app.route('/clear_history', methods=['POST'])
def clear_history():
    salvar_historico([])  # Apaga o histórico do arquivo
    return jsonify({"mensagem": "Histórico apagado com sucesso!"})

# Processamento de email
@app.route('/process', methods=['POST'])
def process_email():
    text = None
    historico = carregar_historico()

    # Processamento de arquivos
    if 'file' in request.files and request.files['file'].filename != '':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)

            if filename.endswith(".txt"):
                text = extract_text_from_txt(file_path)
            elif filename.endswith(".pdf"):
                text = extract_text_from_pdf(file_path)

    # Se nenhum arquivo foi enviado, verifica o campo de texto
    if not text:
        text = request.form.get('email', '').strip()

    if not text:
        return jsonify({"erro": "Nenhum email ou arquivo válido enviado."})

    assunto = extract_subject(text)

    # Enviar requisição para a API Gemini
    prompt = f"""
    Você é um assistente de email da AutoU. Seu trabalho é classificar emails e gerar respostas.

    **Classificação de Emails:**
    - PRODUTIVO: Se o email contém uma solicitação, dúvida ou requer ação do suporte.
    - IMPRODUTIVO: Se o email não requer uma ação específica (ex.: agradecimentos, felicitações).

    **Tarefa:**
    - Classifique o email abaixo como PRODUTIVO ou IMPRODUTIVO.
    - Gere uma resposta curta e profissional.
    - Inclua o assunto do email no início da resposta.

    **Assunto do Email:** {assunto}
    **Conteúdo do Email:** {text}

    **Formato da resposta JSON (sem markdown ou blocos de código):**
    {{
      "categoria": "Produtivo" ou "Improdutivo",
      "resposta": "Assunto: {assunto}\\n\\nTexto da resposta sugerida"
    }}
    """

    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(GEMINI_API_URL, json=payload, headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            data = response.json()
            gemini_text = data["candidates"][0]["content"]["parts"][0]["text"]
            gemini_text = gemini_text.replace("```json", "").replace("```", "").strip()
            
            try:
                resultado = json.loads(gemini_text)
            except json.JSONDecodeError:
                return jsonify({"erro": "Erro ao interpretar a resposta da IA."})

            email_info = {
                "assunto": assunto,
                "email": text,
                "categoria": resultado.get("categoria", "Desconhecido"),
                "resposta": resultado.get("resposta", "Nenhuma resposta gerada.")
            }

            historico.append(email_info)
            salvar_historico(historico)

            return jsonify(email_info)

        else:
            return jsonify({"erro": f"Erro na API Gemini: {response.status_code} - {response.text}"})

    except Exception as e:
        return jsonify({"erro": f"Erro na comunicação com a API: {str(e)}"})

# Iniciar o Flask
if __name__ == '__main__':
    app.run(debug=True)
