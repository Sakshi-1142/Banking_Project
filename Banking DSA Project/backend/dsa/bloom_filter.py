"""
Bloom Filter implementation for fraud detection and duplicate checking.
"""

from .hash_functions import hash_function_1, hash_function_2, hash_function_3


class BloomFilter:
    """
    A Bloom Filter implementation for probabilistic membership testing.
    Used for fraud detection and duplicate transaction checking.
    
    False positives are possible, but false negatives are not.
    """
    
    def __init__(self, size=1000, hash_functions=None):
        """
        Initialize a bloom filter.
        
        Args:
            size: Size of the bit array (default: 1000)
            hash_functions: List of hash functions to use (default: uses 3 built-in functions)
        """
        self.size = size
        self.bit_array = [False] * size
        
        if hash_functions is None:
            self.hash_functions = [hash_function_1, hash_function_2, hash_function_3]
        else:
            self.hash_functions = hash_functions
    
    def add(self, item):
        """
        Add an item to the bloom filter.
        
        Args:
            item: The item to add (will be converted to string)
        """
        for hash_func in self.hash_functions:
            index = hash_func(item, self.size)
            self.bit_array[index] = True
    
    def contains(self, item):
        """
        Check if an item might be in the bloom filter.
        
        Args:
            item: The item to check (will be converted to string)
            
        Returns:
            bool: True if item might be in the set (possible false positive),
                  False if item is definitely not in the set
        """
        for hash_func in self.hash_functions:
            index = hash_func(item, self.size)
            if not self.bit_array[index]:
                return False
        return True
    
    def clear(self):
        """Clear all items from the bloom filter."""
        self.bit_array = [False] * self.size
    
    def get_fill_ratio(self):
        """
        Get the ratio of set bits in the bloom filter.
        
        Returns:
            float: Ratio of set bits (0.0 to 1.0)
        """
        set_bits = sum(self.bit_array)
        return set_bits / self.size
    
    def __str__(self):
        """String representation of the bloom filter."""
        fill_ratio = self.get_fill_ratio()
        return f"BloomFilter(size={self.size}, fill_ratio={fill_ratio:.2%})"
    
    def __repr__(self):
        """Detailed representation of the bloom filter."""
        return f"BloomFilter(size={self.size}, hash_functions={len(self.hash_functions)}, fill_ratio={self.get_fill_ratio():.2%})"
