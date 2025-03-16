import io
import re
import pdfminer.high_level

def extract_text_from_txt(file):
    """ Lê e retorna o conteúdo de um arquivo .txt """
    try:
        return file.read().decode("utf-8").strip()
    except Exception as e:
        return f"Erro ao ler arquivo TXT: {str(e)}"

def extract_text_from_pdf(file):
    """ Extrai e retorna o texto de um arquivo PDF """
    try:
        pdf_content = io.BytesIO(file.read())
        return pdfminer.high_level.extract_text(pdf_content).strip()
    except Exception as e:
        return f"Erro ao extrair texto do PDF: {str(e)}"

def extract_subject(text):
    """ Tenta extrair o assunto do email a partir do texto """
    match = re.search(r"(?i)assunto:\s*(.*)", text)
    return match.group(1).strip() if match else "Sem Assunto"