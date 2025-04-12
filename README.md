
Flask Password Manager

A secure, token-based password manager built with Flask, JWT Authentication, and Fernet Encryption. It allows users to store, retrieve, update, and delete passwords securely using a master password.

---

 Features

- User registration and login with hashed master passwords
- JWT-based authentication
- Encrypted password storage using Fernet (symmetric encryption)
- Master password verification on sensitive actions
- Change master password (with re-encryption)
- Modular code structure for easy scaling
- Environment variables via `.env` file

---
Project Structure

```
project/
│
├── app/
│   ├── __init__.py
│   ├── routes/
│   ├── utils/
│
├── data/
│   ├── users.json
│   ├── passwords.json
│
├── requirements.txt
├── run.py              
├── .env                
├── README.md
```

---

API Endpoints

| Method | Endpoint                          | Description                        |
|--------|-----------------------------------|------------------------------------|
| POST   | `/api/register`                   | Register new user                  |
| POST   | `/api/login`                      | Log in and receive JWT token       |
| GET    | `/api/passwords`                  | Get decrypted passwords (JWT + master password required) |
| POST   | `/api/passwords`                  | Add new password (JWT + master password required) |
| PUT    | `/api/passwords/<id>`             | Update password                    |
| DELETE | `/api/passwords/<id>`             | Delete password                    |
| POST   | `/api/change-master-password`     | Change master password             |

---

## Security Notes

- Passwords are encrypted using a key derived from the master password + a salt
- Master passwords are hashed using `werkzeug.security`
- JWT tokens expire in 1 hour by default
- Avoid pushing `*.json` or `.env` files to public repositories

MIT License. Use this project freely, just don’t forget to give credit. ✌️
