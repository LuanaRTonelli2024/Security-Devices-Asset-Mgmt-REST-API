from flask import request
from firebase_admin import auth

def validate_token():
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return 400

    if not auth_header.startswith("Bearer "):
        return 401

    token = auth_header.split(" ")[1]

    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token   # contém uid e claims

    except Exception:
        return 401
