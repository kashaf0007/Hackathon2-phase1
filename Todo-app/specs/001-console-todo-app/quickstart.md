# Quickstart Guide: Python In-Memory Console Todo Application

**Feature**: 001-console-todo-app
**Date**: 2025-12-22

---

## Prerequisites

- Python 3.13+
- UV runtime installed

---

## Project Setup

### 1. Initialize Project Structure

```bash
# Create source directory
mkdir -p src

# Create empty Python files
touch src/__init__.py
touch src/main.py
touch src/models.py
touch src/services.py
touch src/ui.py
```

### 2. File Structure

After setup, the source directory should look like:

```
src/
├── __init__.py    # Package marker (empty)
├── main.py        # Entry point
├── models.py      # Task data model
├── services.py    # TaskService business logic
└── ui.py          # Console UI
```

---

## Implementation Order

Follow this sequence to implement the application:

### Step 1: models.py

Create the Task dataclass:

```python
from dataclasses import dataclass

@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    completed: bool = False
```

### Step 2: services.py

Implement TaskService with:
- In-memory task list
- ID counter
- CRUD methods
- Toggle status method

### Step 3: ui.py

Implement ConsoleUI with:
- Menu display
- Input handlers
- Result/error display
- Main loop

### Step 4: main.py

Wire components together:

```python
from services import TaskService
from ui import ConsoleUI

def main():
    service = TaskService()
    ui = ConsoleUI(service)
    ui.run()

if __name__ == "__main__":
    main()
```

---

## Running the Application

### With UV

```bash
uv run python src/main.py
```

### With Python directly

```bash
python src/main.py
```

---

## Expected Console Output

### Main Menu

```
=== Todo Application ===
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Toggle Status
6. Exit

Enter choice:
```

### Adding a Task

```
Enter choice: 1
Enter task title: Buy groceries
Enter description (optional): Milk, eggs, bread
Task added successfully! ID: 1
```

### Viewing Tasks

```
Enter choice: 2

=== All Tasks ===
ID: 1 | Title: Buy groceries | Status: Incomplete
Description: Milk, eggs, bread
---
```

### Toggling Status

```
Enter choice: 5
Enter task ID: 1
Task status toggled to: Complete
```

### Exiting

```
Enter choice: 6
Goodbye!
```

---

## Testing Checklist

After implementation, verify these scenarios:

- [ ] Add task with title only
- [ ] Add task with title and description
- [ ] Reject empty title
- [ ] View tasks when empty (shows message)
- [ ] View tasks when populated
- [ ] Update existing task
- [ ] Update non-existent task (shows error)
- [ ] Delete existing task
- [ ] Delete non-existent task (shows error)
- [ ] Toggle status Incomplete -> Complete
- [ ] Toggle status Complete -> Incomplete
- [ ] Toggle non-existent task (shows error)
- [ ] Invalid menu input handling
- [ ] Invalid ID input handling
- [ ] Exit application

---

## Common Issues

### Issue: ModuleNotFoundError

**Cause**: Running from wrong directory

**Fix**: Run from project root:
```bash
cd /path/to/Todo-app
python src/main.py
```

### Issue: Python version error

**Cause**: Python < 3.13

**Fix**: Use UV to ensure correct version:
```bash
uv run python src/main.py
```

---

## Development Notes

- **No external dependencies** - Standard library only
- **No persistence** - Data lost on exit (by design)
- **Single session** - No multi-user support
- **Claude-only code** - All code generated via Claude Code
