"""
Fraud detection service using bloom filters.
"""

from backend.dsa.bloom_filter import BloomFilter
from backend.models.fraud_record import FraudRecord, FraudType, FraudSeverity


class FraudService:
    """
    Service for detecting fraudulent transactions using bloom filters.
    """
    
    def __init__(self, banking_system):
        """
        Initialize the fraud service.
        
        Args:
            banking_system: Reference to the main banking system
        """
        self.banking_system = banking_system
        self.fraud_records = {}  # record_id -> FraudRecord
        self.transaction_bloom = BloomFilter(size=5000)  # For duplicate detection
        self.suspicious_patterns = BloomFilter(size=3000)  # For known fraud patterns
        self._next_record_id = 1
        
        # Thresholds
        self.large_amount_threshold = 10000.0
        self.rapid_transaction_window = {}  # account_id -> list of timestamps
    
    def check_transaction(self, transaction):
        """
        Check if a transaction is potentially fraudulent.
        
        Args:
            transaction: Transaction object to check
            
        Returns:
            bool: True if fraud detected, False otherwise
        """
        fraud_detected = False
        fraud_type = None
        severity = FraudSeverity.LOW
        description = ""
        
        # Check for duplicate transactions
        signature = transaction.get_signature()
        if self.transaction_bloom.contains(signature):
            fraud_detected = True
            fraud_type = FraudType.DUPLICATE_TRANSACTION
            severity = FraudSeverity.MEDIUM
            description = "Duplicate transaction detected"
        else:
            self.transaction_bloom.add(signature)
        
        # Check for unusually large amounts
        if transaction.amount > self.large_amount_threshold:
            fraud_detected = True
            fraud_type = FraudType.UNUSUAL_AMOUNT
            severity = FraudSeverity.HIGH
            description = f"Unusually large amount: ₹{transaction.amount:.2f}"
        
        # If fraud detected, create a record
        if fraud_detected:
            account_id = transaction.from_account or transaction.to_account
            user_id = None
            
            if account_id:
                account = self.banking_system.account_service.get_account(account_id)
                if account:
                    user_id = account.user_id
            
            self.create_fraud_record(
                user_id=user_id,
                account_id=account_id,
                fraud_type=fraud_type,
                description=description,
                severity=severity,
                transaction_id=transaction.transaction_id
            )
        
        return fraud_detected
    
    def create_fraud_record(self, user_id, account_id, fraud_type, description, severity=FraudSeverity.MEDIUM, transaction_id=None):
        """
        Create a new fraud record.
        
        Args:
            user_id: User ID
            account_id: Account ID
            fraud_type: Type of fraud (FraudType enum)
            description: Description of the fraud
            severity: Severity level (FraudSeverity enum)
            transaction_id: Related transaction ID (optional)
            
        Returns:
            FraudRecord: Created fraud record
        """
        record_id = f"F{self._next_record_id:06d}"
        self._next_record_id += 1
        
        record = FraudRecord(record_id, user_id, account_id, fraud_type, description, severity)
        
        if transaction_id:
            record.add_related_transaction(transaction_id)
        
        self.fraud_records[record_id] = record
        
        # Add pattern to bloom filter
        pattern = f"{fraud_type.value}:{account_id}"
        self.suspicious_patterns.add(pattern)
        
        return record
    
    def get_fraud_record(self, record_id):
        """
        Get a fraud record by ID.
        
        Args:
            record_id: Record ID
            
        Returns:
            FraudRecord: Fraud record or None
        """
        return self.fraud_records.get(record_id)
    
    def get_user_fraud_records(self, user_id):
        """
        Get all fraud records for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            list: List of FraudRecord objects
        """
        return [record for record in self.fraud_records.values() if record.user_id == user_id]
    
    def get_account_fraud_records(self, account_id):
        """
        Get all fraud records for an account.
        
        Args:
            account_id: Account ID
            
        Returns:
            list: List of FraudRecord objects
        """
        return [record for record in self.fraud_records.values() if record.account_id == account_id]
    
    def resolve_fraud_record(self, record_id, action_taken):
        """
        Resolve a fraud record.
        
        Args:
            record_id: Record ID
            action_taken: Description of action taken
            
        Returns:
            tuple: (success: bool, message: str)
        """
        record = self.get_fraud_record(record_id)
        if not record:
            return False, "Fraud record not found"
        
        record.resolve(action_taken)
        return True, "Fraud record resolved"
    
    def get_all_fraud_records(self):
        """
        Get all fraud records.
        
        Returns:
            list: List of all fraud records
        """
        return list(self.fraud_records.values())
    
    def get_unresolved_fraud_records(self):
        """
        Get all unresolved fraud records.
        
        Returns:
            list: List of unresolved fraud records
        """
        return [record for record in self.fraud_records.values() if not record.is_resolved]
    
    def get_bloom_filter_stats(self):
        """
        Get statistics about the bloom filters.
        
        Returns:
            dict: Statistics about bloom filters
        """
        return {
            'transaction_bloom_fill': self.transaction_bloom.get_fill_ratio(),
            'suspicious_patterns_fill': self.suspicious_patterns.get_fill_ratio()
        }
