"""
Authentication service for user login and registration.
"""

from backend.models.user import User


class AuthService:
    """
    Service for handling user authentication and registration.
    """
    
    def __init__(self, banking_system):
        """
        Initialize the authentication service.
        
        Args:
            banking_system: Reference to the main banking system
        """
        self.banking_system = banking_system
        self.users = {}  # user_id -> User
        self.username_map = {}  # username -> user_id
        self.current_user = None
        self._next_user_id = 1
    
    def register(self, username, password, email, full_name, phone=None):
        """
        Register a new user.
        
        Args:
            username: Desired username
            password: Password
            email: Email address
            full_name: Full name
            phone: Phone number (optional)
            
        Returns:
            tuple: (success: bool, message: str, user: User or None)
        """
        # Check if username already exists
        if username in self.username_map:
            return False, "Username already exists", None
        
        # Create new user
        user_id = f"U{self._next_user_id:04d}"
        self._next_user_id += 1
        
        user = User(user_id, username, password, email, full_name, phone)
        
        # Store user
        self.users[user_id] = user
        self.username_map[username] = user_id
        
        # Add to search trie
        self.banking_system.search_service.add_user(user)
        
        return True, "Registration successful", user
    
    def login(self, username, password):
        """
        Authenticate a user.
        
        Args:
            username: Username
            password: Password
            
        Returns:
            tuple: (success: bool, message: str, user: User or None)
        """
        # Check if username exists
        if username not in self.username_map:
            return False, "Invalid username or password", None
        
        user_id = self.username_map[username]
        user = self.users[user_id]
        
        # Verify password
        if not user.verify_password(password):
            return False, "Invalid username or password", None
        
        # Check if account is active
        if not user.is_active:
            return False, "Account is inactive", None
        
        # Update last login
        user.update_last_login()
        self.current_user = user
        
        return True, "Login successful", user
    
    def logout(self):
        """
        Logout the current user.
        
        Returns:
            bool: True if successful
        """
        self.current_user = None
        return True
    
    def get_current_user(self):
        """
        Get the currently logged-in user.
        
        Returns:
            User: Current user or None
        """
        return self.current_user
    
    def get_user_by_id(self, user_id):
        """
        Get a user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            User: User object or None
        """
        return self.users.get(user_id)
    
    def get_user_by_username(self, username):
        """
        Get a user by username.
        
        Args:
            username: Username
            
        Returns:
            User: User object or None
        """
        user_id = self.username_map.get(username)
        return self.users.get(user_id) if user_id else None
    
    def is_authenticated(self):
        """
        Check if a user is currently authenticated.
        
        Returns:
            bool: True if authenticated, False otherwise
        """
        return self.current_user is not None
    
    def get_all_users(self):
        """
        Get all users.
        
        Returns:
            list: List of all users
        """
        return list(self.users.values())
