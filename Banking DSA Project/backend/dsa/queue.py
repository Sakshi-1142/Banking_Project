"""
Queue implementation for transaction processing.
"""

class Queue:
    """
    A queue data structure implementation using a list.
    Used for managing transaction processing in FIFO order.
    """
    
    def __init__(self):
        """Initialize an empty queue."""
        self._items = []
    
    def enqueue(self, item):
        """
        Add an item to the rear of the queue.
        
        Args:
            item: The item to add to the queue
        """
        self._items.append(item)
    
    def dequeue(self):
        """
        Remove and return the front item from the queue.
        
        Returns:
            The front item from the queue
            
        Raises:
            IndexError: If the queue is empty
        """
        if self.is_empty():
            raise IndexError("Cannot dequeue from an empty queue")
        return self._items.pop(0)
    
    def front(self):
        """
        Return the front item without removing it.
        
        Returns:
            The front item from the queue
            
        Raises:
            IndexError: If the queue is empty
        """
        if self.is_empty():
            raise IndexError("Cannot peek at an empty queue")
        return self._items[0]
    
    def is_empty(self):
        """
        Check if the queue is empty.
        
        Returns:
            bool: True if queue is empty, False otherwise
        """
        return len(self._items) == 0
    
    def size(self):
        """
        Get the number of items in the queue.
        
        Returns:
            int: Number of items in the queue
        """
        return len(self._items)
    
    def clear(self):
        """Clear all items from the queue."""
        self._items = []
    
    def get_all(self):
        """
        Get all items in the queue without removing them.
        
        Returns:
            list: All items in the queue
        """
        return self._items.copy()
    
    def __str__(self):
        """String representation of the queue."""
        return f"Queue({self._items})"
    
    def __repr__(self):
        """Detailed representation of the queue."""
        return f"Queue(size={self.size()}, items={self._items})"
