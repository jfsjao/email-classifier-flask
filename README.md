# 📩 Classificador Inteligente de Emails

O **Classificador Inteligente de Emails** é uma aplicação web baseada em Flask para classificar mensagens como produtivas ou improdutivas e gerar respostas sugeridas com apoio da API Gemini.

---

## 🏗️ Arquitetura atual

A aplicação foi reorganizada para seguir um padrão mais profissional:

- factory pattern para criação da aplicação Flask
- configuração centralizada via módulo de configuração
- rotas isoladas em blueprint
- camada de serviço dedicada para processamento de arquivos e integração com a IA
- tratamento explícito de erros para entradas inválidas e falhas de API

---

## 🚀 Tecnologias

- Python 3.10+
- Flask
- Google Gemini API
- pdfminer.six
- python-dotenv
- pytest/unittest para testes automatizados

---

## 🛠️ Instalação e configuração

### 1. Criar ambiente virtual
```sh
python -m venv .venv
source .venv/bin/activate
```

### 2. Instalar dependências
```sh
pip install -r requirements.txt
```

### 3. Configurar variáveis de ambiente
Copie o arquivo de exemplo e ajuste os valores:
```sh
cp .env.example .env
```

Exemplo:
```env
FLASK_SECRET_KEY=troque-esta-chave
FLASK_ENV=development
GEMINI_API_KEY=sua-chave-gemini
```

### 4. Executar a aplicação
```sh
python app.py
```

A aplicação fica disponível em http://127.0.0.1:10000/.

---

## 🧪 Testes

Os testes automatizados cobrem a criação da aplicação e as validações das rotas principais:

```sh
python -m unittest discover -s tests -v
```

---

## 🔧 Endpoints principais

- GET /
- GET /app
- POST /email/process
- POST /email/clear_history

A rota de processamento aceita um texto direto ou um arquivo .txt/.pdf.

---

## ✅ Melhorias aplicadas

- separação de responsabilidades entre rotas e serviços
- validação de upload e mensagens vazias
- respostas HTTP mais claras para erros
- configuração externa para chaves e ambiente
- histórico de sessão limitado e mais previsível
- estrutura pronta para evoluir para testes mais completos e novas integrações


