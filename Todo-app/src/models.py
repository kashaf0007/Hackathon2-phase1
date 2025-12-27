"""Data models for Todo Application."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

VALID_PRIORITIES = {"High", "Medium", "Low"}


@dataclass
class Task:
    """Represents a single todo item.

    Attributes:
        id: Unique numeric identifier, immutable after creation.
        title: Non-empty text describing the task.
        description: Optional additional details.
        completed: Task completion status (False = Incomplete, True = Complete).
        priority: Priority level (High/Medium/Low), default Medium.
        tags: List of user-defined category labels, default empty.
        due_date: Optional due date/time for the task.
    """
    id: int
    title: str
    description: str = ""
    completed: bool = False
    priority: str = "Medium"
    tags: List[str] = field(default_factory=list)
    due_date: Optional[datetime] = None

    def __post_init__(self) -> None:
        """Validate fields after initialization."""
        # Validate title
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty")

        # Validate priority
        if self.priority not in VALID_PRIORITIES:
            raise ValueError(
                f"Priority must be one of: {sorted(VALID_PRIORITIES)}"
            )
