"""Business logic for Todo Application."""

from datetime import datetime
from typing import List

from models import Task, VALID_PRIORITIES


# Priority ordering for sort
PRIORITY_ORDER = {"High": 2, "Medium": 1, "Low": 0}


class TaskService:
    """Manages the collection of Task entities in memory.

    Attributes:
        tasks: In-memory storage of all tasks.
        _next_id: Counter for ID generation (starts at 1).
    """

    def __init__(self) -> None:
        """Initialize TaskService with empty task list."""
        self.tasks: list[Task] = []
        self._next_id: int = 1

    def add_task(
        self,
        title: str,
        description: str = "",
        priority: str = "Medium",
        tags: List[str] | None = None,
        due_date: datetime | None = None
    ) -> Task:
        """Create and store a new task.

        Args:
            title: Non-empty string after stripping whitespace.
            description: Optional additional details (default: "").
            priority: Priority level (High/Medium/Low, default: "Medium").
            tags: List of user-defined category labels (default: []).
            due_date: Optional due date/time for the task.

        Returns:
            Task: The newly created task with assigned ID.

        Raises:
            ValueError: If title is empty or whitespace-only, or priority is invalid.
        """
        # Validate title is non-empty after stripping
        stripped_title = title.strip()
        if not stripped_title:
            raise ValueError("Task title cannot be empty")

        # Default tags to empty list if None
        if tags is None:
            tags = []

        # Create task with auto-incremented ID
        task = Task(
            id=self._next_id,
            title=stripped_title,
            description=description.strip(),
            completed=False,
            priority=priority,
            tags=tags,
            due_date=due_date
        )

        # Store and increment ID counter
        self.tasks.append(task)
        self._next_id += 1

        return task

    def get_all_tasks(self) -> list[Task]:
        """Return all tasks in the store.

        Returns:
            list[Task]: All tasks (may be empty). Order preserved (insertion order).
        """
        return self.tasks

    def get_task(self, task_id: int) -> Task | None:
        """Find task by ID.

        Args:
            task_id: Positive integer ID.

        Returns:
            Task: If found.
            None: If not found.
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def toggle_status(self, task_id: int) -> bool:
        """Toggle task between Complete and Incomplete.

        Args:
            task_id: ID of task to toggle.

        Returns:
            bool: True if toggled, False if not found.
        """
        task = self.get_task(task_id)
        if task is None:
            return False

        task.completed = not task.completed
        return True

    def update_task(
        self,
        task_id: int,
        title: str,
        description: str,
        priority: str | None = None,
        tags: List[str] | None = None,
        due_date: datetime | None = None
    ) -> bool:
        """Update an existing task.

        Args:
            task_id: ID of task to update.
            title: New title (must be non-empty).
            description: New description (may be empty).
            priority: New priority (High/Medium/Low), optional.
            tags: New tags list (replaces existing), optional.
            due_date: New due date, optional.

        Returns:
            bool: True if successful, False if task not found.

        Raises:
            ValueError: If title is empty or whitespace-only, or priority is invalid.
        """
        # Validate title first
        stripped_title = title.strip()
        if not stripped_title:
            raise ValueError("Task title cannot be empty")

        task = self.get_task(task_id)
        if task is None:
            return False

        task.title = stripped_title
        task.description = description.strip()
        if priority is not None:
            if priority not in VALID_PRIORITIES:
                raise ValueError(f"Priority must be one of: {sorted(VALID_PRIORITIES)}")
            task.priority = priority
        if tags is not None:
            task.tags = tags
        if due_date is not None:
            task.due_date = due_date
        return True

    def delete_task(self, task_id: int) -> bool:
        """Remove a task by ID.

        Args:
            task_id: ID of task to delete.

        Returns:
            bool: True if deleted, False if not found.

        Note:
            next_id is NOT decremented (IDs are never reused).
        """
        task = self.get_task(task_id)
        if task is None:
            return False

        self.tasks.remove(task)
        return True

    def search_tasks(self, keyword: str) -> List[Task]:
        """Search tasks by keyword in title or description.

        Args:
            keyword: Search term (case-insensitive).

        Returns:
            List[Task]: Matching tasks in original order.
        """
        if not keyword:
            return self.tasks.copy()

        keyword_lower = keyword.lower()
        results = []
        for task in self.tasks:
            if keyword_lower in task.title.lower() or keyword_lower in task.description.lower():
                results.append(task)
        return results

    def filter_tasks(
        self,
        status: bool | None = None,
        priority: str | None = None,
        tags: List[str] | None = None
    ) -> List[Task]:
        """Filter tasks by criteria (AND logic for all provided criteria).

        Args:
            status: Filter by completed field (True = completed, False = incomplete).
            priority: Filter by exact priority match.
            tags: Filter by ANY tag match (OR logic within tags list).

        Returns:
            List[Task]: Filtered tasks in original order.
        """
        results = []
        for task in self.tasks:
            # Status filter
            if status is not None and task.completed != status:
                continue

            # Priority filter
            if priority is not None and task.priority != priority:
                continue

            # Tags filter (OR logic - task has ANY of the specified tags)
            if tags is not None and len(tags) > 0:
                if not any(tag in task.tags for tag in tags):
                    continue

            results.append(task)
        return results

    def sort_tasks(
        self,
        by: str = "due_date",
        order: str = "asc"
    ) -> List[Task]:
        """Sort tasks by specified field.

        Args:
            by: Sort field ("due_date", "priority", "title").
            order: Sort order ("asc", "desc").

        Returns:
            List[Task]: Sorted tasks (new list, original unchanged).

        Raises:
            ValueError: If by or order is invalid.
        """
        valid_by = {"due_date", "priority", "title"}
        valid_order = {"asc", "desc"}

        if by not in valid_by:
            raise ValueError(f"Invalid sort field. Must be one of: {sorted(valid_by)}")
        if order not in valid_order:
            raise ValueError(f"Invalid sort order. Must be one of: {sorted(valid_order)}")

        reverse = order == "desc"

        if by == "due_date":
            # None values at end
            def sort_key(task: Task):
                if task.due_date is None:
                    return (1, datetime.max)
                return (0, task.due_date)
            return sorted(self.tasks, key=sort_key, reverse=reverse)

        elif by == "priority":
            def sort_key(task: Task):
                return PRIORITY_ORDER.get(task.priority, 0)
            return sorted(self.tasks, key=sort_key, reverse=reverse)

        elif by == "title":
            def sort_key(task: Task):
                return task.title.lower()
            return sorted(self.tasks, key=sort_key, reverse=reverse)

        return self.tasks.copy()
