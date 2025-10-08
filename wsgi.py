"""WSGI entry point for production deployment"""
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import the Flask app
from app import app

if __name__ == "__main__":
    app.run()

