from flask import Flask
from controllers import user_controller  # Import your custom controller

# Initialize the Flask application
app = Flask(__name__)

# Simple route for testing
@app.route("/")
def home():
    # Return a basic response to confirm the app is running
    return "Flask application is running!"

# Entry point of the application
if __name__ == "__main__":
    # Run the app in debug mode (auto-reload on changes)
    app.run(debug=True)
