# Research: Testing Framework for Todo Organization Feature

**Feature**: 001-task-organization
**Date**: 2025-12-24
**Purpose**: Resolve testing approach for the enhanced Todo application

## Unknown: Testing Framework and Patterns

### Question: What testing framework and patterns should be used for Python console application with dataclass models and service layer?

### Decision: pytest with standard fixtures and parametrize decorator

**Rationale**:
- pytest is the de facto standard for Python testing with excellent Python 3.13+ support
- Built-in fixture system for test isolation (ideal for in-memory TaskService)
- Parametrize decorator for testing multiple input cases efficiently
- Clear assertions with helpful failure messages
- No external dependencies required (stdlib compatible)
- Well-documented patterns for testing dataclasses and service logic

**Alternatives Considered**:
- **unittest** (stdlib): Built-in but more verbose; requires boilerplate for similar functionality
- **unittest + unittest.mock**: More complex setup than pytest fixtures; less readable test code

### Implementation Patterns

#### 1. Testing Dataclass Models (Task)

**Pattern**: Use `@dataclass` frozen testing for immutability verification
```python
import pytest
from models import Task

def test_task_creation_with_defaults():
    """Test task creation with default priority and no tags."""
    task = Task(id=1, title="Test Task")
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.priority == "Medium"  # default
    assert task.tags == []            # default

@pytest.mark.parametrize("priority,valid", [
    ("High", True),
    ("Medium", True),
    ("Low", True),
    ("Urgent", False),
    ("", False),
])
def test_priority_validation(priority, valid):
    """Test priority field accepts only valid values."""
    if valid:
        task = Task(id=1, title="Test", priority=priority)
        assert task.priority == priority
    else:
        with pytest.raises(ValueError):
            Task(id=1, title="Test", priority=priority)
```

#### 2. Testing Service Layer (TaskService)

**Pattern**: Use pytest fixtures for service instance with isolated state
```python
@pytest.fixture
def task_service():
    """Provide fresh TaskService instance for each test."""
    service = TaskService()
    yield service
    # No cleanup needed for in-memory storage

def test_add_task_with_new_fields(task_service):
    """Test adding task with priority, tags, and due_date."""
    task = task_service.add_task(
        title="Test Task",
        priority="High",
        tags=["work", "urgent"],
        due_date=datetime(2025, 12, 25)
    )
    assert task.id == 1
    assert task.priority == "High"
    assert task.tags == ["work", "urgent"]
    assert task.due_date == datetime(2025, 12, 25)
```

**Pattern**: Use parametrize for search/filter/sort edge cases
```python
@pytest.mark.parametrize("keyword,expected_count", [
    ("report", 1),      # partial match
    ("REPORT", 1),      # case-insensitive
    ("nonexistent", 0), # no match
    ("", 3),            # empty returns all
])
def test_search_cases(task_service, keyword, expected_count):
    """Test search with various keyword inputs."""
    # Setup tasks...
    results = task_service.search_tasks(keyword)
    assert len(results) == expected_count
```

#### 3. Testing CLI Commands

**Pattern**: Mock input/output using monkeypatch fixture
```python
def test_add_task_cli(monkeypatch, capsys):
    """Test add command with CLI input simulation."""
    inputs = ["Test Title", "Test Description", "High", "work,urgent", "2025-12-25"]
    monkeypatch.setattr('builtins.input', lambda _: inputs.pop(0))

    # Run CLI command...
    captured = capsys.readouterr()
    assert "Task added successfully" in captured.out
```

### Test Structure

**Organization**:
```
tests/
├── unit/
│   ├── test_models.py       # Task dataclass tests
│   │   ├── test_task_creation.py
│   │   ├── test_priority_validation.py
│   │   └── test_tags_validation.py
│   └── test_services.py     # TaskService tests
│       ├── test_add_task.py
│       ├── test_search_tasks.py
│       ├── test_filter_tasks.py
│       └── test_sort_tasks.py
└── integration/
    └── test_cli.py           # End-to-end CLI tests
```

### Coverage Goals

- Unit tests: 90%+ coverage on models and services
- Edge cases covered for:
  - Invalid priority values
  - Empty tags list
  - Tasks without due dates
  - Empty search terms
  - Conflicting filters
- Performance validation:
  - Search under 5 seconds with 1000 tasks
  - Filter under 3 seconds with 1000 tasks
  - Sort under 3 seconds with 1000 tasks

### Dependencies

Only pytest required (no external mocking libraries needed):
```toml
[project.optional-dependencies]
test = ["pytest>=8.0"]
```

Or add to existing project config as needed.

## Conclusion

**Framework**: pytest
**Approach**:
- Unit tests with fixtures for isolation
- Parametrize for multi-case testing
- Monkeypatch for CLI input/output mocking
- No external dependencies beyond pytest

This approach satisfies the fixed tech stack constraint (Python 3.13+) while providing excellent testability for the in-memory Todo application.
