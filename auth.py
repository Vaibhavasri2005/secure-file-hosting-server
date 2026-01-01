import os
import hashlib
import json
from datetime import datetime

class User:
    """Simple user class for authentication"""
    
    def __init__(self, username, password_hash=None):
        self.username = username
        self.password_hash = password_hash
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False
    
    def get_id(self):
        return self.username
    
    @staticmethod
    def hash_password(password):
        """Hash a password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def check_password(self, password):
        """Verify a password against the hash"""
        return self.password_hash == self.hash_password(password)


class UserManager:
    """Manages user storage and authentication"""
    
    def __init__(self, users_file='users.json'):
        self.users_file = users_file
        self._ensure_users_file()
    
    def _ensure_users_file(self):
        """Create users file if it doesn't exist"""
        if not os.path.exists(self.users_file):
            # Create default admin user
            default_users = {
                'admin': {
                    'password_hash': User.hash_password('admin123'),
                    'created_at': datetime.now().isoformat()
                }
            }
            with open(self.users_file, 'w') as f:
                json.dump(default_users, f, indent=2)
    
    def load_users(self):
        """Load users from file"""
        with open(self.users_file, 'r') as f:
            return json.load(f)
    
    def save_users(self, users):
        """Save users to file"""
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)
    
    def get_user(self, username):
        """Get a user by username"""
        users = self.load_users()
        if username in users:
            user_data = users[username]
            user = User(username, user_data['password_hash'])
            return user
        return None
    
    def authenticate(self, username, password):
        """Authenticate a user"""
        user = self.get_user(username)
        if user and user.check_password(password):
            return user
        return None
    
    def create_user(self, username, password):
        """Create a new user"""
        users = self.load_users()
        if username in users:
            return False, "User already exists"
        
        users[username] = {
            'password_hash': User.hash_password(password),
            'created_at': datetime.now().isoformat()
        }
        self.save_users(users)
        return True, "User created successfully"
    
    def user_exists(self, username):
        """Check if a user exists"""
        users = self.load_users()
        return username in users
