from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

def create_app():
    app = Flask(__name__)
    CORS(app)  # This will enable CORS for all routes

    # Load environment variables from .env file
    load_dotenv()

    # Register blueprints
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

# Create the app instance for Gunicorn
app = create_app()
