# Service Contracts: Python In-Memory Console Todo Application

**Feature**: 001-console-todo-app
**Date**: 2025-12-22
**Type**: Internal Function Contracts (Console Application)

---

## Overview

This document defines the function contracts for the TaskService class. Since this is a console application (not a web API), contracts are defined as Python function signatures with preconditions, postconditions, and error handling specifications.

---

## TaskService Contracts

### 1. add_task

**Purpose**: Create a new task and add it to the in-memory store.

```python
def add_task(self, title: str, description: str = "") -> Task:
    """
    Create and store a new task.

    Args:
        title: Non-empty string after stripping whitespace
        description: Optional additional details (default: "")

    Returns:
        Task: The newly created task with assigned ID

    Raises:
        ValueError: If title is empty or whitespace-only

    Preconditions:
        - title.strip() != ""

    Postconditions:
        - New Task exists in tasks list
        - Task.id is unique and positive
        - Task.completed == False
        - next_id incremented by 1
    """
```

**Mapping to Requirements**:
- FR-001: Allow users to add new tasks with required non-empty title
- FR-002: Assign unique ID
- FR-003: Default status "Incomplete"

---

### 2. get_all_tasks

**Purpose**: Retrieve all tasks for display.

```python
def get_all_tasks(self) -> list[Task]:
    """
    Return all tasks in the store.

    Returns:
        list[Task]: All tasks (may be empty)

    Preconditions:
        - None

    Postconditions:
        - Returns copy or reference to tasks list
        - Order preserved (insertion order)
        - No side effects on store
    """
```

**Mapping to Requirements**:
- FR-004: Display all tasks
- FR-005: Handle empty list case (UI responsibility to show message)

---

### 3. get_task

**Purpose**: Find a single task by ID.

```python
def get_task(self, task_id: int) -> Task | None:
    """
    Find task by ID.

    Args:
        task_id: Positive integer ID

    Returns:
        Task: If found
        None: If not found

    Preconditions:
        - task_id is an integer

    Postconditions:
        - Returns Task if ID exists
        - Returns None if ID not found
        - No side effects on store
    """
```

**Mapping to Requirements**:
- FR-009: Handle invalid/non-existent IDs gracefully

---

### 4. update_task

**Purpose**: Modify an existing task's title and/or description.

```python
def update_task(self, task_id: int, title: str, description: str) -> bool:
    """
    Update an existing task.

    Args:
        task_id: ID of task to update
        title: New title (must be non-empty)
        description: New description (may be empty)

    Returns:
        bool: True if successful, False if task not found

    Raises:
        ValueError: If title is empty or whitespace-only

    Preconditions:
        - task_id is positive integer
        - title.strip() != ""

    Postconditions:
        - If task found: title and description updated
        - If task not found: no changes made
        - Task.id and Task.completed unchanged
    """
```

**Mapping to Requirements**:
- FR-006: Allow updating title and description by ID
- FR-009: Handle non-existent IDs
- FR-010: Handle empty title input

---

### 5. delete_task

**Purpose**: Remove a task from the store.

```python
def delete_task(self, task_id: int) -> bool:
    """
    Remove a task by ID.

    Args:
        task_id: ID of task to delete

    Returns:
        bool: True if deleted, False if not found

    Preconditions:
        - task_id is positive integer

    Postconditions:
        - If task found: removed from tasks list
        - If task not found: no changes made
        - next_id NOT decremented (IDs never reused)
    """
```

**Mapping to Requirements**:
- FR-007: Allow deleting tasks by ID
- FR-009: Handle non-existent IDs

---

### 6. toggle_status

**Purpose**: Toggle a task's completion status.

```python
def toggle_status(self, task_id: int) -> bool:
    """
    Toggle task between Complete and Incomplete.

    Args:
        task_id: ID of task to toggle

    Returns:
        bool: True if toggled, False if not found

    Preconditions:
        - task_id is positive integer

    Postconditions:
        - If task found: completed = not completed
        - If task not found: no changes made
    """
```

**Mapping to Requirements**:
- FR-008: Toggle status between Complete and Incomplete
- FR-009: Handle non-existent IDs

---

## UI Layer Contracts

### Menu Display

```python
def show_menu(self) -> None:
    """
    Display main menu options.

    Postconditions:
        - Menu printed to stdout
        - No input read
    """
```

### Input Handling

```python
def get_menu_choice(self) -> int:
    """
    Read and validate menu selection.

    Returns:
        int: Valid menu option (1-6)

    Postconditions:
        - Prompts until valid input received
        - Handles non-numeric input gracefully
    """

def get_task_id(self) -> int:
    """
    Read and validate task ID input.

    Returns:
        int: Positive integer ID

    Postconditions:
        - Prompts until valid positive integer received
        - Handles non-numeric and negative input
    """

def get_task_title(self) -> str:
    """
    Read and validate task title.

    Returns:
        str: Non-empty string (after strip)

    Postconditions:
        - Prompts until non-empty input received
    """

def get_task_description(self) -> str:
    """
    Read optional task description.

    Returns:
        str: Any string (may be empty)
    """
```

---

## Error Response Contracts

| Error Condition | Response Message | Action |
|-----------------|------------------|--------|
| Empty title | "Task title cannot be empty" | Re-prompt |
| Non-numeric ID | "Invalid ID format. Please enter a number." | Re-prompt |
| Negative ID | "Invalid ID. Please enter a positive number." | Re-prompt |
| Task not found | "Task not found" | Return to menu |
| Invalid menu option | "Invalid option. Please try again." | Re-prompt |

---

## Traceability Matrix

| Contract | Functional Requirement | User Story |
|----------|----------------------|------------|
| add_task | FR-001, FR-002, FR-003 | US-1 |
| get_all_tasks | FR-004, FR-005 | US-2 |
| update_task | FR-006, FR-009, FR-010 | US-4 |
| delete_task | FR-007, FR-009 | US-5 |
| toggle_status | FR-008, FR-009 | US-3 |
| show_menu | FR-013 | All |
| Input handlers | FR-010, FR-014 | All |
