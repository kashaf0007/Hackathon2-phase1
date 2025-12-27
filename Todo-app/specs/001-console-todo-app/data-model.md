# Data Model: Python In-Memory Console Todo Application

**Feature**: 001-console-todo-app
**Date**: 2025-12-22
**Source**: spec.md Key Entities section

---

## Entities

### Task

Represents a single todo item in the application.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| id | int | Yes | Auto-generated | Unique numeric identifier, immutable after creation |
| title | str | Yes | - | Non-empty text describing the task |
| description | str | No | "" | Optional additional details |
| completed | bool | Yes | False | Task completion status |

**Validation Rules**:
- `id`: Positive integer, auto-assigned by system, never reused within session
- `title`: Must be non-empty after whitespace trimming
- `description`: Any string allowed, empty string if not provided
- `completed`: Boolean, represents "Complete" (True) or "Incomplete" (False)

**State Transitions**:
```
[Created] --> completed=False ("Incomplete")
    |
    v
[Toggle] <--> completed=True ("Complete")
```

**Implementation Notes**:
- Use Python `@dataclass` decorator for clean definition
- Immutable ID - only title, description, completed can change
- ID assignment handled by TaskService, not Task itself

---

### TaskService (In-Memory Storage)

Manages the collection of Task entities.

| Component | Type | Description |
|-----------|------|-------------|
| tasks | List[Task] | In-memory storage of all tasks |
| next_id | int | Counter for ID generation (starts at 1) |

**Operations**:

| Method | Input | Output | Description |
|--------|-------|--------|-------------|
| add_task | title: str, description: str = "" | Task | Create and store new task |
| get_all_tasks | - | List[Task] | Return all tasks |
| get_task | id: int | Task \| None | Find task by ID |
| update_task | id: int, title: str, description: str | bool | Update task, return success |
| delete_task | id: int | bool | Remove task, return success |
| toggle_status | id: int | bool | Toggle completed flag, return success |

**Invariants**:
- `next_id` always increases (never decrements on delete)
- All IDs in `tasks` list are unique
- Task order is preserved (insertion order)

---

## Entity Relationships

```
┌─────────────────────────────────────────┐
│              TaskService                │
│  ┌────────────────────────────────────┐ │
│  │  tasks: List[Task]                 │ │
│  │  ┌──────┐ ┌──────┐ ┌──────┐       │ │
│  │  │Task 1│ │Task 2│ │Task n│ ...   │ │
│  │  └──────┘ └──────┘ └──────┘       │ │
│  └────────────────────────────────────┘ │
│  next_id: int                           │
└─────────────────────────────────────────┘
```

**Cardinality**:
- TaskService : Task = 1 : 0..*
- One TaskService instance contains zero or more Tasks

---

## Display Format

When displaying tasks (View Tasks operation):

```
ID: {id} | Title: {title} | Status: {status}
Description: {description}
---
```

Where:
- `status` = "Complete" if completed=True, else "Incomplete"
- Description line omitted if empty

**Example Output**:
```
ID: 1 | Title: Buy groceries | Status: Incomplete
Description: Milk, eggs, bread
---
ID: 2 | Title: Call doctor | Status: Complete
---
```

---

## Error Conditions

| Condition | Trigger | Response |
|-----------|---------|----------|
| Empty title | title.strip() == "" | Reject with "Task title cannot be empty" |
| Task not found | get_task(id) returns None | Return "Task not found" |
| Invalid ID format | Non-numeric input | Return "Invalid ID format" |
| Negative ID | id < 1 | Return "Invalid ID" |

---

## Python Type Definitions

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    completed: bool = False
```

**Note**: This is a reference definition. Actual implementation in `src/models.py`.
