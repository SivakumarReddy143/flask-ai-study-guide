from flask import Flask
from app.main.routes import main as main_blueprint
import firebase_admin
from firebase_admin import credentials
import os
from dotenv import load_dotenv

def create_app():
    print("🔧 Loading environment variables...")
    load_dotenv()  # Load variables from .env

    print("🚀 Creating Flask app...") 
    app = Flask(__name__)

    # Set secret key from .env
    app.secret_key = os.getenv("FLASK_SECRET_KEY")

    # Load Firebase credentials path from .env
    firebase_cred_path = os.getenv("FIREBASE_CRED_PATH")
    cred = credentials.Certificate(firebase_cred_path)
    firebase_admin.initialize_app(cred)

    # Register blueprints
    print("📦 Registering main blueprint...")
    app.register_blueprint(main_blueprint)

    return app
