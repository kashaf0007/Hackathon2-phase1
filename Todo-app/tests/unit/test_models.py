"""Unit tests for Task dataclass."""

import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import pytest
from models import Task


def test_task_creation_with_defaults():
    """Test task creation with default priority and no tags."""
    task = Task(id=1, title="Test Task")
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.priority == "Medium"  # default
    assert task.tags == []            # default
    assert task.due_date is None       # default


@pytest.mark.parametrize("priority,valid", [
    ("High", True),
    ("Medium", True),
    ("Low", True),
    ("Urgent", False),
    ("", False),
    ("Critical", False),
])
def test_priority_validation(priority, valid):
    """Test priority field accepts only valid values."""
    if valid:
        task = Task(id=1, title="Test", priority=priority)
        assert task.priority == priority
    else:
        with pytest.raises(ValueError):
            Task(id=1, title="Test", priority=priority)


# User Story 2: Tags Tests
def test_task_creation_with_empty_tags():
    """T025: Test task creation with empty tags list."""
    task = Task(id=1, title="Test Task", tags=[])
    assert task.tags == []


def test_task_creation_with_multiple_tags():
    """T026: Test task creation with multiple tags."""
    tags = ["work", "urgent", "finance"]
    task = Task(id=1, title="Test Task", tags=tags)
    assert task.tags == ["work", "urgent", "finance"]
    assert len(task.tags) == 3


def test_tags_default_to_empty_list():
    """T027: Test tags default to empty list when not provided."""
    task = Task(id=1, title="Test Task")
    assert task.tags == []
    assert isinstance(task.tags, list)


# Phase 8: Due Date Tests
from datetime import datetime


def test_task_creation_with_due_date():
    """T096: Test task creation with due_date field."""
    due = datetime(2025, 12, 31, 23, 59)
    task = Task(id=1, title="Deadline Task", due_date=due)
    assert task.due_date == due


def test_task_due_date_defaults_to_none():
    """T097: Test due_date defaults to None when not provided."""
    task = Task(id=1, title="Test Task")
    assert task.due_date is None
