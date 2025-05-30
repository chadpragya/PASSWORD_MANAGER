import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app  # Import the create_app function from app/__init__.py

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)  # You can change debug=False for production
