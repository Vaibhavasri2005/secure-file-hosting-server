import os
import hashlib
from datetime import datetime
from werkzeug.utils import secure_filename

class FileManager:
    """Manages file operations and metadata"""
    
    def __init__(self, upload_folder, allowed_extensions):
        self.upload_folder = upload_folder
        self.allowed_extensions = allowed_extensions
        self._ensure_upload_folder()
    
    def _ensure_upload_folder(self):
        """Create upload folder if it doesn't exist"""
        if not os.path.exists(self.upload_folder):
            os.makedirs(self.upload_folder)
    
    def get_user_folder(self, username):
        """Get or create user-specific folder"""
        user_folder = os.path.join(self.upload_folder, username)
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)
        return user_folder
    
    def allowed_file(self, filename):
        """Check if file extension is allowed"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.allowed_extensions
    
    def save_file(self, file, username, relative_path=''):
        """Save uploaded file to user's folder with optional subdirectory support"""
        if not file or file.filename == '':
            return None, "No file selected"
        
        # For folder uploads, allow any file type
        if not relative_path and not self.allowed_file(file.filename):
            return None, "File type not allowed"
        
        # Secure the filename and relative path
        filename = secure_filename(file.filename)
        if relative_path:
            relative_path = secure_filename(relative_path)
        
        # Get user folder
        user_folder = self.get_user_folder(username)
        
        # Create subdirectory if relative_path is provided
        if relative_path:
            target_folder = os.path.join(user_folder, relative_path)
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)
        else:
            target_folder = user_folder
        
        # Handle duplicate filenames
        base_name, ext = os.path.splitext(filename)
        counter = 1
        final_filename = filename
        file_path = os.path.join(target_folder, final_filename)
        
        while os.path.exists(file_path):
            final_filename = f"{base_name}_{counter}{ext}"
            file_path = os.path.join(target_folder, final_filename)
            counter += 1
        
        # Save the file
        file.save(file_path)
        
        # Calculate file hash for integrity
        file_hash = self._calculate_file_hash(file_path)
        
        # Return full path if in subdirectory
        if relative_path:
            return os.path.join(relative_path, final_filename), file_hash
        return final_filename, file_hash
    
    def _calculate_file_hash(self, file_path):
        """Calculate SHA-256 hash of file"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def get_user_files(self, username, path=''):
        """Get list of files and folders for a user"""
        user_folder = self.get_user_folder(username)
        if path:
            current_folder = os.path.join(user_folder, secure_filename(path))
        else:
            current_folder = user_folder
        
        if not os.path.exists(current_folder):
            return []
        
        items = []
        
        for item_name in os.listdir(current_folder):
            item_path = os.path.join(current_folder, item_name)
            stat = os.stat(item_path)
            
            if os.path.isdir(item_path):
                # Count files in directory
                file_count = sum([len(files) for r, d, files in os.walk(item_path)])
                items.append({
                    'name': item_name,
                    'type': 'folder',
                    'size': file_count,
                    'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                    'size_formatted': f"{file_count} items",
                    'path': os.path.join(path, item_name) if path else item_name
                })
            else:
                items.append({
                    'name': item_name,
                    'type': 'file',
                    'size': stat.st_size,
                    'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                    'size_formatted': self._format_file_size(stat.st_size),
                    'path': os.path.join(path, item_name) if path else item_name
                })
        
        # Sort folders first, then by name
        items.sort(key=lambda x: (x['type'] != 'folder', x['name']))
        return items
    
    def _format_file_size(self, size):
        """Format file size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} TB"
    
    def delete_file(self, username, filename):
        """Delete a file or folder from user's folder"""
        # Secure the filename
        filename = secure_filename(filename)
        user_folder = self.get_user_folder(username)
        file_path = os.path.join(user_folder, filename)
        
        if not os.path.exists(file_path):
            return False, "File or folder not found"
        
        try:
            if os.path.isdir(file_path):
                import shutil
                shutil.rmtree(file_path)
                return True, "Folder deleted successfully"
            else:
                os.remove(file_path)
                return True, "File deleted successfully"
        except Exception as e:
            return False, f"Error deleting: {str(e)}"
    
    def get_file_path(self, username, filename):
        """Get full path to a file"""
        filename = secure_filename(filename)
        user_folder = self.get_user_folder(username)
        file_path = os.path.join(user_folder, filename)
        
        if os.path.exists(file_path):
            return file_path
        return None
