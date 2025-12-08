import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyCt7VoQKfW_v2ZwbHPNrLlua1y6VReXYLE",
    "authDomain": "securitydevassetsmgt.firebaseapp.com",
    "databaseURL": "https://securitydevassetsmgt.firebaseio.com",
    "projectId": "securitydevassetsmgt",
    "storageBucket": "securitydevassetsmgt.appspot.com",
    "messagingSenderId": "123456789012",
    "appId": "1:123456789012:web:abcdef123456"

}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

email = "luana@gmail.com"
password = "123456"

try:
    user = auth.sign_in_with_email_and_password(email, password)
    id_token = user['idToken']
    print("ID Token:", id_token)
except Exception as e:
    print("Erro ao gerar token:", e)
