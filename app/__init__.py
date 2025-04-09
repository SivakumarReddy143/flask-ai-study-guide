from flask import Flask
# from app.main import main as main_blueprint
from app.main.routes import main as main_blueprint
import firebase_admin
from firebase_admin import credentials, auth
def create_app():
    print("Creating Flask app...") 
    app = Flask(__name__)
    app.secret_key = 'Siva@143'
    cred = credentials.Certificate("app/config/serviceAccountKey.json")  # <- use your actual path here
    firebase_admin.initialize_app(cred)
    
    # Register blueprints
    print("Registering main blueprint...")
    app.register_blueprint(main_blueprint)

    return app