from flask import Flask
from .database import init_db
from .routes import main
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(main)

    with app.app_context():
        init_db()

    return app