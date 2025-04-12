from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
from app.utils.file_ops import get_users, get_passwords, save_passwords
from app.utils.crypto import get_cipher
from datetime import datetime
import uuid

passwords_bp = Blueprint('passwords', __name__, url_prefix='/api/passwords')

@passwords_bp.route('', methods=['GET'])
@jwt_required()
def get_user_passwords():
    current_user = get_jwt_identity()
    master_password = request.headers.get('X-Master-Password')
    
    users = get_users()
    if not master_password or not check_password_hash(users[current_user]['password_hash'], master_password):
        return jsonify({"error": "Invalid or missing master password"}), 401

    cipher = get_cipher(master_password, users[current_user]['salt'])

    passwords = get_passwords().get(current_user, [])
    decrypted = []
    for entry in passwords:
        try:
            decrypted.append({
                "id": entry['id'],
                "site": entry['site'],
                "username": entry['username'],
                "password": cipher.decrypt(entry['encrypted_password'].encode()).decode(),
                "notes": entry.get('notes', ''),
                "created_at": entry['created_at'],
                "updated_at": entry['updated_at']
            })
        except:
            continue  # Skip undecryptable entries
    return jsonify(decrypted)


@passwords_bp.route('', methods=['POST'])
@jwt_required()
def add_password():
    current_user = get_jwt_identity()
    data = request.get_json()
    master_password = request.headers.get('X-Master-Password')

    if not data or not data.get('site') or not data.get('username') or not data.get('password'):
        return jsonify({"error": "Missing required fields"}), 400

    users = get_users()
    if not master_password or not check_password_hash(users[current_user]['password_hash'], master_password):
        return jsonify({"error": "Invalid master password"}), 401

    cipher = get_cipher(master_password, users[current_user]['salt'])

    entry = {
        "id": str(uuid.uuid4()),
        "site": data['site'],
        "username": data['username'],
        "encrypted_password": cipher.encrypt(data['password'].encode()).decode(),
        "notes": data.get('notes', ''),
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }

    passwords = get_passwords()
    passwords.setdefault(current_user, []).append(entry)
    save_passwords(passwords)

    return jsonify({
        "id": entry['id'],
        "site": entry['site'],
        "username": entry['username'],
        "password": data['password'],
        "notes": entry['notes'],
        "created_at": entry['created_at'],
        "updated_at": entry['updated_at']
    }), 201

# @passwords_bp.route('/store-password', methods=['POST'])
# @jwt_required()
# def store_password():
#     current_user = get_jwt_identity()
#     data = request.get_json()
#     master_password = request.headers.get('X-Master-Password')

#     if not data or not data.get('site') or not data.get('password'):
#         return jsonify({"error": "Missing required fields: site and password"}), 400

#     users = get_users()
#     if not master_password or not check_password_hash(users[current_user]['password_hash'], master_password):
#         return jsonify({"error": "Invalid master password"}), 401

#     cipher = get_cipher(master_password, users[current_user]['salt'])

#     site = data['site']
#     encrypted_password = cipher.encrypt(data['password'].encode()).decode()

#     passwords = get_passwords()
#     user_passwords = passwords.get(current_user, {})
#     user_passwords[site] = encrypted_password
#     passwords[current_user] = user_passwords
#     save_passwords(passwords)

#     return jsonify({"message": f"Password stored successfully for {site}"}), 201


@passwords_bp.route('/<password_id>', methods=['PUT'])
@jwt_required()
def update_password(password_id):
    current_user = get_jwt_identity()
    data = request.get_json()
    master_password = request.headers.get('X-Master-Password')

    users = get_users()
    if not master_password or not check_password_hash(users[current_user]['password_hash'], master_password):
        return jsonify({"error": "Invalid master password"}), 401

    cipher = get_cipher(master_password, users[current_user]['salt'])
    passwords = get_passwords()
    user_pwds = passwords.get(current_user, [])

    for i, entry in enumerate(user_pwds):
        if entry['id'] == password_id:
            if 'site' in data:
                entry['site'] = data['site']
            if 'username' in data:
                entry['username'] = data['username']
            if 'password' in data:
                entry['encrypted_password'] = cipher.encrypt(data['password'].encode()).decode()
            if 'notes' in data:
                entry['notes'] = data['notes']
            entry['updated_at'] = datetime.now().isoformat()

            user_pwds[i] = entry
            passwords[current_user] = user_pwds
            save_passwords(passwords)

            return jsonify({
                "id": entry['id'],
                "site": entry['site'],
                "username": entry['username'],
                "password": data.get('password', ''),
                "notes": entry['notes'],
                "created_at": entry['created_at'],
                "updated_at": entry['updated_at']
            })

    return jsonify({"error": "Password entry not found"}), 404


@passwords_bp.route('/<password_id>', methods=['DELETE'])
@jwt_required()
def delete_password(password_id):
    current_user = get_jwt_identity()
    passwords = get_passwords()
    user_pwds = passwords.get(current_user, [])

    for i, entry in enumerate(user_pwds):
        if entry['id'] == password_id:
            del user_pwds[i]
            passwords[current_user] = user_pwds
            save_passwords(passwords)
            return jsonify({"message": "Password deleted successfully"}), 200

    return jsonify({"error": "Password entry not found"}), 404
