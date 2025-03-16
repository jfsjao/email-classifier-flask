import os
import logging
from flask import Flask, render_template
from dotenv import load_dotenv
from routes.email_routes import email_bp

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Carregar variáveis de ambiente
load_dotenv()

# Inicializar Flask
app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = os.getenv("FLASK_SECRET_KEY", "chave_secreta_flask")

# Registrar blueprints (módulos de rotas)
app.register_blueprint(email_bp, url_prefix="/email")

# Página inicial
@app.route('/')
def landing():
    return render_template('landing.html')

# Página principal da aplicação
@app.route('/app')
def home():
    return render_template('index.html')

# Iniciar o Flask
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
