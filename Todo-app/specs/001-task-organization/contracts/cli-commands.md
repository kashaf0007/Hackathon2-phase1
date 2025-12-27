# CLI Commands Contract

**Feature**: 001-task-organization
**Date**: 2025-12-24
**Module**: `ui.py` (ConsoleUI class) and `main.py`

## Overview

This contract defines the CLI commands for the Todo application, including new commands for search, filter, and sort. The application uses an interactive menu-based interface with numbered options.

## Existing Commands (Enhanced)

### 1. Add Task (Option 1)

**Interactive Flow**:
```
Enter task title: <user input>
Enter description (optional): <user input or empty>
Enter priority (High/Medium/Low, default Medium): <user input or empty>
Enter tags (comma-separated, optional): <user input or empty>
Enter due date (YYYY-MM-DD, optional): <user input or empty>
```

**Behavior**:
- All prompts required, but description/priority/tags/due_date optional
- Default priority: "Medium" if user presses Enter
- Tags: Split by comma and strip whitespace
- Due date: Parse ISO 8601 format, validate if provided
- Validation: Show error and re-prompt on invalid input

**Example Session**:
```
Enter task title: Complete project report
Enter description (optional): Submit quarterly analysis
Enter priority (High/Medium/Low, default Medium): High
Enter tags (comma-separated, optional): work,finance,urgent
Enter due date (YYYY-MM-DD, optional): 2025-12-31
Task added successfully! ID: 1
```

**Error Handling**:
- Empty title: "Task title cannot be empty. Please try again."
- Invalid priority: "Invalid priority. Must be High, Medium, or Low."
- Invalid date: "Invalid date format. Use YYYY-MM-DD."

---

### 2. Update Task (Option 3)

**Interactive Flow**:
```
Enter task ID: <user input>
Current title: {current title}
Current description: {current description or (none)}
Current priority: {current priority}
Current tags: {current tags or (none)}
Current due date: {current date or (none)}
Enter new title (leave empty to keep current): <user input>
Enter new description (leave empty to keep current): <user input>
Enter new priority (High/Medium/Low, leave empty to keep current): <user input>
Enter new tags (comma-separated, leave empty to keep current): <user input>
Enter new due date (YYYY-MM-DD, leave empty to keep current): <user input>
```

**Behavior**:
- Task must exist, show error if not found
- Display current values for reference
- Empty input keeps current value (no change)
- Update only fields with non-empty input
- Validation on priority and date if provided

**Example Session**:
```
Enter task ID: 1
Current title: Complete project report
Current description: Submit quarterly analysis
Current priority: High
Current tags: work,finance,urgent
Current due date: 2025-12-31
Enter new title (leave empty to keep current):
Enter new description (leave empty to keep current): Update with latest figures
Enter new priority (High/Medium/Low, leave empty to keep current): Medium
Enter new tags (comma-separated, leave empty to keep current): work,finance
Enter new due date (YYYY-MM-DD, leave empty to keep current):
Task updated successfully!
```

**Error Handling**:
- Invalid ID: "Task not found"
- Empty title (if changing title): "Task title cannot be empty"
- Invalid priority: "Invalid priority. Must be High, Medium, or Low."

---

### 3. View Tasks (Option 2) - Enhanced Display

**New Display Format** (with table-like alignment):
```
=== All Tasks ===
ID: 1 | Title: Complete project report | Priority: High | Status: Incomplete
Due: 2025-12-31 | Tags: work, finance, urgent
Description: Submit quarterly analysis
---
ID: 2 | Title: Buy groceries | Priority: Medium | Status: Incomplete
Tags: personal, shopping
Description: Weekly grocery run
---
ID: 3 | Title: Read book | Priority: Low | Status: Complete
Description: Finish reading "Clean Code"
---
```

**Behavior**:
- Display tasks in current order (may be sorted/filtered)
- Show all fields: ID, title, priority, status, due_date, tags, description
- Due date only shown if set
- Tags only shown if non-empty
- Description only shown if non-empty

---

## New Commands

### 4. Search Tasks (New Option)

**Interactive Flow**:
```
Enter search keyword: <user input>
```

**Behavior**:
- Search case-insensitive in title and description
- Display matching tasks with enhanced format
- Show count of results
- If no results: "No tasks found matching '{keyword}'"
- If empty keyword: Show all tasks (same as View Tasks)

**Example Session**:
```
Enter search keyword: report
=== 1 task found ===
ID: 1 | Title: Complete project report | Priority: High | Status: Incomplete
Due: 2025-12-31 | Tags: work, finance, urgent
Description: Submit quarterly analysis
---
```

**Menu Position**: Option 6 (after Toggle Status, before Exit)

---

### 5. Filter Tasks (New Option)

