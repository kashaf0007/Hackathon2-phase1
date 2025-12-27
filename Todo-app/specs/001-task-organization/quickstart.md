# Quick Start: Task Organization Enhancement

**Feature**: 001-task-organization
**Date**: 2025-12-24

## Overview

This guide provides quick examples for using the enhanced Todo application with task organization features including priorities, tags, due dates, search, filtering, and sorting.

## Prerequisites

- Python 3.13+
- UV runtime
- Feature branch: `001-task-organization`

## Installation

```bash
# Install dependencies
uv sync

# Run the application
uv run python main.py
```

## Quick Examples

### 1. Adding Tasks with Organization Fields

**Interactive CLI**:
```
=== Todo Application ===
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Toggle Status
6. Search Tasks
7. Filter Tasks
8. Sort Tasks
9. Exit

Enter choice: 1
Enter task title: Complete project report
Enter description (optional): Submit quarterly financial analysis
Enter priority (High/Medium/Low, default Medium): High
Enter tags (comma-separated, optional): work,finance,urgent
Enter due date (YYYY-MM-DD, optional): 2025-12-31
Task added successfully! ID: 1
```

### 2. Viewing Tasks with Enhanced Display

```
Enter choice: 2

=== All Tasks ===
ID: 1 | Title: Complete project report | Priority: High | Status: Incomplete
Due: 2025-12-31 | Tags: work, finance, urgent
Description: Submit quarterly financial analysis
---
ID: 2 | Title: Buy groceries | Priority: Medium | Status: Incomplete
Tags: personal, shopping
Description: Weekly grocery run
---
ID: 3 | Title: Read book | Priority: Low | Status: Complete
Description: Finish reading "Clean Code"
---
```

### 3. Searching Tasks

**Search by keyword**:
```
Enter choice: 6
Enter search keyword: report

=== 1 task found ===
ID: 1 | Title: Complete project report | Priority: High | Status: Incomplete
Due: 2025-12-31 | Tags: work, finance, urgent
Description: Submit quarterly financial analysis
---
```

**Case-insensitive search**:
```
Enter search keyword: REPORT
# Returns same results (case-insensitive)
```

### 4. Filtering Tasks

**Filter by status**:
```
Enter choice: 7
Filter by:
1. All tasks
2. Incomplete only
3. Complete only
4. High priority
5. Medium priority
6. Low priority
7. By tags
8. Multiple filters
Enter choice: 2

=== 2 incomplete tasks ===
[Shows only incomplete tasks]
```

**Filter by tags**:
```
Enter choice: 7
Filter by:
...
Enter choice: 7
Enter tags (comma-separated): work,finance

=== 2 tasks matching tags ===
[Shows tasks with 'work' or 'finance' tags]
```

**Multiple filters**:
```
Enter choice: 7
...
Enter choice: 8
Enter status (completed/incomplete, leave empty to skip): incomplete
Enter priority (High/Medium/Low, leave empty to skip): High
Enter tags (comma-separated, leave empty to skip): work,urgent

=== 1 task matching all filters ===
[Shows incomplete, High priority tasks with work or urgent tags]
```

### 5. Sorting Tasks

**Sort by due date**:
```
Enter choice: 8
Sort by:
1. Due date
2. Priority
3. Title (alphabetical)
Enter choice: 1
Sort order (asc/desc): asc

=== Tasks sorted by due date (ascending) ===
[Shows tasks from earliest to latest due date]
```

**Sort by priority (high first)**:
```
Enter choice: 8
Sort by:
...
Enter choice: 2
Sort order (asc/desc): desc

=== Tasks sorted by priority (descending) ===
[Shows tasks: High, Medium, Low]
```

### 6. Updating Tasks

**Update priority and tags**:
```
Enter choice: 3
Enter task ID: 1
Current title: Complete project report
Current description: Submit quarterly financial analysis
Current priority: High
Current tags: work, finance, urgent
Current due date: 2025-12-31
Enter new title (leave empty to keep current):
Enter new description (leave empty to keep current):
Enter new priority (High/Medium/Low, leave empty to keep current): Low
Enter new tags (comma-separated, leave empty to keep current): work,finance
Enter new due date (YYYY-MM-DD, leave empty to keep current):
Task updated successfully!
```

## Python API Examples

### Using TaskService Directly

```python
from services import TaskService
from datetime import datetime

# Create service
service = TaskService()

# Add task with all fields
task = service.add_task(
    title="Complete report",
    description="Submit quarterly analysis",
    priority="High",
    tags=["work", "urgent"],
    due_date=datetime(2025, 12, 31)
)

# Search tasks
results = service.search_tasks("report")

# Filter tasks
high_priority_incomplete = service.filter_tasks(
    status=False,
    priority="High"
)

# Sort tasks
sorted_by_due = service.sort_tasks(
    by="due_date",
    order="asc"
)
```

## Common Use Cases

### Use Case 1: Daily Task Planning

1. **Add today's tasks**:
   - Set due dates to today
   - Assign priorities (High for urgent, Medium for normal, Low for nice-to-have)
   - Add tags: "today", project names

2. **Filter for today**:
   ```
   Filter by: Multiple filters
   Tags: today
   Status: incomplete
   ```

3. **Sort by priority**:
   ```
   Sort by: Priority (descending)
   ```

### Use Case 2: Project Organization

1. **Add project tasks** with project tag:
   ```
   Add task: "Review requirements"
   Tags: project-x, research
   ```

2. **View project tasks**:
   ```
   Filter by: Tags
   Enter tags: project-x
   ```

### Use Case 3: Deadline Management

1. **Add tasks with due dates**

2. **View upcoming deadlines**:
   ```
   Sort by: Due date (ascending)
   ```

3. **Focus on urgent**:
   ```
   Filter by: Multiple filters
   Priority: High
   Sort by: Due date (ascending)
   ```

## Tips and Tricks

- **Default values**: Press Enter to use defaults (priority=Medium, no tags, no due date)
- **Multiple tags**: Separate tags with commas (e.g., "work,urgent,project-x")
- **Search**: Searches both title and description, case-insensitive
- **Filter multiple**: Use option 8 for combining filters (e.g., High priority + incomplete + work tag)
- **Sort without filtering**: Sort displays all tasks in specified order
- **Update**: Leave fields empty to keep current values

## Next Steps

- Read the full spec: `specs/001-task-organization/spec.md`
- Review API contracts: `specs/001-task-organization/contracts/`
- See data model: `specs/001-task-organization/data-model.md`
- Run tests: `uv run pytest tests/`

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Invalid priority value | Use exactly "High", "Medium", or "Low" (case-sensitive) |
| Date format error | Use YYYY-MM-DD format (e.g., 2025-12-31) |
| Empty search returns nothing | Search with empty keyword shows all tasks |
| Filter shows nothing | Check filter criteria don't conflict (e.g., complete + incomplete) |
| Sort not what expected | Verify `by` option and `order` (asc/desc) |
