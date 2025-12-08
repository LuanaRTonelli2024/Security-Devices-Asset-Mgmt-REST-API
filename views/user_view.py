from flask import Blueprint, jsonify, request
from database.__init__ import database
from models.user_model import User
from controllers.user_controller import create_user, fetch_users
from firebase_admin import auth

user = Blueprint("user", __name__)

@user.route('/users/signup', methods=['POST'])
def add_user():
    try:
        my_body = request.json

        if 'email' not in my_body:
            return jsonify({'error': 'Email is needed in the request!'}), 400
        if 'name' not in my_body:
            return jsonify({'error': 'Name is needed in the request!'}), 400
        if 'password' not in my_body:
            return jsonify({'error': 'Password is needed in the request!'}), 400

        uid = create_user(my_body["name"], my_body["email"], my_body["password"])

        return jsonify({"id": uid}), 201

    except Exception as e:
        return jsonify({'error': f'Something went wrong: {str(e)}'}), 500
    


@user.route('/users/all', methods=['GET'])
def get_users():
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'Token is missing in the request!'}), 400

        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return jsonify({'error': 'Invalid authentication header format!'}), 400
        id_token = parts[1]

        try:
            decoded_token = auth.verify_id_token(id_token)
        except Exception:
            return jsonify({'error': 'Invalid authentication token!'}), 401

        return fetch_users()

    except Exception as e:
        return jsonify({'error': f'Something wrong happened when fetching users: {str(e)}'}), 500