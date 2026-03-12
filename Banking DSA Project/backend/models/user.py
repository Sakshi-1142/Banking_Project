"""
User model for authentication and profile management.
"""

from datetime import datetime
import hashlib


class User:
    """
    Represents a user in the banking system.
    """
    
    def __init__(self, user_id, username, password, email, full_name, phone=None):
        """
        Initialize a new user.
        
        Args:
            user_id: Unique user identifier
            username: Username for login
            password: Password (will be hashed)
            email: User's email address
            full_name: User's full name
            phone: User's phone number (optional)
        """
        self.user_id = user_id
        self.username = username
        self.password_hash = self._hash_password(password)
        self.email = email
        self.full_name = full_name
        self.phone = phone
        self.created_at = datetime.now()
        self.last_login = None
        self.is_active = True
        self.accounts = []  # List of account IDs
    
    def _hash_password(self, password):
        """
        Hash a password using SHA-256.
        
        Args:
            password: Plain text password
            
        Returns:
            str: Hashed password
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password):
        """
        Verify a password against the stored hash.
        
        Args:
            password: Plain text password to verify
            
        Returns:
            bool: True if password matches, False otherwise
        """
        return self.password_hash == self._hash_password(password)
    
    def update_last_login(self):
        """Update the last login timestamp."""
        self.last_login = datetime.now()
    
    def add_account(self, account_id):
        """
        Add an account to the user's account list.
        
        Args:
            account_id: Account ID to add
        """
        if account_id not in self.accounts:
            self.accounts.append(account_id)
    
    def to_dict(self):
        """
        Convert user to dictionary representation.
        
        Returns:
            dict: User data as dictionary
        """
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'phone': self.phone,
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'is_active': self.is_active,
            'accounts': self.accounts
        }
    
    def __str__(self):
        """String representation of the user."""
        return f"User({self.username}, {self.full_name})"
    
    def __repr__(self):
        """Detailed representation of the user."""
        return f"User(id={self.user_id}, username={self.username}, email={self.email})"
