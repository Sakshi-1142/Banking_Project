"""
Data initializer for populating sample data.
"""

from backend.models.account import AccountType
from backend.models.complaint import ComplaintPriority


class DataInitializer:
    """
    Initializes the banking system with sample data for demonstration.
    """
    
    def __init__(self, banking_system):
        """
        Initialize the data initializer.
        
        Args:
            banking_system: Reference to the banking system
        """
        self.banking_system = banking_system
    
    def initialize_sample_data(self):
        """
        Create sample users, accounts, and transactions.
        
        Returns:
            dict: Summary of initialized data
        """
        print("\n=== Initializing Sample Data ===\n")
        
        # Create sample users
        users = self._create_sample_users()
        print(f"✓ Created {len(users)} sample users")
        
        # Create sample accounts
        accounts = self._create_sample_accounts(users)
        print(f"✓ Created {len(accounts)} sample accounts")
        
        # Create sample transactions
        transactions = self._create_sample_transactions(accounts)
        print(f"✓ Queued {len(transactions)} sample transactions")
        
        # Process transactions
        results = self.banking_system.process_pending_transactions()
        successful = sum(1 for r in results if r[0])
        print(f"✓ Processed {successful}/{len(results)} transactions successfully")
        
        # Create sample complaints
        complaints = self._create_sample_complaints(users)
        print(f"✓ Created {len(complaints)} sample complaints")
        
        print("\n=== Sample Data Initialization Complete ===\n")
        
        return {
            'users': len(users),
            'accounts': len(accounts),
            'transactions': len(transactions),
            'complaints': len(complaints)
        }
    
    def _create_sample_users(self):
        """Create sample users."""
        sample_users = [
            ("john_doe", "password123", "john.doe@email.com", "John Doe", "555-0101"),
            ("jane_smith", "password123", "jane.smith@email.com", "Jane Smith", "555-0102"),
            ("bob_wilson", "password123", "bob.wilson@email.com", "Bob Wilson", "555-0103"),
            ("alice_brown", "password123", "alice.brown@email.com", "Alice Brown", "555-0104"),
            ("charlie_davis", "password123", "charlie.davis@email.com", "Charlie Davis", "555-0105"),
        ]
        
        created_users = []
        for username, password, email, full_name, phone in sample_users:
            success, message, user = self.banking_system.auth_service.register(
                username, password, email, full_name, phone
            )
            if success:
                created_users.append(user)
        
        return created_users
    
    def _create_sample_accounts(self, users):
        """Create sample accounts for users."""
        created_accounts = []
        
        account_types = [AccountType.SAVINGS, AccountType.CHECKING, AccountType.BUSINESS]
        
        for i, user in enumerate(users):
            # Each user gets 1-2 accounts
            num_accounts = 1 if i % 2 == 0 else 2
            
            for j in range(num_accounts):
                account_type = account_types[j % len(account_types)]
                initial_balance = 1000.0 + (i * 500) + (j * 250)
                
                success, message, account = self.banking_system.account_service.create_account(
                    user.user_id, account_type, initial_balance
                )
                
                if success:
                    created_accounts.append(account)
                    # Add to search index
                    self.banking_system.search_service.add_account(account)
        
        return created_accounts
    
    def _create_sample_transactions(self, accounts):
        """Create sample transactions."""
        created_transactions = []
        
        if len(accounts) < 2:
            return created_transactions
        
        # Deposits
        for i in range(min(3, len(accounts))):
            success, message, trans = self.banking_system.transaction_service.deposit(
                accounts[i].account_id, 500.0, "Sample deposit"
            )
            if success:
                created_transactions.append(trans)
        
        # Withdrawals
        for i in range(min(2, len(accounts))):
            success, message, trans = self.banking_system.transaction_service.withdraw(
                accounts[i].account_id, 100.0, "Sample withdrawal"
            )
            if success:
                created_transactions.append(trans)
        
        # Transfers
        for i in range(min(2, len(accounts) - 1)):
            success, message, trans = self.banking_system.transaction_service.transfer(
                accounts[i].account_id,
                accounts[i + 1].account_id,
                200.0,
                "Sample transfer"
            )
            if success:
                created_transactions.append(trans)
        
        # Create a large transaction to trigger fraud detection
        if len(accounts) > 0:
            success, message, trans = self.banking_system.transaction_service.deposit(
                accounts[0].account_id, 15000.0, "Large deposit (fraud test)"
            )
            if success:
                created_transactions.append(trans)
        
        return created_transactions
    
    def _create_sample_complaints(self, users):
        """Create sample complaints."""
        created_complaints = []
        
        sample_complaints = [
            ("Transaction Issue", "My recent transfer didn't go through", ComplaintPriority.HIGH),
            ("Account Access", "Cannot access my account online", ComplaintPriority.MEDIUM),
            ("Card Problem", "My debit card was declined", ComplaintPriority.LOW),
        ]
        
        for i, (subject, description, priority) in enumerate(sample_complaints):
            if i < len(users):
                success, message, complaint = self.banking_system.complaint_service.create_complaint(
                    users[i].user_id, subject, description, priority
                )
                if success:
                    created_complaints.append(complaint)
        
        return created_complaints
