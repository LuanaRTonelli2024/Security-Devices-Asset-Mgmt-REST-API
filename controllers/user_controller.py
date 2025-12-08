from flask import jsonify
from database.__init__ import database
import app_config as config

from firebase_admin import auth
from database import database
import app_config as config
from models.user_model import User


def create_user(displayName, email, password):
    try:
        # 1. Normalizar dados
        displayName = displayName.strip()
        email = email.lower().strip()

        # 2. Criar usuário no Firebase Auth
        user_record = auth.create_user(
            email=email,
            password=password,
            display_name=displayName
        )

        user = User(displayName, email, True)

        database.collection(config.CONST_USER_COLLECTION).document(user_record.uid).set({
            "displayName": user.displayName,
            "email": user.email,
            "isActive": user.isActive
        })

        return user_record.uid

    except Exception as e:
        raise Exception(f"Error on creating user: {str(e)}")

    
def fetch_users():
    try:
        users = []
        docs = database.collection(config.CONST_USER_COLLECTION).stream()

        for doc in docs:
            data = doc.to_dict()
            current_user = {
                'id': doc.id,                 
                'email': data.get('email'),   
                'name': data.get('displayName')
            }
            users.append(current_user)

        return jsonify({'users': users})
    except:
        raise Exception(f"Error on fetching users: {str(e)}")