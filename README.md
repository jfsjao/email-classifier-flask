# 📩 Classificador Inteligente de Emails

O **Classificador Inteligente de Emails** é uma aplicação web baseada em Flask que utiliza a **API Gemini do Google** para classificar emails automaticamente como **produtivos** ou **improdutivos** e gerar respostas sugeridas com base no conteúdo analisado.

**https://classificador-de-email.onrender.com/**

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
---

## 🚀 Como Executar o Projeto

Após instalar as dependências e configurar o `.env`, execute:
```sh
python app.py
```

O servidor Flask será iniciado e estará acessível em **http://127.0.0.1:5000/** para testes local.

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

### 🗑️ **Limpeza de Histórico**
- O usuário pode limpar o histórico temporário com um botão.

### 🔄 **Botão de Voltar para a Landing Page**
- Um botão discreto no **canto superior esquerdo** permite retornar para a página inicial.

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

## 📜 **Arquivo `requirements.txt`**
Caso precise instalar as dependências manualmente, o **`requirements.txt`** contém:
```txt
flask
requests
pdfminer.six
python-dotenv
werkzeug
```
Instale usando:
```sh
pip install -r requirements.txt
```

---

## 🖥️ **Exemplo de Uso**
1. Acesse **http://127.0.0.1:5000/**, quando iniciado localmente, ou acesse https://classificador-de-email.onrender.com/
2. Clique em **"Começar Agora"**.
3. Digite ou envie um email para análise.
4. Veja a classificação e a resposta gerada automaticamente.

---

## 📢 **Autor**
Desenvolvido por **João Felipe Silva**  
🔗 [LinkedIn](https://www.linkedin.com/in/joao-silva-jfs/)  
🔗 [GitHub](https://github.com/jfsjao)  

---

