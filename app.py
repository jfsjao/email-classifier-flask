import logging
import os

from flask import Flask, jsonify, render_template
from dotenv import load_dotenv

from config import TestingConfig, get_config
from routes.email_routes import email_bp


load_dotenv()


def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def create_app(config_object=None, testing=False):
    configure_logging()
    if testing:
        config_object = TestingConfig
    elif config_object is None:
        config_object = get_config()

    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(config_object)
    app.secret_key = app.config.get("SECRET_KEY", "chave_secreta_flask")

    app.register_blueprint(email_bp, url_prefix="/email")

    @app.route("/")
    def landing():
        return render_template("landing.html")

    @app.route("/app")
    def home():
        return render_template("index.html")

    @app.errorhandler(400)
    def handle_bad_request(error):
        return jsonify({"erro": "Requisição inválida."}), 400

    @app.errorhandler(404)
    def handle_not_found(error):
        return jsonify({"erro": "Recurso não encontrado."}), 404

    @app.errorhandler(500)
    def handle_server_error(error):
        return jsonify({"erro": "Erro interno do servidor."}), 500

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=app.config.get("DEBUG", False))
