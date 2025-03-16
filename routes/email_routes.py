from flask import Blueprint, request, jsonify, session
import services.file_processing as file_processing
from services.gemini_service import process_email_with_gemini

# Criar Blueprint para as rotas de email
email_bp = Blueprint("email", __name__)

ALLOWED_EXTENSIONS = {"txt", "pdf"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Rota para processar emails
@email_bp.route("/process", methods=["POST"])
def process_email():
    text = None
    historico = session.get("historico", [])

    # Processar arquivos
    if "file" in request.files and request.files["file"].filename != "":
        file = request.files["file"]
        if file and allowed_file(file.filename):
            if file.filename.endswith(".txt"):
                text = file_processing.extract_text_from_txt(file)
            elif file.filename.endswith(".pdf"):
                text = file_processing.extract_text_from_pdf(file)

    # Se nenhum arquivo foi enviado, verifica o campo de texto
    if not text:
        text = request.form.get("email", "").strip()

    if not text:
        return jsonify({"erro": "Nenhum email ou arquivo válido enviado."})

    assunto = file_processing.extract_subject(text)

    # Processar com API Gemini
    email_info = process_email_with_gemini(assunto, text)

    historico.append(email_info)
    session["historico"] = historico  # Salvar histórico

    return jsonify(email_info)

# Rota para limpar histórico
@email_bp.route("/clear_history", methods=["POST"])
def clear_history():
    session.pop("historico", None)
    return jsonify({"mensagem": "Histórico apagado com sucesso!"})