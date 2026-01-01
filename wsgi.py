import os
from app import app

# Ensure upload folder exists
upload_folder = os.environ.get('UPLOAD_FOLDER', 'uploads')
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
