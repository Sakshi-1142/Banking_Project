"""
Trie implementation for fast user and account search.
"""

class TrieNode:
    """A node in the Trie data structure."""
    
    def __init__(self):
        """Initialize a trie node."""
        self.children = {}
        self.is_end_of_word = False
        self.data = None  # Store associated data (e.g., user ID, account number)


class Trie:
    """
    A Trie (prefix tree) implementation for efficient string searching.
    Used for fast user and account search by name or prefix.
    """
    
    def __init__(self):
        """Initialize an empty trie."""
        self.root = TrieNode()
    
    def insert(self, word, data=None):
        """
        Insert a word into the trie.
        
        Args:
            word: The word to insert (case-insensitive)
            data: Optional data to associate with the word
        """
        word = word.lower()
        node = self.root
        
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        
        node.is_end_of_word = True
        node.data = data
    
    def search(self, word):
        """
        Search for an exact word in the trie.
        
        Args:
            word: The word to search for (case-insensitive)
            
        Returns:
            bool: True if word exists, False otherwise
        """
        word = word.lower()
        node = self._find_node(word)
        return node is not None and node.is_end_of_word
    
    def starts_with(self, prefix):
        """
        Check if any word in the trie starts with the given prefix.
        
        Args:
            prefix: The prefix to search for (case-insensitive)
            
        Returns:
            bool: True if prefix exists, False otherwise
        """
        prefix = prefix.lower()
        return self._find_node(prefix) is not None
    
    def get_data(self, word):
        """
        Get the data associated with a word.
        
        Args:
            word: The word to get data for (case-insensitive)
            
        Returns:
            The associated data, or None if word not found
        """
        word = word.lower()
        node = self._find_node(word)
        if node and node.is_end_of_word:
            return node.data
        return None
    
    def get_all_with_prefix(self, prefix):
        """
        Get all words (and their data) that start with the given prefix.
        
        Args:
            prefix: The prefix to search for (case-insensitive)
            
        Returns:
            list: List of tuples (word, data) matching the prefix
        """
        prefix = prefix.lower()
        results = []
        node = self._find_node(prefix)
        
        if node:
            self._collect_words(node, prefix, results)
        
        return results
    
    def _find_node(self, word):
        """
        Find the node corresponding to a word or prefix.
        
        Args:
            word: The word or prefix to find
            
        Returns:
            TrieNode: The node if found, None otherwise
        """
        node = self.root
        
        for char in word:
            if char not in node.children:
                return None
            node = node.children[char]
        
        return node
    
    def _collect_words(self, node, current_word, results):
        """
        Recursively collect all words from a given node.
        
        Args:
            node: The current node
            current_word: The word built so far
            results: List to append results to
        """
        if node.is_end_of_word:
            results.append((current_word, node.data))
        
        for char, child_node in node.children.items():
            self._collect_words(child_node, current_word + char, results)
    
    def delete(self, word):
        """
        Delete a word from the trie.
        
        Args:
            word: The word to delete (case-insensitive)
            
        Returns:
            bool: True if word was deleted, False if not found
        """
        word = word.lower()
        return self._delete_helper(self.root, word, 0)
    
    def _delete_helper(self, node, word, index):
        """
        Helper method for deleting a word.
        
        Args:
            node: Current node
            word: Word to delete
            index: Current character index
            
        Returns:
            bool: True if node should be deleted
        """
        if index == len(word):
            if not node.is_end_of_word:
                return False
            node.is_end_of_word = False
            node.data = None
            return len(node.children) == 0
        
        char = word[index]
        if char not in node.children:
            return False
        
        child_node = node.children[char]
        should_delete_child = self._delete_helper(child_node, word, index + 1)
        
        if should_delete_child:
            del node.children[char]
            return len(node.children) == 0 and not node.is_end_of_word
        
        return False
    
    def clear(self):
        """Clear all words from the trie."""
        self.root = TrieNode()
    
    def __str__(self):
        """String representation of the trie."""
        return f"Trie(root_children={len(self.root.children)})"
