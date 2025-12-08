from flask import Flask, jsonify, request
from views.user_view import user
from views.company_view import company
from views.camera_view import camera



app = Flask(__name__)

app.register_blueprint(user)
app.register_blueprint(company)
app.register_blueprint(camera)

@app.route('/', methods=['GET'])
def home():
   return "<h1>HOME</h1>"

if __name__ == "__main__":
    app.run(debug=True)
