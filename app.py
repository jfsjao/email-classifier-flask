from flask import Flask, request, render_template, jsonify, session
import requests
import json
import os
import re
import io
import pdfminer.high_level
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Carregar variáveis de ambiente do .env
load_dotenv()

# Configuração da API Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("❌ ERRO: A chave da API Gemini não foi carregada. Verifique o arquivo .env.")

GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

# Inicialização do Flask
app = Flask(__name__, static_folder="static")
app.secret_key = os.getenv("FLASK_SECRET_KEY", "chave_secreta_flask")

# Configuração para uploads (sem armazenamento)
ALLOWED_EXTENSIONS = {"txt", "pdf"}

# Função para verificar extensão de arquivo
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Função para extrair texto de arquivos
def extract_text_from_txt(file):
    try:
        return file.read().decode("utf-8").strip()
    except Exception as e:
        return f"Erro ao ler arquivo TXT: {str(e)}"

def extract_text_from_pdf(file):
    try:
        pdf_content = io.BytesIO(file.read())
        return pdfminer.high_level.extract_text(pdf_content).strip()
    except Exception as e:
        return f"Erro ao extrair texto do PDF: {str(e)}"

# Função para extrair o assunto automaticamente
def extract_subject(text):
    match = re.search(r"(?i)assunto:\s*(.*)", text)
    return match.group(1).strip() if match else "Sem Assunto"

# Página inicial (Landing Page)
@app.route('/')
def landing():
    return render_template('landing.html')

# Página da aplicação principal
@app.route('/app')
def home():
    historico = session.get('historico', [])  # Recupera histórico da sessão
    return render_template('index.html', historico=historico)

# Rota para limpar o histórico do usuário
@app.route('/clear_history', methods=['POST'])
def clear_history():
    session.pop('historico', None)  # Remove o histórico da sessão do usuário
    return jsonify({"mensagem": "Histórico apagado com sucesso!"})

# Processamento de email
@app.route('/process', methods=['POST'])
def process_email():
    text = None
    historico = session.get('historico', [])  # Recupera histórico da sessão

    # Processamento de arquivos (sem armazenamento permanente)
    if 'file' in request.files and request.files['file'].filename != '':
        file = request.files['file']
        if file and allowed_file(file.filename):
            if file.filename.endswith(".txt"):
                text = extract_text_from_txt(file)
            elif file.filename.endswith(".pdf"):
                text = extract_text_from_pdf(file)

    # Se nenhum arquivo foi enviado, verifica o campo de texto
    if not text:
        text = request.form.get('email', '').strip()

    if not text:
        return jsonify({"erro": "Nenhum email ou arquivo válido enviado."})

    assunto = extract_subject(text)

    # Enviar requisição para a API Gemini
    prompt = f"""
    Você é um assistente de email. Seu trabalho é classificar emails e gerar respostas.

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

            # 🔍 Verifica se a resposta veio corretamente
            if "candidates" not in data or not data["candidates"]:
                return jsonify({"erro": "Resposta vazia da IA."})

            gemini_text = data["candidates"][0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()

            # 🔧 Remove `json` e `markdown` se existirem
            gemini_text = gemini_text.replace("```json", "").replace("```", "").strip()

            # Tenta converter para JSON
            try:
                resultado = json.loads(gemini_text)
            except json.JSONDecodeError:
                print("⚠️ Erro ao converter resposta para JSON:", gemini_text)
                return jsonify({"erro": "Erro ao interpretar a resposta da IA."})

            email_info = {
                "assunto": assunto,
                "email": text,
                "categoria": resultado.get("categoria", "Desconhecido"),
                "resposta": resultado.get("resposta", "Nenhuma resposta gerada.")
            }

            historico.append(email_info)
            session['historico'] = historico  # Salva o histórico na sessão do usuário

            return jsonify(email_info)

        else:
            print(f"❌ Erro na API Gemini: {response.status_code} - {response.text}")
            return jsonify({"erro": f"Erro na API Gemini: {response.status_code} - {response.text}"})

    except Exception as e:
        print(f"❌ Erro na comunicação com a API Gemini: {str(e)}")
        return jsonify({"erro": f"Erro na comunicação com a API: {str(e)}"})

# Iniciar o Flask
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Usa a porta fornecida pelo Render
    app.run(host="0.0.0.0", port=port)