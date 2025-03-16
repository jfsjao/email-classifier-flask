# 📩 Classificador Inteligente de Emails

O **Classificador Inteligente de Emails** é uma aplicação web baseada em Flask que utiliza a **API Gemini do Google** para classificar emails automaticamente como **produtivos** ou **improdutivos** e gerar respostas sugeridas com base no conteúdo analisado.

🔗 **Acesse a aplicação em produção:** [Classificador de Email](https://classificador-de-email.onrender.com/)

---

## 🚀 Tecnologias Utilizadas

- **Python 3.8+**
- **Flask** (Framework Web)
- **Google Gemini API** (Inteligência Artificial)
- **JavaScript (Fetch API)** (Comunicação Assíncrona)
- **HTML5 e CSS3** (Interface Gráfica)
- **pdfminer.six** (Processamento de PDFs)
- **Session do Flask** (Histórico de Navegação)
- **LocalStorage** (Histórico Temporário no Navegador)

---

## 🛠️ Instalação e Configuração

### 1️⃣ **Clone o Repositório**
```sh
git clone https://github.com/jfsjao/email-classifier-flask.git
cd email-classifier-flask
```

### 2️⃣ **Crie um Ambiente Virtual (Recomendado)**
```sh
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3️⃣ **Instale as Dependências**
```sh
pip install -r requirements.txt
```

### 4️⃣ **Crie o arquivo `.env`**
```sh
echo GEMINI_API_KEY="sua-chave-aqui" > .env
```

---

## 🚀 Como Executar o Projeto

Após instalar as dependências e configurar o `.env`, execute:
```sh
python app.py
```

O servidor Flask será iniciado e estará acessível em **http://127.0.0.1:10000/** para testes locais.

---

## 📝 Funcionalidades

### 🏠 **Landing Page (Explicação do Sistema)**
- Explica de forma visual como o sistema funciona.
- Permite acessar a aplicação principal com um botão "Começar Agora".

### 📤 **Envio de Email ou Arquivo**
- O usuário pode **digitar um email manualmente** ou **enviar um arquivo** (`.txt` ou `.pdf`).
- O conteúdo do email é analisado automaticamente.

### 🤖 **Classificação Automática**
- A API Gemini classifica o email como:
  - **Produtivo** → Requer uma ação, dúvida ou suporte.
  - **Improdutivo** → Apenas informativo, agradecimentos, etc.

### ✉️ **Geração de Resposta Automática**
- A IA gera uma resposta automática para o email com base na análise.
- O usuário pode visualizar e copiar a resposta gerada.

### 📜 **Histórico Temporário**
- Os últimos **5 emails** analisados são armazenados temporariamente na **sessão do usuário** e no **LocalStorage**.
- O histórico **não é salvo permanentemente**.

---

## 🔧 **Endpoints da API**
### ➤ `GET /`
- Exibe a **Landing Page**.

### ➤ `GET /app`
- Exibe a **Página Principal** para classificar emails.

### ➤ `POST /process`
- Recebe um email ou arquivo e retorna a **classificação** e **resposta gerada**.
- **Parâmetros:**
  - `email` (opcional) → Texto do email.
  - `file` (opcional) → Arquivo `.txt` ou `.pdf`.
- **Resposta (JSON):**
```json
{
  "assunto": "Reunião sobre o projeto",
  "email": "Olá, gostaria de agendar uma reunião...",
  "categoria": "Produtivo",
  "resposta": "Assunto: Reunião sobre o projeto\n\nOlá, podemos marcar um horário para discutir os detalhes?"
}
```

### ➤ `POST /clear_history`
- Limpa o histórico temporário da sessão.

---

## 📜 **Arquivo `.gitignore` (Novo!)**
Para evitar que arquivos indesejados sejam enviados para o repositório, utilizamos um `.gitignore` com as seguintes regras:
```gitignore
# Ignorar ambiente virtual
venv/
.venv/

# Ignorar credenciais e variáveis de ambiente
.env

# Ignorar arquivos de cache do Python
__pycache__/
*.pyc
*.pyo

# Ignorar pastas do VSCode/PyCharm
.vscode/
.idea/

# Ignorar logs e banco de dados local
logs/
*.log
db.sqlite3

# Ignorar arquivos do sistema
.DS_Store
Thumbs.db
```

---

## 🖥️ **Exemplo de Uso**
1. Acesse **http://127.0.0.1:10000/** quando iniciado localmente ou visite **https://classificador-de-email.onrender.com/**
2. Clique em **"Começar Agora"**.
3. Digite ou envie um email para análise.
4. Veja a classificação e a resposta gerada automaticamente.

---

## 📢 **Autor**
Desenvolvido por **João Felipe Silva**  
🔗 [LinkedIn](https://www.linkedin.com/in/joao-silva-jfs/)  
🔗 [GitHub](https://github.com/jfsjao)  

---

