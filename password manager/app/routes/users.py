from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from app.utils.file_ops import get_users, save_users, get_passwords, save_passwords
from app.utils.crypto import get_cipher
from datetime import datetime
import uuid

users_bp = Blueprint('users', __name__, url_prefix='/api')

@users_bp.route('/change-master-password', methods=['POST'])
@jwt_required()
def change_master_password():
    current_user = get_jwt_identity()
    data = request.get_json()

    current_password = data.get('current_password')
    new_password = data.get('new_password')

    if not current_password or not new_password:
        return jsonify({"error": "Both current and new passwords required"}), 400

    users = get_users()
    user_data = users[current_user]

    if not check_password_hash(user_data['password_hash'], current_password):
        return jsonify({"error": "Current password is incorrect"}), 401

    passwords = get_passwords()
    user_pwds = passwords.get(current_user, [])

    old_cipher = get_cipher(current_password, user_data['salt'])
    new_salt = uuid.uuid4().hex
    new_cipher = get_cipher(new_password, new_salt)

    for entry in user_pwds:
        decrypted = old_cipher.decrypt(entry['encrypted_password'].encode()).decode()
        entry['encrypted_password'] = new_cipher.encrypt(decrypted.encode()).decode()

    user_data['password_hash'] = generate_password_hash(new_password)
    user_data['salt'] = new_salt

    users[current_user] = user_data
    passwords[current_user] = user_pwds

    save_users(users)
    save_passwords(passwords)

    return jsonify({"message": "Master password updated successfully"}), 200
