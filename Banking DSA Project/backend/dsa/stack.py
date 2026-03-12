"""
Stack implementation for operation history (undo/redo functionality).
"""

class Stack:
    """
    A stack data structure implementation using a list.
    Used for tracking operation history to enable undo/redo functionality.
    """
    
    def __init__(self):
        """Initialize an empty stack."""
        self._items = []
    
    def push(self, item):
        """
        Add an item to the top of the stack.
        
        Args:
            item: The item to add to the stack
        """
        self._items.append(item)
    
    def pop(self):
        """
        Remove and return the top item from the stack.
        
        Returns:
            The top item from the stack
            
        Raises:
            IndexError: If the stack is empty
        """
        if self.is_empty():
            raise IndexError("Cannot pop from an empty stack")
        return self._items.pop()
    
    def peek(self):
        """
        Return the top item without removing it.
        
        Returns:
            The top item from the stack
            
        Raises:
            IndexError: If the stack is empty
        """
        if self.is_empty():
            raise IndexError("Cannot peek at an empty stack")
        return self._items[-1]
    
    def is_empty(self):
        """
        Check if the stack is empty.
        
        Returns:
            bool: True if stack is empty, False otherwise
        """
        return len(self._items) == 0
    
    def size(self):
        """
        Get the number of items in the stack.
        
        Returns:
            int: Number of items in the stack
        """
        return len(self._items)
    
    def clear(self):
        """Clear all items from the stack."""
        self._items = []
    
    def __str__(self):
        """String representation of the stack."""
        return f"Stack({self._items})"
    
    def __repr__(self):
        """Detailed representation of the stack."""
        return f"Stack(size={self.size()}, items={self._items})"
