import os
import requests
import json
import logging
from dotenv import load_dotenv
import re

# Carregar variáveis de ambiente
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

def extract_subject(text):
    """ Tenta extrair o assunto do email a partir do texto. """
    match = re.search(r"(?i)(?:assunto|subject):\s*(.+)", text)
    if match:
        return match.group(1).strip()
    else:
        return ""

def process_email_with_gemini(assunto, text):
    """ Envia o email para a API Gemini e retorna a classificação e resposta formatada. """
    assunto_extraido = extract_subject(text)
    
    prompt = f"""
    Você é um assistente de email. Seu trabalho é classificar emails e gerar respostas.

    **Classificação de Emails:**
    - PRODUTIVO: Se o email contém uma solicitação, dúvida ou requer ação do suporte.
    - IMPRODUTIVO: Se o email não requer uma ação específica (ex.: agradecimentos, felicitações).

    **Tarefa:**
    - Classifique o email abaixo como PRODUTIVO ou IMPRODUTIVO.
    - Gere uma resposta curta e profissional.
    - Se o assunto não for detectado, gere um baseado no conteúdo do email.
    - Retorne os dados no formato JSON.

    **Assunto do Email:** {assunto_extraido if assunto_extraido else "Gere um assunto apropriado"}
    **Conteúdo do Email:** {text}

    **Formato da resposta JSON:**
    {{
      "assunto": "Assunto detectado ou gerado",
      "categoria": "Produtivo" ou "Improdutivo",
      "resposta": "Texto formatado da resposta gerada."
    }}
    """

    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(GEMINI_API_URL, json=payload, headers={"Content-Type": "application/json"})

        if response.status_code == 200:
            data = response.json()

            if "candidates" not in data or not data["candidates"]:
                logging.warning("Resposta vazia da API Gemini.")
                return {"erro": "Resposta vazia da IA."}

            gemini_text = data["candidates"][0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()
            gemini_text = gemini_text.replace("```json", "").replace("```", "").strip()

            try:
                resultado = json.loads(gemini_text)
                return {
                    "assunto": resultado.get("assunto", "(Sem Assunto)"),
                    "email": text,
                    "categoria": resultado.get("categoria", "Desconhecido"),
                    "resposta": resultado.get("resposta", "Nenhuma resposta gerada.")
                }
            except json.JSONDecodeError:
                logging.error("Erro ao converter resposta da IA para JSON.")
                return {"erro": "Erro ao interpretar a resposta da IA."}

        else:
            logging.error(f"Erro na API Gemini: {response.status_code} - {response.text}")
            return {"erro": f"Erro na API Gemini: {response.status_code} - {response.text}"}

    except Exception as e:
        logging.error(f"Erro na comunicação com a API Gemini: {str(e)}")
        return {"erro": f"Erro na comunicação com a API: {str(e)}"}