**Interactive Flow**:
```
Filter by:
1. All tasks
2. Incomplete only
3. Complete only
4. High priority
5. Medium priority
6. Low priority
7. By tags
8. Multiple filters
Enter choice: <user input>
```

**Sub-flows**:

**Option 1-6**: Apply single filter, display results
```
Enter choice: 2
=== 2 incomplete tasks ===
[filtered task list]
```

**Option 7** (By tags):
```
Enter tags (comma-separated): work,finance
=== 3 tasks matching tags ===
[filtered task list]
```

**Option 8** (Multiple filters):
```
Enter status (completed/incomplete, leave empty to skip): incomplete
Enter priority (High/Medium/Low, leave empty to skip): High
Enter tags (comma-separated, leave empty to skip): work,urgent
=== 1 task matching all filters ===
[filtered task list]
```

**Behavior**:
- Display count of filtered tasks
- If no matches: "No tasks match the selected filters"
- Enhanced display format for results

**Menu Position**: Option 7 (after Search Tasks, before Exit)

---

### 6. Sort Tasks (New Option)

**Interactive Flow**:
```
Sort by:
1. Due date
2. Priority
3. Title (alphabetical)
Enter choice: <user input>
Sort order (asc/desc): <user input>
```

**Behavior**:
- Display sorted tasks with enhanced format
- Due date sort: None values at end
- Priority sort: High > Medium > Low for desc
- Title sort: Case-insensitive alphabetical

**Example Session**:
```
Sort by:
1. Due date
2. Priority
3. Title (alphabetical)
Enter choice: 1
Sort order (asc/desc): asc
=== Tasks sorted by due date (ascending) ===
[sorted task list]
```

**Menu Position**: Option 8 (after Filter Tasks, before Exit)

---

## Updated Main Menu

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
```

**Note**: Options 1-5 are existing (some enhanced), 6-8 are new.

---

## Enhanced Display Utility

### display_task Method (Updated)

**Signature**:
```python
def display_task(self, task: Task) -> None
```

**Display Logic**:
```python
status = "Complete" if task.completed else "Incomplete"

# Main line (always shown)
priority_str = f"Priority: {task.priority}"
print(f"ID: {task.id} | Title: {task.title} | {priority_str} | Status: {status}")

# Due date (if set)
if task.due_date:
    due_str = task.due_date.strftime("%Y-%m-%d")
    print(f"Due: {due_str}", end="")
    if task.tags:
        print(f" | Tags: {', '.join(task.tags)}")
    else:
        print()
# Tags only (if no due date)
elif task.tags:
    print(f"Tags: {', '.join(task.tags)}")

# Description (if set)
if task.description:
    print(f"Description: {task.description}")

print("---")
```

**Format Examples**:

**Full task**:
```
ID: 1 | Title: Complete project | Priority: High | Status: Incomplete
Due: 2025-12-31 | Tags: work, urgent
Description: Submit quarterly report
---
```

**Task without due date, with tags**:
```
ID: 2 | Title: Buy groceries | Priority: Medium | Status: Incomplete
Tags: personal, shopping
Description: Weekly grocery run
---
```

**Minimal task**:
```
ID: 3 | Title: Read book | Priority: Low | Status: Complete
Description: Finish reading "Clean Code"
---
```

---

## Input Validation Helpers

### get_priority Method

**Signature**:
```python
def get_priority(self, default: str = "Medium") -> str
```

**Behavior**:
- Prompt: "Enter priority (High/Medium/Low, default {default}): "
- Empty input: Return `default`
- Validate: Must be in ["High", "Medium", "Low"]
- Invalid: Show error and re-prompt

---

### get_tags Method

**Signature**:
```python
def get_tags() -> List[str]
```

**Behavior**:
- Prompt: "Enter tags (comma-separated, optional): "
- Empty input: Return empty list
- Split by comma, strip whitespace from each tag
- Return list of non-empty tags

---

### get_due_date Method

**Signature**:
```python
def get_due_date() -> datetime | None
```

**Behavior**:
- Prompt: "Enter due date (YYYY-MM-DD, optional): "
- Empty input: Return `None`
- Parse: ISO 8601 date format
- Invalid: Show error and re-prompt

---

## CLI Colors (Optional Enhancement)

For better UX, consider color coding:
- Priority High: Red
- Priority Medium: Yellow
- Priority Low: Green
- Complete: Green
- Incomplete: Yellow

**Note**: Using `colorama` or ANSI escape codes (stdlib on Unix, Windows 10+).

---

## Performance Requirements

All CLI commands must meet spec success criteria:
- Add Task: <10 seconds user input latency
- Search: <5 seconds for result display (with 1000 tasks)
- Filter: <3 seconds for result display (with 1000 tasks)
- Sort: <3 seconds for result display (with 1000 tasks)
- View: <3 seconds to display (with 1000 tasks)
