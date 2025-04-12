from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from app.config import Config
from app.routes.auth import auth_bp
from app.routes.passwords import passwords_bp

import os

jwt = JWTManager()

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(Config)
    jwt.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.passwords import passwords_bp
    from app.routes.users import users_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(passwords_bp)
    app.register_blueprint(users_bp)

    return app
