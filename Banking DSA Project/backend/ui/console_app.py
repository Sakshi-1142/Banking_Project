"""
Console-based user interface for the banking system.
"""

from backend.core.banking_system import BankingSystem
from backend.core.data_initializer import DataInitializer
from backend.models.account import AccountType
from backend.models.complaint import ComplaintPriority


class ConsoleApp:
    """
    Console application for interacting with the banking system.
    """
    
    def __init__(self):
        """Initialize the console application."""
        self.banking_system = BankingSystem()
        self.running = False
    
    def run(self):
        """Run the console application."""
        self.running = True
        self.show_welcome()
        
        while self.running:
            self.show_main_menu()
    
    def show_welcome(self):
        """Display welcome message."""
        print("\n" + "=" * 60)
        print("   BANKING SYSTEM - DSA PROJECT")
        print("=" * 60)
        print("\nWelcome to the Banking System!")
        print("This system demonstrates various Data Structures:")
        print("  • Stack - Operation History (Undo/Redo)")
        print("  • Queue - Transaction Processing")
        print("  • Trie - Fast User/Account Search")
        print("  • Bloom Filter - Fraud Detection")
        print("=" * 60 + "\n")
    
    def show_main_menu(self):
        """Display main menu."""
        if not self.banking_system.auth_service.is_authenticated():
            self.show_guest_menu()
        else:
            self.show_user_menu()
    
    def show_guest_menu(self):
        """Display menu for non-authenticated users."""
        print("\n--- Main Menu ---")
        print("1. Login")
        print("2. Register")
        print("3. Initialize Sample Data")
        print("4. View System Statistics")
        print("5. Exit")
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == "1":
            self.login()
        elif choice == "2":
            self.register()
        elif choice == "3":
            self.initialize_sample_data()
        elif choice == "4":
            self.view_system_stats()
        elif choice == "5":
            self.exit_app()
        else:
            print("Invalid choice. Please try again.")
    
    def show_user_menu(self):
        """Display menu for authenticated users."""
        user = self.banking_system.auth_service.get_current_user()
        print(f"\n--- Welcome, {user.full_name}! ---")
        print("1. View Dashboard")
        print("2. View Accounts")
        print("3. Create Account")
        print("4. Make Transaction")
        print("5. Process Pending Transactions")
        print("6. Search Users")
        print("7. File Complaint")
        print("8. View My Complaints")
        print("9. View System Statistics")
        print("10. Logout")
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == "1":
            self.view_dashboard()
        elif choice == "2":
            self.view_accounts()
        elif choice == "3":
            self.create_account()
        elif choice == "4":
            self.make_transaction()
        elif choice == "5":
            self.process_transactions()
        elif choice == "6":
            self.search_users()
        elif choice == "7":
            self.file_complaint()
        elif choice == "8":
            self.view_my_complaints()
        elif choice == "9":
            self.view_system_stats()
        elif choice == "10":
            self.logout()
        else:
            print("Invalid choice. Please try again.")
    
    def login(self):
        """Handle user login."""
        print("\n--- Login ---")
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        
        success, message, user = self.banking_system.auth_service.login(username, password)
        print(f"\n{message}")
    
    def register(self):
        """Handle user registration."""
        print("\n--- Register ---")
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        email = input("Email: ").strip()
        full_name = input("Full Name: ").strip()
        phone = input("Phone (optional): ").strip() or None
        
        success, message, user = self.banking_system.auth_service.register(
            username, password, email, full_name, phone
        )
        print(f"\n{message}")
    
    def logout(self):
        """Handle user logout."""
        self.banking_system.auth_service.logout()
        print("\nLogged out successfully!")
    
    def view_dashboard(self):
        """Display user dashboard."""
        user = self.banking_system.auth_service.get_current_user()
        dashboard = self.banking_system.get_user_dashboard(user.user_id)
        
        print("\n" + "=" * 60)
        print("   DASHBOARD")
        print("=" * 60)
        print(f"\nUser: {dashboard['user']['full_name']}")
        print(f"Email: {dashboard['user']['email']}")
        print(f"Total Balance: ₹{dashboard['total_balance']:.2f}")
        print(f"\nAccounts: {len(dashboard['accounts'])}")
        print(f"Complaints: {len(dashboard['complaints'])}")
        print(f"Fraud Alerts: {len(dashboard['fraud_alerts'])}")
        print("=" * 60)
    
    def view_accounts(self):
        """Display user accounts."""
        user = self.banking_system.auth_service.get_current_user()
        accounts = self.banking_system.account_service.get_user_accounts(user.user_id)
        
        print("\n--- Your Accounts ---")
        if not accounts:
            print("No accounts found.")
        else:
            for acc in accounts:
                print(f"\n{acc.account_id} - {acc.account_type.value}")
                print(f"  Balance: ₹{acc.balance:.2f}")
                print(f"  Status: {acc.status.value}")
                print(f"  Transactions: {len(acc.transaction_history)}")
    
    def create_account(self):
        """Create a new account."""
        user = self.banking_system.auth_service.get_current_user()
        
        print("\n--- Create Account ---")
        print("Account Types:")
        print("1. Savings")
        print("2. Checking")
        print("3. Business")
        
        choice = input("Select account type: ").strip()
        type_map = {"1": "SAVINGS", "2": "CHECKING", "3": "BUSINESS"}
        
        if choice not in type_map:
            print("Invalid choice.")
            return
        
        initial_balance = input("Initial balance (default 0): ").strip()
        initial_balance = float(initial_balance) if initial_balance else 0.0
        
        success, message, account = self.banking_system.account_service.create_account(
            user.user_id, type_map[choice], initial_balance
        )
        print(f"\n{message}")
        if success:
            print(f"Account ID: {account.account_id}")
    
    def make_transaction(self):
        """Make a transaction."""
        print("\n--- Make Transaction ---")
        print("1. Deposit")
        print("2. Withdrawal")
        print("3. Transfer")
        
        choice = input("Select transaction type: ").strip()
        
        if choice == "1":
            self.make_deposit()
        elif choice == "2":
            self.make_withdrawal()
        elif choice == "3":
            self.make_transfer()
        else:
            print("Invalid choice.")
    
    def make_deposit(self):
        """Make a deposit."""
        account_id = input("Account ID: ").strip()
        amount = float(input("Amount: ").strip())
        description = input("Description (optional): ").strip()
        
        success, message, trans = self.banking_system.transaction_service.deposit(
            account_id, amount, description
        )
        print(f"\n{message}")
        if success:
            print(f"Transaction ID: {trans.transaction_id}")
    
    def make_withdrawal(self):
        """Make a withdrawal."""
        account_id = input("Account ID: ").strip()
        amount = float(input("Amount: ").strip())
        description = input("Description (optional): ").strip()
        
        success, message, trans = self.banking_system.transaction_service.withdraw(
            account_id, amount, description
        )
        print(f"\n{message}")
        if success:
            print(f"Transaction ID: {trans.transaction_id}")
    
    def make_transfer(self):
        """Make a transfer."""
        from_account = input("From Account ID: ").strip()
        to_account = input("To Account ID: ").strip()
        amount = float(input("Amount: ").strip())
        description = input("Description (optional): ").strip()
        
        success, message, trans = self.banking_system.transaction_service.transfer(
            from_account, to_account, amount, description
        )
        print(f"\n{message}")
        if success:
            print(f"Transaction ID: {trans.transaction_id}")
    
    def process_transactions(self):
        """Process pending transactions."""
        queue_size = self.banking_system.transaction_service.get_queue_size()
        print(f"\n--- Processing {queue_size} Pending Transactions ---")
        
        results = self.banking_system.process_pending_transactions()
        
        successful = sum(1 for r in results if r[0])
        print(f"\nProcessed: {len(results)} transactions")
        print(f"Successful: {successful}")
        print(f"Failed: {len(results) - successful}")
    
    def search_users(self):
        """Search for users."""
        query = input("\nEnter search query: ").strip()
        results = self.banking_system.search(query, 'users')
        
        print(f"\n--- Search Results ({len(results)} found) ---")
        for result in results:
            print(f"\n{result['username']} - {result['full_name']}")
            print(f"  User ID: {result['user_id']}")
    
    def file_complaint(self):
        """File a complaint."""
        user = self.banking_system.auth_service.get_current_user()
        
        print("\n--- File Complaint ---")
        subject = input("Subject: ").strip()
        description = input("Description: ").strip()
        
        print("\nPriority:")
        print("1. Low")
        print("2. Medium")
        print("3. High")
        print("4. Urgent")
        
        priority_choice = input("Select priority (default 2): ").strip() or "2"
        priority_map = {"1": "LOW", "2": "MEDIUM", "3": "HIGH", "4": "URGENT"}
        priority = priority_map.get(priority_choice, "MEDIUM")
        
        success, message, complaint = self.banking_system.complaint_service.create_complaint(
            user.user_id, subject, description, priority
        )
        print(f"\n{message}")
        if success:
            print(f"Complaint ID: {complaint.complaint_id}")
    
    def view_my_complaints(self):
        """View user's complaints."""
        user = self.banking_system.auth_service.get_current_user()
        complaints = self.banking_system.complaint_service.get_user_complaints(user.user_id)
        
        print("\n--- Your Complaints ---")
        if not complaints:
            print("No complaints found.")
        else:
            for comp in complaints:
                print(f"\n{comp.complaint_id} - {comp.subject}")
                print(f"  Status: {comp.status.value}")
                print(f"  Priority: {comp.priority.value}")
                print(f"  Created: {comp.created_at.strftime('%Y-%m-%d %H:%M')}")
    
    def view_system_stats(self):
        """Display system statistics."""
        stats = self.banking_system.get_system_stats()
        
        print("\n" + "=" * 60)
        print("   SYSTEM STATISTICS")
        print("=" * 60)
        print(f"\nUsers: {stats['total_users']}")
        print(f"Accounts: {stats['total_accounts']}")
        print(f"Transactions: {stats['total_transactions']}")
        print(f"Pending Transactions: {stats['pending_transactions']}")
        print(f"Complaints: {stats['total_complaints']}")
        print(f"Open Complaints: {stats['open_complaints']}")
        print(f"Fraud Records: {stats['total_fraud_records']}")
        print(f"Unresolved Fraud: {stats['unresolved_fraud']}")
        print("\nBloom Filter Statistics:")
        print(f"  Transaction Filter: {stats['bloom_filter_stats']['transaction_bloom_fill']:.2%} full")
        print(f"  Pattern Filter: {stats['bloom_filter_stats']['suspicious_patterns_fill']:.2%} full")
        print("=" * 60)
    
    def initialize_sample_data(self):
        """Initialize sample data."""
        print("\nInitializing sample data...")
        initializer = DataInitializer(self.banking_system)
        summary = initializer.initialize_sample_data()
        print("\nSample data initialized successfully!")
        print(f"You can now login with username 'john_doe' and password 'password123'")
    
    def exit_app(self):
        """Exit the application."""
        print("\nThank you for using the Banking System!")
        print("Goodbye!\n")
        self.running = False


if __name__ == "__main__":
    app = ConsoleApp()
    app.run()
