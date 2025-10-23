from flask import Flask
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__)
    CORS(app)  # This will enable CORS for all routes

    # Note: On Vercel, environment variables are set automatically, no need for load_dotenv

    # Register blueprints
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

# Create the app instance for Gunicorn or Vercel
app = create_app()
