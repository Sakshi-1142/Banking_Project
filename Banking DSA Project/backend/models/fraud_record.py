"""
Fraud Record model for tracking suspicious activities.
"""

from datetime import datetime
from enum import Enum


class FraudType(Enum):
    """Enum for fraud types."""
    DUPLICATE_TRANSACTION = "Duplicate Transaction"
    UNUSUAL_AMOUNT = "Unusual Amount"
    RAPID_TRANSACTIONS = "Rapid Transactions"
    SUSPICIOUS_PATTERN = "Suspicious Pattern"
    ACCOUNT_TAKEOVER = "Account Takeover"


class FraudSeverity(Enum):
    """Enum for fraud severity."""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class FraudRecord:
    """
    Represents a fraud detection record in the banking system.
    """
    
    def __init__(self, record_id, user_id, account_id, fraud_type, description, severity=FraudSeverity.MEDIUM):
        """
        Initialize a new fraud record.
        
        Args:
            record_id: Unique record identifier
            user_id: ID of the user associated with the fraud
            account_id: ID of the account associated with the fraud
            fraud_type: Type of fraud detected (FraudType enum)
            description: Detailed description of the fraud
            severity: Severity level (FraudSeverity enum)
        """
        self.record_id = record_id
        self.user_id = user_id
        self.account_id = account_id
        self.fraud_type = fraud_type if isinstance(fraud_type, FraudType) else FraudType.SUSPICIOUS_PATTERN
        self.description = description
        self.severity = severity if isinstance(severity, FraudSeverity) else FraudSeverity.MEDIUM
        self.detected_at = datetime.now()
        self.is_resolved = False
        self.resolved_at = None
        self.action_taken = None
        self.related_transactions = []
    
    def add_related_transaction(self, transaction_id):
        """
        Add a related transaction to this fraud record.
        
        Args:
            transaction_id: Transaction ID to add
        """
        if transaction_id not in self.related_transactions:
            self.related_transactions.append(transaction_id)
    
    def resolve(self, action_taken):
        """
        Mark the fraud record as resolved.
        
        Args:
            action_taken: Description of action taken
        """
        self.is_resolved = True
        self.resolved_at = datetime.now()
        self.action_taken = action_taken
    
    def to_dict(self):
        """
        Convert fraud record to dictionary representation.
        
        Returns:
            dict: Fraud record data as dictionary
        """
        return {
            'record_id': self.record_id,
            'user_id': self.user_id,
            'account_id': self.account_id,
            'fraud_type': self.fraud_type.value,
            'description': self.description,
            'severity': self.severity.value,
            'detected_at': self.detected_at.isoformat(),
            'is_resolved': self.is_resolved,
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None,
            'action_taken': self.action_taken,
            'related_transactions': self.related_transactions
        }
    
    def __str__(self):
        """String representation of the fraud record."""
        return f"FraudRecord({self.record_id}, {self.fraud_type.value}, {self.severity.value})"
    
    def __repr__(self):
        """Detailed representation of the fraud record."""
        return f"FraudRecord(id={self.record_id}, type={self.fraud_type.value}, severity={self.severity.value}, resolved={self.is_resolved})"
