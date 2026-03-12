"""
Transaction service for processing banking transactions.
"""

from backend.models.transaction import Transaction, TransactionType, TransactionStatus
from backend.dsa.queue import Queue


class TransactionService:
    """
    Service for handling transactions using a queue for processing.
    """
    
    def __init__(self, banking_system):
        """
        Initialize the transaction service.
        
        Args:
            banking_system: Reference to the main banking system
        """
        self.banking_system = banking_system
        self.transactions = {}  # transaction_id -> Transaction
        self.transaction_queue = Queue()
        self._next_transaction_id = 1
    
    def deposit(self, account_id, amount, description=""):
        """
        Create a deposit transaction.
        
        Args:
            account_id: Account ID to deposit to
            amount: Amount to deposit
            description: Optional description
            
        Returns:
            tuple: (success: bool, message: str, transaction: Transaction or None)
        """
        if amount <= 0:
            return False, "Amount must be positive", None
        
        # Create transaction
        transaction_id = f"T{self._next_transaction_id:08d}"
        self._next_transaction_id += 1
        
        transaction = Transaction(
            transaction_id,
            TransactionType.DEPOSIT,
            amount,
            to_account=account_id,
            description=description
        )
        
        # Add to queue and storage
        self.transactions[transaction_id] = transaction
        self.transaction_queue.enqueue(transaction)
        
        return True, "Deposit queued for processing", transaction
    
    def withdraw(self, account_id, amount, description=""):
        """
        Create a withdrawal transaction.
        
        Args:
            account_id: Account ID to withdraw from
            amount: Amount to withdraw
            description: Optional description
            
        Returns:
            tuple: (success: bool, message: str, transaction: Transaction or None)
        """
        if amount <= 0:
            return False, "Amount must be positive", None
        
        # Create transaction
        transaction_id = f"T{self._next_transaction_id:08d}"
        self._next_transaction_id += 1
        
        transaction = Transaction(
            transaction_id,
            TransactionType.WITHDRAWAL,
            amount,
            from_account=account_id,
            description=description
        )
        
        # Add to queue and storage
        self.transactions[transaction_id] = transaction
        self.transaction_queue.enqueue(transaction)
        
        return True, "Withdrawal queued for processing", transaction
    
    def transfer(self, from_account_id, to_account_id, amount, description=""):
        """
        Create a transfer transaction.
        
        Args:
            from_account_id: Source account ID
            to_account_id: Destination account ID
            amount: Amount to transfer
            description: Optional description
            
        Returns:
            tuple: (success: bool, message: str, transaction: Transaction or None)
        """
        if amount <= 0:
            return False, "Amount must be positive", None
        
        if from_account_id == to_account_id:
            return False, "Cannot transfer to the same account", None
        
        # Create transaction
        transaction_id = f"T{self._next_transaction_id:08d}"
        self._next_transaction_id += 1
        
        transaction = Transaction(
            transaction_id,
            TransactionType.TRANSFER,
            amount,
            from_account=from_account_id,
            to_account=to_account_id,
            description=description
        )
        
        # Add to queue and storage
        self.transactions[transaction_id] = transaction
        self.transaction_queue.enqueue(transaction)
        
        return True, "Transfer queued for processing", transaction
    
    def process_next_transaction(self):
        """
        Process the next transaction in the queue.
        
        Returns:
            tuple: (success: bool, message: str, transaction: Transaction or None)
        """
        if self.transaction_queue.is_empty():
            return False, "No transactions to process", None
        
        transaction = self.transaction_queue.dequeue()
        
        # Check for fraud
        fraud_detected = self.banking_system.fraud_service.check_transaction(transaction)
        if fraud_detected:
            transaction.fail("Fraud detected")
            return False, f"Transaction {transaction.transaction_id} failed: Fraud detected", transaction
        
        # Process based on type
        if transaction.transaction_type == TransactionType.DEPOSIT:
            return self._process_deposit(transaction)
        elif transaction.transaction_type == TransactionType.WITHDRAWAL:
            return self._process_withdrawal(transaction)
        elif transaction.transaction_type == TransactionType.TRANSFER:
            return self._process_transfer(transaction)
        
        transaction.fail("Unknown transaction type")
        return False, "Unknown transaction type", transaction
    
    def _process_deposit(self, transaction):
        """Process a deposit transaction."""
        account = self.banking_system.account_service.get_account(transaction.to_account)
        
        if not account:
            transaction.fail("Account not found")
            return False, "Account not found", transaction
        
        if not account.is_active():
            transaction.fail("Account is not active")
            return False, "Account is not active", transaction
        
        # Perform deposit
        account.deposit(transaction.amount)
        account.add_transaction(transaction.transaction_id)
        transaction.complete()
        
        return True, f"Deposit of ₹{transaction.amount:.2f} completed", transaction
    
    def _process_withdrawal(self, transaction):
        """Process a withdrawal transaction."""
        account = self.banking_system.account_service.get_account(transaction.from_account)
        
        if not account:
            transaction.fail("Account not found")
            return False, "Account not found", transaction
        
        if not account.is_active():
            transaction.fail("Account is not active")
            return False, "Account is not active", transaction
        
        if account.balance < transaction.amount:
            transaction.fail("Insufficient funds")
            return False, "Insufficient funds", transaction
        
        # Perform withdrawal
        account.withdraw(transaction.amount)
        account.add_transaction(transaction.transaction_id)
        transaction.complete()
        
        return True, f"Withdrawal of ₹{transaction.amount:.2f} completed", transaction
    
    def _process_transfer(self, transaction):
        """Process a transfer transaction."""
        from_account = self.banking_system.account_service.get_account(transaction.from_account)
        to_account = self.banking_system.account_service.get_account(transaction.to_account)
        
        if not from_account or not to_account:
            transaction.fail("Account not found")
            return False, "Account not found", transaction
        
        if not from_account.is_active() or not to_account.is_active():
            transaction.fail("Account is not active")
            return False, "Account is not active", transaction
        
        if from_account.balance < transaction.amount:
            transaction.fail("Insufficient funds")
            return False, "Insufficient funds", transaction
        
        # Perform transfer
        from_account.withdraw(transaction.amount)
        to_account.deposit(transaction.amount)
        from_account.add_transaction(transaction.transaction_id)
        to_account.add_transaction(transaction.transaction_id)
        transaction.complete()
        
        return True, f"Transfer of ₹{transaction.amount:.2f} completed", transaction
    
    def process_all_transactions(self):
        """
        Process all transactions in the queue.
        
        Returns:
            list: List of results for each transaction
        """
        results = []
        while not self.transaction_queue.is_empty():
            result = self.process_next_transaction()
            results.append(result)
        return results
    
    def get_transaction(self, transaction_id):
        """
        Get a transaction by ID.
        
        Args:
            transaction_id: Transaction ID
            
        Returns:
            Transaction: Transaction object or None
        """
        return self.transactions.get(transaction_id)
    
    def get_pending_transactions(self):
        """
        Get all pending transactions.
        
        Returns:
            list: List of pending transactions
        """
        return self.transaction_queue.get_all()
    
    def get_queue_size(self):
        """
        Get the number of pending transactions.
        
        Returns:
            int: Queue size
        """
        return self.transaction_queue.size()
