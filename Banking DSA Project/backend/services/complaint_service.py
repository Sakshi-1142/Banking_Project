"""
Complaint service for customer service management.
"""

from backend.models.complaint import Complaint, ComplaintStatus, ComplaintPriority


class ComplaintService:
    """
    Service for handling customer complaints.
    """
    
    def __init__(self, banking_system):
        """
        Initialize the complaint service.
        
        Args:
            banking_system: Reference to the main banking system
        """
        self.banking_system = banking_system
        self.complaints = {}  # complaint_id -> Complaint
        self._next_complaint_id = 1
    
    def create_complaint(self, user_id, subject, description, priority=ComplaintPriority.MEDIUM):
        """
        Create a new complaint.
        
        Args:
            user_id: User ID
            subject: Brief subject
            description: Detailed description
            priority: Priority level (ComplaintPriority enum or string)
            
        Returns:
            tuple: (success: bool, message: str, complaint: Complaint or None)
        """
        # Verify user exists
        user = self.banking_system.auth_service.get_user_by_id(user_id)
        if not user:
            return False, "User not found", None
        
        # Convert string to ComplaintPriority if needed
        if isinstance(priority, str):
            try:
                priority = ComplaintPriority[priority.upper()]
            except KeyError:
                priority = ComplaintPriority.MEDIUM
        
        # Create complaint
        complaint_id = f"C{self._next_complaint_id:06d}"
        self._next_complaint_id += 1
        
        complaint = Complaint(complaint_id, user_id, subject, description, priority)
        
        # Store complaint
        self.complaints[complaint_id] = complaint
        
        return True, "Complaint created successfully", complaint
    
    def get_complaint(self, complaint_id):
        """
        Get a complaint by ID.
        
        Args:
            complaint_id: Complaint ID
            
        Returns:
            Complaint: Complaint object or None
        """
        return self.complaints.get(complaint_id)
    
    def get_user_complaints(self, user_id):
        """
        Get all complaints for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            list: List of Complaint objects
        """
        return [c for c in self.complaints.values() if c.user_id == user_id]
    
    def update_complaint_status(self, complaint_id, new_status):
        """
        Update the status of a complaint.
        
        Args:
            complaint_id: Complaint ID
            new_status: New status (ComplaintStatus enum or string)
            
        Returns:
            tuple: (success: bool, message: str)
        """
        complaint = self.get_complaint(complaint_id)
        if not complaint:
            return False, "Complaint not found"
        
        # Convert string to ComplaintStatus if needed
        if isinstance(new_status, str):
            try:
                new_status = ComplaintStatus[new_status.upper().replace(" ", "_")]
            except KeyError:
                return False, "Invalid status"
        
        complaint.update_status(new_status)
        return True, "Complaint status updated"
    
    def assign_complaint(self, complaint_id, agent_id):
        """
        Assign a complaint to an agent.
        
        Args:
            complaint_id: Complaint ID
            agent_id: Agent ID
            
        Returns:
            tuple: (success: bool, message: str)
        """
        complaint = self.get_complaint(complaint_id)
        if not complaint:
            return False, "Complaint not found"
        
        complaint.assign_to(agent_id)
        return True, "Complaint assigned successfully"
    
    def resolve_complaint(self, complaint_id, resolution):
        """
        Resolve a complaint.
        
        Args:
            complaint_id: Complaint ID
            resolution: Resolution description
            
        Returns:
            tuple: (success: bool, message: str)
        """
        complaint = self.get_complaint(complaint_id)
        if not complaint:
            return False, "Complaint not found"
        
        complaint.resolve(resolution)
        return True, "Complaint resolved successfully"
    
    def close_complaint(self, complaint_id):
        """
        Close a complaint.
        
        Args:
            complaint_id: Complaint ID
            
        Returns:
            tuple: (success: bool, message: str)
        """
        complaint = self.get_complaint(complaint_id)
        if not complaint:
            return False, "Complaint not found"
        
        complaint.close()
        return True, "Complaint closed successfully"
    
    def get_all_complaints(self):
        """
        Get all complaints.
        
        Returns:
            list: List of all complaints
        """
        return list(self.complaints.values())
    
    def get_open_complaints(self):
        """
        Get all open complaints.
        
        Returns:
            list: List of open complaints
        """
        return [c for c in self.complaints.values() if c.status == ComplaintStatus.OPEN]
    
    def get_complaints_by_priority(self, priority):
        """
        Get complaints by priority.
        
        Args:
            priority: Priority level (ComplaintPriority enum or string)
            
        Returns:
            list: List of complaints with the specified priority
        """
        if isinstance(priority, str):
            try:
                priority = ComplaintPriority[priority.upper()]
            except KeyError:
                return []
        
        return [c for c in self.complaints.values() if c.priority == priority]
