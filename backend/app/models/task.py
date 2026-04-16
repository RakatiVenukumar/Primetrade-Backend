"""
Task model for task management and CRUD operations.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core import Base


class Task(Base):
    """
    Task table for PrimeTrade.
    
    Fields:
    - id: Primary key
    - user_id: Foreign key referencing User (task owner)
    - title: Task title
    - description: Optional task description
    - completed: Boolean flag for task completion status
    - created_at: Task creation timestamp
    - updated_at: Last update timestamp
    """
    
    __tablename__ = "tasks"
    
    # ========================================================================
    # Columns
    # ========================================================================
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Owner of the task (foreign key to users.id)"
    )
    
    title = Column(
        String(255),
        nullable=False,
        index=True,
        comment="Task title"
    )
    
    description = Column(
        Text,
        nullable=True,
        comment="Optional task description"
    )
    
    completed = Column(
        Boolean,
        nullable=False,
        default=False,
        index=True,
        comment="Task completion status"
    )
    
    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        index=True,
        comment="Task creation timestamp (UTC)"
    )
    
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        comment="Last update timestamp (UTC)"
    )
    
    # ========================================================================
    # Relationships
    # ========================================================================
    
    user = relationship(
        "User",
        backref="tasks"
    )
    
    # ========================================================================
    # Methods
    # ========================================================================
    
    def __repr__(self) -> str:
        """String representation of Task."""
        return f"<Task(id={self.id}, title='{self.title}', completed={self.completed})>"
