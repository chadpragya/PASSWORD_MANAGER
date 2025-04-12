# app.py

from flask import Flask, jsonify
from flask.testing import FlaskClient
from flask_jwt_extended import JWTManager
from app.routes.auth import auth_bp
from app.routes.passwords import passwords_bp
from app.routes.users import users_bp

# 1. Create the Flask app object
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "secret"
    app.config['TESTING'] = True  # Enable testing mode

    # Initialize JWTManager
    jwt = JWTManager(app)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(passwords_bp)
    app.register_blueprint(users_bp)

    # 2. Define at least one route
    @app.route('/')
    def home():
        return jsonify({"message": "Welcome to the Password Manager!"}), 200

    return app

# Create the app instance
app = create_app()

# Optional: Define more routes here or import them from other files
# For example: from auth import auth_bp; app.register_blueprint(auth_bp)

# 3. Run the app if this file is executed directly
if __name__ == '__main__':
    app.run(debug=True)
