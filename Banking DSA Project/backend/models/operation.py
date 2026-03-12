"""
Operation model for tracking reversible operations (undo/redo).
"""

from datetime import datetime
from enum import Enum


class OperationType(Enum):
    """Enum for operation types."""
    CREATE_ACCOUNT = "Create Account"
    UPDATE_PROFILE = "Update Profile"
    TRANSACTION = "Transaction"
    FREEZE_ACCOUNT = "Freeze Account"
    UNFREEZE_ACCOUNT = "Unfreeze Account"


class Operation:
    """
    Represents a reversible operation in the banking system.
    Used with Stack for undo/redo functionality.
    """
    
    def __init__(self, operation_id, operation_type, user_id, data, reverse_data=None):
        """
        Initialize a new operation.
        
        Args:
            operation_id: Unique operation identifier
            operation_type: Type of operation (OperationType enum)
            user_id: ID of the user who performed the operation
            data: Data associated with the operation
            reverse_data: Data needed to reverse the operation
        """
        self.operation_id = operation_id
        self.operation_type = operation_type if isinstance(operation_type, OperationType) else OperationType.TRANSACTION
        self.user_id = user_id
        self.data = data
        self.reverse_data = reverse_data
        self.timestamp = datetime.now()
        self.is_reversed = False
    
    def mark_reversed(self):
        """Mark this operation as reversed."""
        self.is_reversed = True
    
    def to_dict(self):
        """
        Convert operation to dictionary representation.
        
        Returns:
            dict: Operation data as dictionary
        """
        return {
            'operation_id': self.operation_id,
            'operation_type': self.operation_type.value,
            'user_id': self.user_id,
            'data': self.data,
            'reverse_data': self.reverse_data,
            'timestamp': self.timestamp.isoformat(),
            'is_reversed': self.is_reversed
        }
    
    def __str__(self):
        """String representation of the operation."""
        return f"Operation({self.operation_id}, {self.operation_type.value})"
    
    def __repr__(self):
        """Detailed representation of the operation."""
        return f"Operation(id={self.operation_id}, type={self.operation_type.value}, reversed={self.is_reversed})"
