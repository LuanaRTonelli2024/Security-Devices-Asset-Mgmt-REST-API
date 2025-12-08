# app_config.py
# Configuration constants for Firebase and JWT

# Path to Firebase service account JSON file
CONST_FIREBASE_CREDENTIALS = "firebase.json"

# Firebase project ID
CONST_FIREBASE_PROJECT_ID = "securitydevassetsmgt"

# Firestore collections
CONST_USER_COLLECTION = "users"
CONST_COMPANY_COLLECTION = "companies"
CONST_CAMERA_COLLECTION = "cameras"

# JWT configuration
JWT_EXPIRATION = 86400 * 30  # 30 days
TOKEN_SECRET = "ls3fall"