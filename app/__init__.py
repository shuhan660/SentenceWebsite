from flask import Flask
from config import Config
from app.models import db


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():

        # 👉 延遲 import（重點）
        from app.routes import main

        app.register_blueprint(main)

        db.create_all()

    return app