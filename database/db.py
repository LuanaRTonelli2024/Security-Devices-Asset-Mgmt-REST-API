import firebase_admin
from firebase_admin import credentials, firestore, auth
import app_config as config

class Database:
    def __init__(self):
        # Load Firebase credentials from JSON file
        cred = credentials.Certificate(config.CONST_FIREBASE_CREDENTIALS)

        # Initialize Firebase app only once
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred, {
                "projectId": config.CONST_FIREBASE_PROJECT_ID
            })

        # Firestore client
        self.__db_connection = firestore.client()

    @property
    def database(self):
        # Return Firestore client instance
        return self.__db_connection


