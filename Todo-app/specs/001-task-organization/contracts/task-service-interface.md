# TaskService Interface Contract

**Feature**: 001-task-organization
**Date**: 2025-12-24
**Module**: `services.py` (TaskService class)

## Overview

This contract defines the public API for `TaskService`, including all new methods for task organization (search, filter, sort). All methods maintain in-memory storage semantics and follow the existing patterns.

## Existing Methods (Unchanged Signature)

### add_task

**Updated Signature**:
```python
def add_task(
    self,
    title: str,
    description: str = "",
    priority: str = "Medium",
    tags: List[str] | None = None,
    due_date: datetime | None = None
) -> Task
```

**Behavior**:
- Validates `title` is non-empty after strip
- Validates `priority` is one of: "High", "Medium", "Low"
- Defaults `tags` to empty list if `None`
- Auto-increments `_next_id` and assigns to task
- Appends task to `self.tasks`
- Returns the created `Task`

**Raises**:
- `ValueError`: If `title` is empty or `priority` is invalid

**Example**:
```python
task = service.add_task(
    title="Complete report",
    description="Submit quarterly financial analysis",
    priority="High",
    tags=["work", "finance"],
    due_date=datetime(2025, 12, 31)
)
```

---

### update_task

**Updated Signature**:
```python
def update_task(
    self,
    task_id: int,
    title: str | None = None,
    description: str | None = None,
    priority: str | None = None,
    tags: List[str] | None = None,
    due_date: datetime | None = None
) -> bool
```

**Behavior**:
- Finds task by `task_id`
- Updates only provided fields (None = skip field)
- Validates `title` if provided
- Validates `priority` if provided
- Replaces `tags` list entirely if provided
- Sets `due_date` to `None` if explicitly provided as `None`
- Returns `True` on success, `False` if task not found

**Raises**:
- `ValueError`: If `title` is empty or `priority` is invalid

**Example**:
```python
service.update_task(
    task_id=1,
    priority="Low",
    tags=["personal"]
)
```

---

## New Methods

### search_tasks

**Signature**:
```python
def search_tasks(self, keyword: str) -> List[Task]
```

**Behavior**:
- Performs case-insensitive substring search
- Matches `keyword` in either `task.title` or `task.description`
- Empty `keyword` returns all tasks
- Returns matching tasks in original order (insertion order)

**Time Complexity**: O(n) where n = total tasks

**Edge Cases**:
- Empty keyword: Return all tasks
- No matches: Return empty list
- Case-insensitive: "report" matches "Report", "REPORT"

**Example**:
```python
results = service.search_tasks("report")
# Returns tasks where title or description contains "report" (any case)
```

---

### filter_tasks

**Signature**:
```python
def filter_tasks(
    self,
    status: bool | None = None,
    priority: str | None = None,
    tags: List[str] | None = None
) -> List[Task]
```

**Behavior**:
- Filters tasks by all provided criteria (AND logic)
- `status`: Filter by `completed` field (True = completed, False = incomplete)
- `priority`: Filter by exact priority match
- `tags`: Filter by ANY tag match (OR logic within tags list)
- All parameters optional: `None` = no filter on that dimension
- Returns filtered tasks in original order

**Time Complexity**: O(n) where n = total tasks

**Edge Cases**:
- All `None`: Return all tasks
- No matches: Return empty list
- Conflicting filters: Return empty list (e.g., status=True and status=False)

**Example**:
```python
# High priority incomplete tasks
results = service.filter_tasks(status=False, priority="High")

# Tasks with "work" or "finance" tags
results = service.filter_tasks(tags=["work", "finance"])

# Completed tasks with "urgent" tag
results = service.filter_tasks(status=True, tags=["urgent"])
```

---

### sort_tasks

**Signature**:
```python
def sort_tasks(
    self,
    by: str = "due_date",
    order: str = "asc"
) -> List[Task]
```

**Behavior**:
- Sorts tasks without modifying original `self.tasks`
- Returns new sorted list
- `by` options:
  - `"due_date"`: Sort by `due_date`
  - `"priority"`: Sort by priority (High > Medium > Low)
  - `"title"`: Sort by `title` alphabetically (case-insensitive)
- `order` options:
  - `"asc"`: Ascending order
  - `"desc"`: Descending order
- `None` due dates placed at end for `"due_date"` sort

**Time Complexity**: O(n log n) using Python Timsort

**Priority Ordering** (for `"by=priority"`):
- High = 2, Medium = 1, Low = 0
- Ascending: Low → Medium → High
- Descending: High → Medium → Low

**Edge Cases**:
- Invalid `by` or `order`: Raise `ValueError`
- Tasks without due dates: Placed at end
- Empty task list: Return empty list

**Example**:
```python
# Earliest due date first
results = service.sort_tasks(by="due_date", order="asc")

# Highest priority first
results = service.sort_tasks(by="priority", order="desc")

# Alphabetically by title
results = service.sort_tasks(by="title", order="asc")
```

---

## Unchanged Methods (No Signature Change)

### get_all_tasks
```python
def get_all_tasks(self) -> List[Task]
```
Returns all tasks in insertion order.

### get_task
```python
def get_task(self, task_id: int) -> Task | None
```
Returns task by ID or `None` if not found.

### toggle_status
```python
def toggle_status(self, task_id: int) -> bool
```
Toggles `completed` status, returns `True` on success.

### delete_task
```python
def delete_task(self, task_id: int) -> bool
```
Removes task, returns `True` on success. Does not reuse IDs.

---

## Error Handling

All methods follow consistent error handling patterns:

| Error Type | Raised When | Recovery |
|------------|--------------|----------|
| `ValueError` | Invalid priority value | Catch and display user-friendly message |
| `ValueError` | Empty title | Catch and display error |
| `ValueError` | Invalid `by`/`order` in sort_tasks | Catch and display valid options |
| `bool False` return | Task not found (get/update/delete) | Display "Task not found" message |

---

## Thread Safety

**Not thread-safe**: Single-user, single-session design per constitution.

---

## Performance Requirements

| Operation | Max Tasks | Target Latency |
|-----------|-----------|-----------------|
| `search_tasks` | 1,000 | <5 seconds |
| `filter_tasks` | 1,000 | <3 seconds |
| `sort_tasks` | 1,000 | <3 seconds |
| `add_task` | N/A | <100ms |
| `update_task` | N/A | <100ms |
