"""
Account service for account management operations.
"""

from backend.models.account import Account, AccountType, AccountStatus


class AccountService:
    """
    Service for handling account operations.
    """
    
    def __init__(self, banking_system):
        """
        Initialize the account service.
        
        Args:
            banking_system: Reference to the main banking system
        """
        self.banking_system = banking_system
        self.accounts = {}  # account_id -> Account
        self._next_account_id = 1
    
    def create_account(self, user_id, account_type, initial_balance=0.0):
        """
        Create a new account for a user.
        
        Args:
            user_id: User ID
            account_type: Type of account (AccountType enum or string)
            initial_balance: Starting balance (default: 0.0)
            
        Returns:
            tuple: (success: bool, message: str, account: Account or None)
        """
        # Verify user exists
        user = self.banking_system.auth_service.get_user_by_id(user_id)
        if not user:
            return False, "User not found", None
        
        # Convert string to AccountType if needed
        if isinstance(account_type, str):
            try:
                account_type = AccountType[account_type.upper()]
            except KeyError:
                return False, "Invalid account type", None
        
        # Create account
        account_id = f"A{self._next_account_id:06d}"
        self._next_account_id += 1
        
        account = Account(account_id, user_id, account_type, initial_balance)
        
        # Store account
        self.accounts[account_id] = account
        
        # Add to user's account list
        user.add_account(account_id)
        
        return True, "Account created successfully", account
    
    def get_account(self, account_id):
        """
        Get an account by ID.
        
        Args:
            account_id: Account ID
            
        Returns:
            Account: Account object or None
        """
        return self.accounts.get(account_id)
    
    def get_user_accounts(self, user_id):
        """
        Get all accounts for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            list: List of Account objects
        """
        user = self.banking_system.auth_service.get_user_by_id(user_id)
        if not user:
            return []
        
        return [self.accounts[acc_id] for acc_id in user.accounts if acc_id in self.accounts]
    
    def get_balance(self, account_id):
        """
        Get the balance of an account.
        
        Args:
            account_id: Account ID
            
        Returns:
            float: Account balance or None if not found
        """
        account = self.get_account(account_id)
        return account.balance if account else None
    
    def freeze_account(self, account_id):
        """
        Freeze an account.
        
        Args:
            account_id: Account ID
            
        Returns:
            tuple: (success: bool, message: str)
        """
        account = self.get_account(account_id)
        if not account:
            return False, "Account not found"
        
        account.freeze()
        return True, "Account frozen successfully"
    
    def unfreeze_account(self, account_id):
        """
        Unfreeze an account.
        
        Args:
            account_id: Account ID
            
        Returns:
            tuple: (success: bool, message: str)
        """
        account = self.get_account(account_id)
        if not account:
            return False, "Account not found"
        
        account.unfreeze()
        return True, "Account unfrozen successfully"
    
    def close_account(self, account_id):
        """
        Close an account.
        
        Args:
            account_id: Account ID
            
        Returns:
            tuple: (success: bool, message: str)
        """
        account = self.get_account(account_id)
        if not account:
            return False, "Account not found"
        
        if account.balance > 0:
            return False, "Cannot close account with positive balance"
        
        account.close()
        return True, "Account closed successfully"
    
    def get_transaction_history(self, account_id):
        """
        Get transaction history for an account.
        
        Args:
            account_id: Account ID
            
        Returns:
            list: List of Transaction objects
        """
        account = self.get_account(account_id)
        if not account:
            return []
        
        transactions = []
        for trans_id in account.transaction_history:
            trans = self.banking_system.transaction_service.get_transaction(trans_id)
            if trans:
                transactions.append(trans)
        
        return transactions
    
    def get_all_accounts(self):
        """
        Get all accounts.
        
        Returns:
            list: List of all accounts
        """
        return list(self.accounts.values())
