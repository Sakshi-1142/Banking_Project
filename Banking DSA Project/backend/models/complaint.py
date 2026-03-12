"""
Complaint model for customer service.
"""

from datetime import datetime
from enum import Enum


class ComplaintStatus(Enum):
    """Enum for complaint status."""
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"
    CLOSED = "Closed"


class ComplaintPriority(Enum):
    """Enum for complaint priority."""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    URGENT = "Urgent"


class Complaint:
    """
    Represents a customer complaint in the banking system.
    """
    
    def __init__(self, complaint_id, user_id, subject, description, priority=ComplaintPriority.MEDIUM):
        """
        Initialize a new complaint.
        
        Args:
            complaint_id: Unique complaint identifier
            user_id: ID of the user who filed the complaint
            subject: Brief subject of the complaint
            description: Detailed description
            priority: Priority level (ComplaintPriority enum)
        """
        self.complaint_id = complaint_id
        self.user_id = user_id
        self.subject = subject
        self.description = description
        self.priority = priority if isinstance(priority, ComplaintPriority) else ComplaintPriority.MEDIUM
        self.status = ComplaintStatus.OPEN
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.resolved_at = None
        self.resolution = None
        self.assigned_to = None
    
    def update_status(self, new_status):
        """
        Update the complaint status.
        
        Args:
            new_status: New status (ComplaintStatus enum)
        """
        self.status = new_status if isinstance(new_status, ComplaintStatus) else self.status
        self.updated_at = datetime.now()
    
    def assign_to(self, agent_id):
        """
        Assign the complaint to an agent.
        
        Args:
            agent_id: ID of the agent to assign to
        """
        self.assigned_to = agent_id
        self.status = ComplaintStatus.IN_PROGRESS
        self.updated_at = datetime.now()
    
    def resolve(self, resolution):
        """
        Resolve the complaint.
        
        Args:
            resolution: Resolution description
        """
        self.resolution = resolution
        self.status = ComplaintStatus.RESOLVED
        self.resolved_at = datetime.now()
        self.updated_at = datetime.now()
    
    def close(self):
        """Close the complaint."""
        self.status = ComplaintStatus.CLOSED
        self.updated_at = datetime.now()
    
    def to_dict(self):
        """
        Convert complaint to dictionary representation.
        
        Returns:
            dict: Complaint data as dictionary
        """
        return {
            'complaint_id': self.complaint_id,
            'user_id': self.user_id,
            'subject': self.subject,
            'description': self.description,
            'priority': self.priority.value,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None,
            'resolution': self.resolution,
            'assigned_to': self.assigned_to
        }
    
    def __str__(self):
        """String representation of the complaint."""
        return f"Complaint({self.complaint_id}, {self.subject}, {self.status.value})"
    
    def __repr__(self):
        """Detailed representation of the complaint."""
        return f"Complaint(id={self.complaint_id}, priority={self.priority.value}, status={self.status.value})"
