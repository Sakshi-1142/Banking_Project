"""
Search service using Trie for fast lookups.
"""

from backend.dsa.trie import Trie


class SearchService:
    """
    Service for searching users and accounts using Trie data structure.
    """
    
    def __init__(self, banking_system):
        """
        Initialize the search service.
        
        Args:
            banking_system: Reference to the main banking system
        """
        self.banking_system = banking_system
        self.user_trie = Trie()  # Search by username and full name
        self.account_trie = Trie()  # Search by account ID
    
    def add_user(self, user):
        """
        Add a user to the search index.
        
        Args:
            user: User object
        """
        # Index by username
        self.user_trie.insert(user.username, {
            'user_id': user.user_id,
            'username': user.username,
            'full_name': user.full_name,
            'type': 'username'
        })
        
        # Index by full name
        self.user_trie.insert(user.full_name, {
            'user_id': user.user_id,
            'username': user.username,
            'full_name': user.full_name,
            'type': 'full_name'
        })
    
    def add_account(self, account):
        """
        Add an account to the search index.
        
        Args:
            account: Account object
        """
        self.account_trie.insert(account.account_id, {
            'account_id': account.account_id,
            'user_id': account.user_id,
            'account_type': account.account_type.value
        })
    
    def search_users(self, query):
        """
        Search for users by username or full name.
        
        Args:
            query: Search query
            
        Returns:
            list: List of matching user data
        """
        if not query:
            return []
        
        results = self.user_trie.get_all_with_prefix(query)
        
        # Remove duplicates (same user might match on both username and full name)
        seen_user_ids = set()
        unique_results = []
        
        for word, data in results:
            if data and data['user_id'] not in seen_user_ids:
                seen_user_ids.add(data['user_id'])
                unique_results.append(data)
        
        return unique_results
    
    def search_accounts(self, query):
        """
        Search for accounts by account ID.
        
        Args:
            query: Search query
            
        Returns:
            list: List of matching account data
        """
        if not query:
            return []
        
        results = self.account_trie.get_all_with_prefix(query)
        return [data for word, data in results if data]
    
    def search_user_exact(self, username):
        """
        Search for an exact username match.
        
        Args:
            username: Username to search for
            
        Returns:
            dict: User data or None
        """
        return self.user_trie.get_data(username)
    
    def search_account_exact(self, account_id):
        """
        Search for an exact account ID match.
        
        Args:
            account_id: Account ID to search for
            
        Returns:
            dict: Account data or None
        """
        return self.account_trie.get_data(account_id)
    
    def autocomplete_users(self, prefix, limit=10):
        """
        Get autocomplete suggestions for users.
        
        Args:
            prefix: Prefix to search for
            limit: Maximum number of results
            
        Returns:
            list: List of autocomplete suggestions
        """
        results = self.search_users(prefix)
        return results[:limit]
    
    def autocomplete_accounts(self, prefix, limit=10):
        """
        Get autocomplete suggestions for accounts.
        
        Args:
            prefix: Prefix to search for
            limit: Maximum number of results
            
        Returns:
            list: List of autocomplete suggestions
        """
        results = self.search_accounts(prefix)
        return results[:limit]
    
    def remove_user(self, username):
        """
        Remove a user from the search index.
        
        Args:
            username: Username to remove
            
        Returns:
            bool: True if successful
        """
        return self.user_trie.delete(username)
    
    def remove_account(self, account_id):
        """
        Remove an account from the search index.
        
        Args:
            account_id: Account ID to remove
            
        Returns:
            bool: True if successful
        """
        return self.account_trie.delete(account_id)
    
    def clear_all(self):
        """Clear all search indices."""
        self.user_trie.clear()
        self.account_trie.clear()
