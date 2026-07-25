from flask import Blueprint, jsonify, request, session

from services.email_service import (
    EmailProcessingError,
    GeminiClientError,
    allowed_file,
    extract_text_from_pdf,
    extract_text_from_txt,
    process_email_with_gemini,
)

email_bp = Blueprint("email", __name__)


@email_bp.route("/process", methods=["POST"])
def process_email():
    text = None
    historico = session.get("historico", [])

    file_storage = request.files.get("file")
    if file_storage and file_storage.filename:
        if not allowed_file(file_storage.filename):
            return jsonify({"erro": "Tipo de arquivo não suportado. Envie um arquivo .txt ou .pdf."}), 400

        try:
            if file_storage.filename.lower().endswith(".txt"):
                text = extract_text_from_txt(file_storage)
            elif file_storage.filename.lower().endswith(".pdf"):
                text = extract_text_from_pdf(file_storage)
        except EmailProcessingError as exc:
            return jsonify({"erro": str(exc)}), 400

    if not text:
        text = request.form.get("email", "").strip()

    if not text:
        return jsonify({"erro": "Nenhum email ou arquivo válido enviado."}), 400

    try:
        email_info = process_email_with_gemini("Sem Assunto", text)
    except GeminiClientError as exc:
        return jsonify({"erro": str(exc)}), 502

    historico.append(email_info)
    session["historico"] = historico[-5:]

    return jsonify(email_info)


@email_bp.route("/clear_history", methods=["POST"])
def clear_history():
    session.pop("historico", None)
    return jsonify({"mensagem": "Histórico apagado com sucesso!"})