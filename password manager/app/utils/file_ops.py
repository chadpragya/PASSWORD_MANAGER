import json
import os

USERS_FILE = 'users.json'
PASSWORDS_FILE = 'passwords.json'

for file in [USERS_FILE, PASSWORDS_FILE]:
    if not os.path.exists(file):
        with open(file, 'w') as f:
            json.dump({} if file == USERS_FILE else [], f)

def get_users():
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def get_passwords():
    with open(PASSWORDS_FILE, 'r') as f:
        return json.load(f)

def save_passwords(passwords):
    with open(PASSWORDS_FILE, 'w') as f:
        json.dump(passwords, f, indent=2)
