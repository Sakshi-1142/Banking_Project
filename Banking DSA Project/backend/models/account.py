"""
Account model for bank accounts.
"""

from datetime import datetime
from enum import Enum


class AccountType(Enum):
    """Enum for account types."""
    SAVINGS = "Savings"
    CHECKING = "Checking"
    BUSINESS = "Business"


class AccountStatus(Enum):
    """Enum for account status."""
    ACTIVE = "Active"
    FROZEN = "Frozen"
    CLOSED = "Closed"


class Account:
    """
    Represents a bank account in the banking system.
    """
    
    def __init__(self, account_id, user_id, account_type, initial_balance=0.0):
        """
        Initialize a new account.
        
        Args:
            account_id: Unique account identifier
            user_id: ID of the user who owns this account
            account_type: Type of account (AccountType enum)
            initial_balance: Starting balance (default: 0.0)
        """
        self.account_id = account_id
        self.user_id = user_id
        self.account_type = account_type if isinstance(account_type, AccountType) else AccountType.SAVINGS
        self.balance = initial_balance
        self.status = AccountStatus.ACTIVE
        self.created_at = datetime.now()
        self.transaction_history = []  # List of transaction IDs
        self.interest_rate = self._get_default_interest_rate()
    
    def _get_default_interest_rate(self):
        """
        Get default interest rate based on account type.
        
        Returns:
            float: Interest rate as a percentage
        """
        rates = {
            AccountType.SAVINGS: 2.5,
            AccountType.CHECKING: 0.5,
            AccountType.BUSINESS: 1.5
        }
        return rates.get(self.account_type, 0.0)
    
    def deposit(self, amount):
        """
        Deposit money into the account.
        
        Args:
            amount: Amount to deposit
            
        Returns:
            bool: True if successful, False otherwise
        """
        if amount <= 0:
            return False
        
        self.balance += amount
        return True
    
    def withdraw(self, amount):
        """
        Withdraw money from the account.
        
        Args:
            amount: Amount to withdraw
            
        Returns:
            bool: True if successful, False otherwise
        """
        if amount <= 0 or amount > self.balance:
            return False
        
        self.balance -= amount
        return True
    
    def add_transaction(self, transaction_id):
        """
        Add a transaction to the account's history.
        
        Args:
            transaction_id: Transaction ID to add
        """
        self.transaction_history.append(transaction_id)
    
    def freeze(self):
        """Freeze the account."""
        self.status = AccountStatus.FROZEN
    
    def unfreeze(self):
        """Unfreeze the account."""
        self.status = AccountStatus.ACTIVE
    
    def close(self):
        """Close the account."""
        self.status = AccountStatus.CLOSED
    
    def is_active(self):
        """
        Check if account is active.
        
        Returns:
            bool: True if active, False otherwise
        """
        return self.status == AccountStatus.ACTIVE
    
    def to_dict(self):
        """
        Convert account to dictionary representation.
        
        Returns:
            dict: Account data as dictionary
        """
        return {
            'account_id': self.account_id,
            'user_id': self.user_id,
            'account_type': self.account_type.value,
            'balance': self.balance,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'interest_rate': self.interest_rate,
            'transaction_count': len(self.transaction_history)
        }
    
    def __str__(self):
        """String representation of the account."""
        return f"Account({self.account_id}, {self.account_type.value}, Balance: ₹{self.balance:.2f})"
    
    def __repr__(self):
        """Detailed representation of the account."""
        return f"Account(id={self.account_id}, type={self.account_type.value}, balance={self.balance}, status={self.status.value})"
