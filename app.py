import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from config import config
from auth import UserManager, User
from file_manager import FileManager

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Load configuration
env = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[env])

# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

# Initialize managers
user_manager = UserManager()
file_manager = FileManager(app.config['UPLOAD_FOLDER'], app.config['ALLOWED_EXTENSIONS'])

@login_manager.user_loader
def load_user(username):
    """Load user for Flask-Login"""
    return user_manager.get_user(username)

@app.after_request
def set_security_headers(response):
    """Add security headers to all responses"""
    for header, value in app.config['SECURITY_HEADERS'].items():
        response.headers[header] = value
    return response

@app.route('/')
def index():
    """Home page - redirect to login or dashboard"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = user_manager.authenticate(username, password)
        if user:
            login_user(user)
            flash('Login successful!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not username or not password:
            flash('Username and password are required', 'error')
        elif len(username) < 3:
            flash('Username must be at least 3 characters', 'error')
        elif len(password) < 6:
            flash('Password must be at least 6 characters', 'error')
        elif password != confirm_password:
            flash('Passwords do not match', 'error')
        else:
            success, message = user_manager.create_user(username, password)
            if success:
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('login'))
            else:
                flash(message, 'error')
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    """Logout user"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard - shows uploaded files"""
    files = file_manager.get_user_files(current_user.username)
    return render_template('dashboard.html', files=files, username=current_user.username)

@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    """Handle file and folder upload"""
    # Check for both 'file' and 'files[]' for compatibility
    if 'file' not in request.files and 'files[]' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('dashboard'))
    
    # Get files from whichever input is present
    if 'file' in request.files:
        files = request.files.getlist('file')
    else:
        files = request.files.getlist('files[]')
    
    uploaded_count = 0
    error_count = 0
    
    for file in files:
        if file and file.filename:
            # Get the full path from the filename (includes folder structure for folder uploads)
            full_filename = file.filename
            relative_path = ''
            
            # Check if this is a folder upload (path contains /)
            if '/' in full_filename or '\\' in full_filename:
                # Normalize path separators
                full_filename = full_filename.replace('\\', '/')
                # Split into directory and filename
                path_parts = full_filename.rsplit('/', 1)
                if len(path_parts) == 2:
                    relative_path = path_parts[0]
                    file.filename = path_parts[1]  # Update filename to just the file name
            
            try:
                result, message = file_manager.save_file(file, current_user.username, relative_path)
                
                if result:
                    uploaded_count += 1
                    print(f"Successfully uploaded: {file.filename} to {relative_path}")
                else:
                    error_count += 1
                    print(f"Failed to upload: {file.filename} - {message}")
            except Exception as e:
                print(f"Error uploading {file.filename}: {str(e)}")
                error_count += 1
    
    if uploaded_count > 0:
        flash(f'✅ Successfully uploaded {uploaded_count} file(s)!', 'success')
        if error_count > 0:
            flash(f'⚠️ {error_count} file(s) failed to upload', 'error')
    else:
        flash('❌ No files were uploaded', 'error')
    
    return redirect(url_for('dashboard'))

@app.route('/download/<filename>')
@login_required
def download_file(filename):
    """Handle file download"""
    file_path = file_manager.get_file_path(current_user.username, filename)
    
    if file_path:
        return send_file(file_path, as_attachment=True, download_name=filename)
    else:
        flash('File not found', 'error')
        return redirect(url_for('dashboard'))

@app.route('/delete/<filename>', methods=['POST'])
@login_required
def delete_file(filename):
    """Handle file deletion"""
    success, message = file_manager.delete_file(current_user.username, filename)
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    
    return redirect(url_for('dashboard'))

@app.route('/api/files')
@login_required
def api_files():
    """API endpoint to get user files"""
    files = file_manager.get_user_files(current_user.username)
    return jsonify({'files': files, 'username': current_user.username})

@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return render_template('404.html'), 404

@app.errorhandler(413)
def request_entity_too_large(error):
    """413 error handler - file too large"""
    flash('File is too large. Maximum file size is 100MB.', 'error')
    return redirect(url_for('dashboard'))

@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Ensure upload folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    # Get port from environment variable for Railway deployment
    port = int(os.environ.get('PORT', 5000))
    
    # Run the application
    app.run(host='0.0.0.0', port=port, debug=True)
