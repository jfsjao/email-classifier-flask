import io
import json
import logging
import re
from typing import Any

import pdfminer.high_level
import requests
from flask import current_app

logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {"txt", "pdf"}


class EmailProcessingError(Exception):
    """Raised when an email cannot be processed."""


class GeminiClientError(Exception):
    """Raised when the Gemini API request fails."""


def allowed_file(filename: str) -> bool:
    if not filename:
        return False
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_txt(file_storage: Any) -> str:
    try:
        return file_storage.read().decode("utf-8").strip()
    except UnicodeDecodeError as exc:
        raise EmailProcessingError("Não foi possível ler o arquivo TXT como texto UTF-8.") from exc
    except Exception as exc:
        raise EmailProcessingError(f"Erro ao ler arquivo TXT: {exc}") from exc


def extract_text_from_pdf(file_storage: Any) -> str:
    try:
        pdf_content = io.BytesIO(file_storage.read())
        text = pdfminer.high_level.extract_text(pdf_content)
        if not text:
            raise EmailProcessingError("Nenhum texto foi encontrado no PDF.")
        return text.strip()
    except EmailProcessingError:
        raise
    except Exception as exc:
        raise EmailProcessingError(f"Erro ao extrair texto do PDF: {exc}") from exc


def extract_subject(text: str) -> str:
    match = re.search(r"(?i)(?:assunto|subject):\s*(.+)", text)
    return match.group(1).strip() if match else "Sem Assunto"


def build_prompt(text: str) -> str:
    subject = extract_subject(text)
    return f"""
    Você é um assistente de email. Seu trabalho é classificar emails e gerar respostas.

    **Classificação de Emails:**
    - PRODUTIVO: Se o email contém uma solicitação, dúvida ou requer ação do suporte.
    - IMPRODUTIVO: Se o email não requer uma ação específica (ex.: agradecimentos, felicitações).

    **Tarefa:**
    - Classifique o email abaixo como PRODUTIVO ou IMPRODUTIVO.
    - Gere uma resposta curta e profissional.
    - Se o assunto não for detectado, gere um baseado no conteúdo do email.
    - Retorne os dados no formato JSON.

    **Assunto do Email:** {subject if subject else 'Gere um assunto apropriado'}
    **Conteúdo do Email:** {text}

    **Formato da resposta JSON:**
    {{
      "assunto": "Assunto detectado ou gerado",
      "categoria": "Produtivo" ou "Improdutivo",
      "resposta": "Texto formatado da resposta gerada."
    }}
    """


def process_email_with_gemini(assunto: str, text: str) -> dict[str, Any]:
    api_key = current_app.config.get("GEMINI_API_KEY")
    if not api_key:
        logger.warning("GEMINI_API_KEY não configurada; retornando resposta padrão.")
        return {
            "assunto": assunto or "Sem Assunto",
            "email": text,
            "categoria": "Improdutivo",
            "resposta": "Resposta automática indisponível no momento. Configure GEMINI_API_KEY para ativar a IA.",
        }

    prompt = build_prompt(text)
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    endpoint = current_app.config.get("GEMINI_API_URL") or f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

    try:
        response = requests.post(
            endpoint,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=20,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise GeminiClientError(f"Erro na comunicação com a API Gemini: {exc}") from exc

    try:
        data = response.json()
    except ValueError as exc:
        raise GeminiClientError("Resposta inválida da API Gemini.") from exc

    if not data.get("candidates"):
        raise GeminiClientError("Resposta vazia da API Gemini.")

    gemini_text = data["candidates"][0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()
    gemini_text = gemini_text.replace("```json", "").replace("```", "").strip()

    try:
        resultado = json.loads(gemini_text)
    except json.JSONDecodeError as exc:
        raise GeminiClientError("Erro ao interpretar a resposta da IA.") from exc

    return {
        "assunto": resultado.get("assunto", assunto or "Sem Assunto"),
        "email": text,
        "categoria": resultado.get("categoria", "Desconhecido"),
        "resposta": resultado.get("resposta", "Nenhuma resposta gerada."),
    }
