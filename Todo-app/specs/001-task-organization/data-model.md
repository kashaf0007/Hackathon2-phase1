# Data Model: Task Organization Enhancement

**Feature**: 001-task-organization
**Date**: 2025-12-24
**Source**: Derived from `spec.md` FR-001 to FR-014

## Entity: Task

### Overview

The `Task` entity represents a single to-do item in the in-memory Todo application. This dataclass extends the existing base Task model with three new optional fields for organization: priority, tags, and due_date.

### Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `id` | `int` | Yes | N/A | Unique numeric identifier, immutable after creation |
| `title` | `str` | Yes | N/A | Non-empty text describing the task |
| `description` | `str` | No | `""` | Optional additional details |
| `completed` | `bool` | No | `False` | Task completion status (False = Incomplete, True = Complete) |
| `priority` | `str` | No | `"Medium"` | Priority level: "High", "Medium", or "Low" |
| `tags` | `list[str]` | No | `[]` | List of user-defined category labels |
| `due_date` | `datetime | None` | No | `None` | Optional due date/time for the task |

### Field Validation

#### Priority

**Valid Values**: "High", "Medium", "Low"
**Validation**: `priority` must be one of the three allowed values
**Default**: "Medium" if not provided

**Implementation**:
```python
VALID_PRIORITIES = {"High", "Medium", "Low"}

if priority not in VALID_PRIORITIES:
    raise ValueError(f"Priority must be one of: {sorted(VALID_PRIORITIES)}")
```

#### Tags

**Type**: `list[str]`
**Validation**: None - any string values accepted
**Empty List**: Valid (no tags assigned)
**Duplicates**: Allowed (not enforced as duplicates)

**Implementation**:
```python
# Tags stored as-is, no validation on content
tags = tags if tags is not None else []
```

#### Due Date

**Type**: `datetime | None`
**Validation**: Must be `datetime` or `None`
**Default**: `None` if not provided
**Parsing**: From CLI input, parse ISO 8601 format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)

**Implementation**:
```python
from datetime import datetime

# CLI parsing example
if due_date_str:
    due_date = datetime.fromisoformat(due_date_str)
else:
    due_date = None
```

### State Transitions

The Task entity is immutable after creation in the current architecture. Updates create a conceptual new state by modifying the dataclass fields in-place (Python dataclass mutable by default).

**No explicit state machine** - fields can be updated independently:

- `completed`: Can be toggled from `False` ↔ `True`
- `priority`: Can be changed among High/Medium/Low
- `tags`: Can be added/removed/replaced entirely
- `due_date`: Can be set or cleared (`None`)

### Relationships

**No relationships** - Tasks are standalone entities stored in a flat list in `TaskService`.

### Invariants

1. **ID Stability**: Once assigned, `id` never changes or is reused
2. **Title Non-Empty**: `title` after `strip()` must have length > 0
3. **Priority Enum**: `priority` must be one of High/Medium/Low
4. **Tags List**: `tags` is always a list (never `None`)
5. **Due Date Optional**: `due_date` may be `None` or `datetime`

### Python Dataclass Definition

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

VALID_PRIORITIES = {"High", "Medium", "Low"}

@dataclass
class Task:
    """Represents a single todo item with organization fields.

    Attributes:
        id: Unique numeric identifier, immutable after creation.
        title: Non-empty text describing the task.
        description: Optional additional details.
        completed: Task completion status.
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

        # Ensure tags is always a list
        if self.tags is None:
            self.tags = []
```

### Usage Examples

#### Creating Tasks

```python
from models import Task
from datetime import datetime

# Minimal task (all defaults)
task1 = Task(id=1, title="Basic task")
# priority="Medium", tags=[], due_date=None

# Task with priority
task2 = Task(
    id=2,
    title="Important task",
    priority="High"
)

# Full task
task3 = Task(
    id=3,
    title="Project deadline",
    description="Submit final report",
    priority="High",
    tags=["work", "urgent"],
    due_date=datetime(2025, 12, 31, 23, 59)
)

# Invalid priority raises ValueError
try:
    Task(id=4, title="Test", priority="Urgent")
except ValueError as e:
    print(e)  # "Priority must be one of: ['High', 'Low', 'Medium']"
```

#### Updating Tasks (via TaskService)

```python
# Update priority
task.priority = "Low"

# Add tags
task.tags.extend(["personal", "shopping"])

# Set due date
task.due_date = datetime(2025, 12, 25)

# Clear due date
task.due_date = None
```

### Sorting/Filtering Keys

**For Sort Operations**:
- `by='due_date'`: Sort by `due_date` field (None values last)
- `by='priority'`: Sort by custom ordering High > Medium > Low
- `by='title'`: Sort by `title` alphabetically (case-insensitive)

**For Filter Operations**:
- `status`: Filter by `completed` field (True/False)
- `priority`: Filter by `priority` field
- `tags`: Filter if task has ANY of specified tags

**For Search Operations**:
- Search `keyword` in both `title` and `description` fields (case-insensitive)

### Performance Considerations

- **Search**: Linear scan over all tasks - O(n)
- **Filter**: Linear scan - O(n)
- **Sort**: Python Timsort - O(n log n)

For MVP with ~1000 tasks, linear operations are acceptable. Consider indexing if scale increases beyond ~10,000 tasks.

### Migration Notes

**From Existing Tasks**:
- Existing tasks will have `priority="Medium"`, `tags=[]`, `due_date=None` when loaded
- No breaking changes to existing functionality
- Backward compatible with old code that ignores new fields
