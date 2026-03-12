"""
Hash functions for bloom filter implementation.
"""

def hash_function_1(item, size):
    """
    First hash function using simple character sum.
    
    Args:
        item: The item to hash (converted to string)
        size: The size of the bloom filter array
        
    Returns:
        int: Hash value within the range [0, size)
    """
    item_str = str(item)
    hash_value = sum(ord(char) for char in item_str)
    return hash_value % size


def hash_function_2(item, size):
    """
    Second hash function using polynomial rolling hash.
    
    Args:
        item: The item to hash (converted to string)
        size: The size of the bloom filter array
        
    Returns:
        int: Hash value within the range [0, size)
    """
    item_str = str(item)
    hash_value = 0
    prime = 31
    
    for i, char in enumerate(item_str):
        hash_value += ord(char) * (prime ** i)
    
    return hash_value % size


def hash_function_3(item, size):
    """
    Third hash function using XOR and bit shifting.
    
    Args:
        item: The item to hash (converted to string)
        size: The size of the bloom filter array
        
    Returns:
        int: Hash value within the range [0, size)
    """
    item_str = str(item)
    hash_value = 0
    
    for i, char in enumerate(item_str):
        hash_value ^= (ord(char) << (i % 8))
    
    return abs(hash_value) % size


def get_hash_functions():
    """
    Get all available hash functions.
    
    Returns:
        list: List of hash functions
    """
    return [hash_function_1, hash_function_2, hash_function_3]
