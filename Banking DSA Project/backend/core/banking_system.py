"""
Main Banking System orchestrator.
"""

from backend.services.auth_service import AuthService
from backend.services.account_service import AccountService
from backend.services.transaction_service import TransactionService
from backend.services.fraud_service import FraudService
from backend.services.complaint_service import ComplaintService
from backend.services.search_service import SearchService
from backend.dsa.stack import Stack


class BankingSystem:
    """
    Main banking system that orchestrates all services and data structures.
    """
    
    def __init__(self):
        """Initialize the banking system with all services."""
        # Initialize services (order matters for dependencies)
        self.search_service = SearchService(self)
        self.auth_service = AuthService(self)
        self.account_service = AccountService(self)
        self.fraud_service = FraudService(self)
        self.transaction_service = TransactionService(self)
        self.complaint_service = ComplaintService(self)
        
        # Operation history for undo/redo
        self.operation_history = Stack()
        self.redo_stack = Stack()
        
        print("Banking System initialized successfully!")
    
    def get_system_stats(self):
        """
        Get statistics about the banking system.
        
        Returns:
            dict: System statistics
        """
        return {
            'total_users': len(self.auth_service.users),
            'total_accounts': len(self.account_service.accounts),
            'total_transactions': len(self.transaction_service.transactions),
            'pending_transactions': self.transaction_service.get_queue_size(),
            'total_complaints': len(self.complaint_service.complaints),
            'open_complaints': len(self.complaint_service.get_open_complaints()),
            'total_fraud_records': len(self.fraud_service.fraud_records),
            'unresolved_fraud': len(self.fraud_service.get_unresolved_fraud_records()),
            'bloom_filter_stats': self.fraud_service.get_bloom_filter_stats()
        }
    
    def process_pending_transactions(self):
        """
        Process all pending transactions in the queue.
        
        Returns:
            list: Results of processing
        """
        return self.transaction_service.process_all_transactions()
    
    def search(self, query, search_type='users'):
        """
        Search for users or accounts.
        
        Args:
            query: Search query
            search_type: Type of search ('users' or 'accounts')
            
        Returns:
            list: Search results
        """
        if search_type == 'users':
            return self.search_service.search_users(query)
        elif search_type == 'accounts':
            return self.search_service.search_accounts(query)
        else:
            return []
    
    def get_user_dashboard(self, user_id):
        """
        Get dashboard data for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            dict: Dashboard data
        """
        user = self.auth_service.get_user_by_id(user_id)
        if not user:
            return None
        
        accounts = self.account_service.get_user_accounts(user_id)
        complaints = self.complaint_service.get_user_complaints(user_id)
        fraud_records = self.fraud_service.get_user_fraud_records(user_id)
        
        total_balance = sum(acc.balance for acc in accounts)
        
        return {
            'user': user.to_dict(),
            'accounts': [acc.to_dict() for acc in accounts],
            'total_balance': total_balance,
            'complaints': [c.to_dict() for c in complaints],
            'fraud_alerts': [f.to_dict() for f in fraud_records if not f.is_resolved]
        }
    
    def __str__(self):
        """String representation of the banking system."""
        stats = self.get_system_stats()
        return f"BankingSystem(users={stats['total_users']}, accounts={stats['total_accounts']}, transactions={stats['total_transactions']})"
