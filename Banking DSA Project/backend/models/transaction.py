"""
Transaction model for banking transactions.
"""

from datetime import datetime
from enum import Enum


class TransactionType(Enum):
    """Enum for transaction types."""
    DEPOSIT = "Deposit"
    WITHDRAWAL = "Withdrawal"
    TRANSFER = "Transfer"


class TransactionStatus(Enum):
    """Enum for transaction status."""
    PENDING = "Pending"
    COMPLETED = "Completed"
    FAILED = "Failed"
    REVERSED = "Reversed"


class Transaction:
    """
    Represents a financial transaction in the banking system.
    """
    
    def __init__(self, transaction_id, transaction_type, amount, from_account=None, to_account=None, description=""):
        """
        Initialize a new transaction.
        
        Args:
            transaction_id: Unique transaction identifier
            transaction_type: Type of transaction (TransactionType enum)
            amount: Transaction amount
            from_account: Source account ID (for withdrawals and transfers)
            to_account: Destination account ID (for deposits and transfers)
            description: Optional description
        """
        self.transaction_id = transaction_id
        self.transaction_type = transaction_type if isinstance(transaction_type, TransactionType) else TransactionType.DEPOSIT
        self.amount = amount
        self.from_account = from_account
        self.to_account = to_account
        self.description = description
        self.status = TransactionStatus.PENDING
        self.created_at = datetime.now()
        self.completed_at = None
        self.error_message = None
    
    def complete(self):
        """Mark the transaction as completed."""
        self.status = TransactionStatus.COMPLETED
        self.completed_at = datetime.now()
    
    def fail(self, error_message):
        """
        Mark the transaction as failed.
        
        Args:
            error_message: Reason for failure
        """
        self.status = TransactionStatus.FAILED
        self.error_message = error_message
        self.completed_at = datetime.now()
    
    def reverse(self):
        """Mark the transaction as reversed."""
        self.status = TransactionStatus.REVERSED
    
    def is_pending(self):
        """
        Check if transaction is pending.
        
        Returns:
            bool: True if pending, False otherwise
        """
        return self.status == TransactionStatus.PENDING
    
    def is_completed(self):
        """
        Check if transaction is completed.
        
        Returns:
            bool: True if completed, False otherwise
        """
        return self.status == TransactionStatus.COMPLETED
    
    def get_signature(self):
        """
        Generate a unique signature for fraud detection.
        
        Returns:
            str: Transaction signature
        """
        return f"{self.from_account}:{self.to_account}:{self.amount}:{self.transaction_type.value}"
    
    def to_dict(self):
        """
        Convert transaction to dictionary representation.
        
        Returns:
            dict: Transaction data as dictionary
        """
        return {
            'transaction_id': self.transaction_id,
            'transaction_type': self.transaction_type.value,
            'amount': self.amount,
            'from_account': self.from_account,
            'to_account': self.to_account,
            'description': self.description,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'error_message': self.error_message
        }
    
    def __str__(self):
        """String representation of the transaction."""
        return f"Transaction({self.transaction_id}, {self.transaction_type.value}, ₹{self.amount:.2f}, {self.status.value})"
    
    def __repr__(self):
        """Detailed representation of the transaction."""
        return f"Transaction(id={self.transaction_id}, type={self.transaction_type.value}, amount={self.amount}, status={self.status.value})"
