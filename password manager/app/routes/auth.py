from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app.utils.file_ops import get_users, save_users, get_passwords, save_passwords
import uuid
from datetime import datetime

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('master_password')
    if not username or not password:
        return jsonify({"error": "Username and master password required"}), 400

    users = get_users()
    if username in users:
        return jsonify({"error": "Username already exists"}), 409

    salt = uuid.uuid4().hex
    users[username] = {
        "username": username,
        "password_hash": generate_password_hash(password),
        "salt": salt,
        "created_at": datetime.now().isoformat()
    }

    save_users(users)
    passwords = get_passwords()
    passwords[username] = []
    save_passwords(passwords)

    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('master_password')

    users = get_users()
    if username not in users or not check_password_hash(users[username]['password_hash'], password):
        return jsonify({"error": "Invalid username or password"}), 401

    token = create_access_token(identity=username)
    return jsonify({"access_token": token, "username": username}), 200
