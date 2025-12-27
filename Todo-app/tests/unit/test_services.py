"""Unit tests for TaskService."""

import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import pytest
from models import Task
from services import TaskService


def test_add_task_with_priority(task_service):
    """Test adding task with priority parameter."""
    task = task_service.add_task(
        title="Test Task",
        description="Test description",
        priority="High"
    )
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.priority == "High"


def test_update_task_with_priority(task_service):
    """Test updating task priority."""
    # Create a task first
    task = task_service.add_task("Test", priority="Medium")
    assert task.priority == "Medium"

    # Update priority
    task_service.update_task(task.id, "Test", "", priority="High")
    updated = task_service.get_task(task.id)
    assert updated.priority == "High"


def test_add_task_validates_invalid_priority(task_service):
    """Test add_task raises ValueError for invalid priority."""
    with pytest.raises(ValueError, match="Priority must be one of"):
        task_service.add_task("Test", priority="Urgent")


# User Story 2: Tags Service Tests
def test_add_task_with_tags(task_service):
    """T028: Test add_task with tags parameter."""
    task = task_service.add_task(
        title="Test Task",
        description="Test description",
        tags=["work", "urgent"]
    )
    assert task.id == 1
    assert task.tags == ["work", "urgent"]


def test_update_task_with_tags(task_service):
    """T029: Test update_task with tags parameter."""
    # Create a task first
    task = task_service.add_task("Test", tags=["work"])
    assert task.tags == ["work"]

    # Update tags
    task_service.update_task(task.id, "Test", "", tags=["personal", "shopping"])
    updated = task_service.get_task(task.id)
    assert updated.tags == ["personal", "shopping"]


# User Story 3: Search Tests
from datetime import datetime


def test_search_with_matching_keyword_in_title(task_service):
    """T038: Test search with matching keyword in title."""
    task_service.add_task("Complete project report", "Quarterly analysis")
    task_service.add_task("Buy groceries", "Weekly shopping")

    results = task_service.search_tasks("report")
    assert len(results) == 1
    assert results[0].title == "Complete project report"


def test_search_with_matching_keyword_in_description(task_service):
    """T039: Test search with matching keyword in description."""
    task_service.add_task("Task One", "Contains important info")
    task_service.add_task("Task Two", "Regular description")

    results = task_service.search_tasks("important")
    assert len(results) == 1
    assert results[0].title == "Task One"


def test_case_insensitive_search(task_service):
    """T040: Test case-insensitive search."""
    task_service.add_task("Complete REPORT", "Test description")

    # Search lowercase
    results_lower = task_service.search_tasks("report")
    assert len(results_lower) == 1

    # Search uppercase
    results_upper = task_service.search_tasks("REPORT")
    assert len(results_upper) == 1

    # Search mixed case
    results_mixed = task_service.search_tasks("RePoRt")
    assert len(results_mixed) == 1


def test_search_with_no_matches_returns_empty_list(task_service):
    """T041: Test search with no matches returns empty list."""
    task_service.add_task("Task One", "Description one")
    task_service.add_task("Task Two", "Description two")

    results = task_service.search_tasks("nonexistent")
    assert results == []
    assert len(results) == 0


def test_search_with_empty_keyword_returns_all_tasks(task_service):
    """T042: Test search with empty keyword returns all tasks."""
    task_service.add_task("Task One", "Description one")
    task_service.add_task("Task Two", "Description two")
    task_service.add_task("Task Three", "Description three")

    results = task_service.search_tasks("")
    assert len(results) == 3


# User Story 4: Filter Tests
def test_filter_by_status_completed(task_service):
    """T050: Test filter by status=True (completed)."""
    task1 = task_service.add_task("Task One")
    task2 = task_service.add_task("Task Two")
    task_service.toggle_status(task1.id)  # Mark as completed

    results = task_service.filter_tasks(status=True)
    assert len(results) == 1
    assert results[0].completed is True


def test_filter_by_status_incomplete(task_service):
    """T051: Test filter by status=False (incomplete)."""
    task1 = task_service.add_task("Task One")
    task2 = task_service.add_task("Task Two")
    task_service.toggle_status(task1.id)  # Mark as completed

    results = task_service.filter_tasks(status=False)
    assert len(results) == 1
    assert results[0].completed is False


def test_filter_by_priority(task_service):
    """T052: Test filter by priority."""
    task_service.add_task("High Task", priority="High")
    task_service.add_task("Medium Task", priority="Medium")
    task_service.add_task("Low Task", priority="Low")

    results = task_service.filter_tasks(priority="High")
    assert len(results) == 1
    assert results[0].priority == "High"


def test_filter_by_single_tag(task_service):
    """T053: Test filter by single tag."""
    task_service.add_task("Work Task", tags=["work"])
    task_service.add_task("Personal Task", tags=["personal"])
    task_service.add_task("Both Task", tags=["work", "personal"])

    results = task_service.filter_tasks(tags=["work"])
    assert len(results) == 2  # Work Task and Both Task


def test_filter_by_multiple_tags_or_logic(task_service):
    """T054: Test filter by multiple tags (OR logic)."""
    task_service.add_task("Work Task", tags=["work"])
    task_service.add_task("Personal Task", tags=["personal"])
    task_service.add_task("Finance Task", tags=["finance"])

    results = task_service.filter_tasks(tags=["work", "personal"])
    assert len(results) == 2  # Work Task and Personal Task


def test_filter_by_multiple_criteria(task_service):
    """T055: Test filter by multiple criteria (status + priority + tags)."""
    task1 = task_service.add_task("High Priority Work", priority="High", tags=["work"])
    task2 = task_service.add_task("Medium Priority Work", priority="Medium", tags=["work"])
    task3 = task_service.add_task("High Priority Personal", priority="High", tags=["personal"])
    task_service.toggle_status(task1.id)  # Mark first as completed

    # Filter: incomplete, High priority, work tag
    results = task_service.filter_tasks(status=False, priority="High", tags=["work"])
    assert len(results) == 0  # task1 matches but is completed


def test_filter_with_all_none_returns_all_tasks(task_service):
    """T056: Test filter with all None returns all tasks."""
    task_service.add_task("Task One")
    task_service.add_task("Task Two")
    task_service.add_task("Task Three")

    results = task_service.filter_tasks()
    assert len(results) == 3


def test_filter_with_conflicting_criteria_returns_empty(task_service):
    """T057: Test filter with conflicting criteria returns empty list."""
    task1 = task_service.add_task("Task One", priority="High")
    task_service.toggle_status(task1.id)  # Mark as completed

    # Filter for incomplete High priority - task1 is High but completed
    results = task_service.filter_tasks(status=False, priority="High")
    assert len(results) == 0


# User Story 5: Sort Tests
def test_sort_by_due_date_ascending(task_service):
    """T069: Test sort by due_date ascending."""
    task_service.add_task("Task Later", due_date=datetime(2025, 12, 31))
    task_service.add_task("Task Earlier", due_date=datetime(2025, 12, 1))
    task_service.add_task("Task Middle", due_date=datetime(2025, 12, 15))

    results = task_service.sort_tasks(by="due_date", order="asc")
    assert results[0].title == "Task Earlier"
    assert results[1].title == "Task Middle"
    assert results[2].title == "Task Later"


def test_sort_by_due_date_descending(task_service):
    """T070: Test sort by due_date descending."""
    task_service.add_task("Task Later", due_date=datetime(2025, 12, 31))
    task_service.add_task("Task Earlier", due_date=datetime(2025, 12, 1))
    task_service.add_task("Task Middle", due_date=datetime(2025, 12, 15))

    results = task_service.sort_tasks(by="due_date", order="desc")
    assert results[0].title == "Task Later"
    assert results[1].title == "Task Middle"
    assert results[2].title == "Task Earlier"


def test_sort_by_priority_descending(task_service):
    """T071: Test sort by priority descending (High->Medium->Low)."""
    task_service.add_task("Low Task", priority="Low")
    task_service.add_task("High Task", priority="High")
    task_service.add_task("Medium Task", priority="Medium")

    results = task_service.sort_tasks(by="priority", order="desc")
    assert results[0].priority == "High"
    assert results[1].priority == "Medium"
    assert results[2].priority == "Low"


def test_sort_by_priority_ascending(task_service):
    """T072: Test sort by priority ascending (Low->Medium->High)."""
    task_service.add_task("Low Task", priority="Low")
    task_service.add_task("High Task", priority="High")
    task_service.add_task("Medium Task", priority="Medium")

    results = task_service.sort_tasks(by="priority", order="asc")
    assert results[0].priority == "Low"
    assert results[1].priority == "Medium"
    assert results[2].priority == "High"


def test_sort_by_title_ascending(task_service):
    """T073: Test sort by title ascending."""
    task_service.add_task("Zebra Task")
    task_service.add_task("Apple Task")
    task_service.add_task("Mango Task")

    results = task_service.sort_tasks(by="title", order="asc")
    assert results[0].title == "Apple Task"
    assert results[1].title == "Mango Task"
    assert results[2].title == "Zebra Task"


def test_sort_handles_none_due_date_at_end(task_service):
    """T074: Test sort handles None due_date values (places at end)."""
    task_service.add_task("No Date Task")  # due_date=None
    task_service.add_task("Has Date", due_date=datetime(2025, 12, 15))
    task_service.add_task("Also No Date")  # due_date=None

    results = task_service.sort_tasks(by="due_date", order="asc")
    assert results[0].title == "Has Date"
    # None values at end (order between them may vary)
    assert results[1].due_date is None
    assert results[2].due_date is None


def test_sort_with_invalid_by_raises_valueerror(task_service):
    """T075: Test sort with invalid by parameter raises ValueError."""
    task_service.add_task("Test Task")

    with pytest.raises(ValueError, match="Invalid sort field"):
        task_service.sort_tasks(by="invalid_field")


def test_sort_with_invalid_order_raises_valueerror(task_service):
    """T076: Test sort with invalid order parameter raises ValueError."""
    task_service.add_task("Test Task")

    with pytest.raises(ValueError, match="Invalid sort order"):
        task_service.sort_tasks(by="title", order="invalid_order")


# Phase 8: Due Date Tests
def test_add_task_with_due_date(task_service):
    """T098: Test add_task with due_date parameter."""
    due = datetime(2025, 12, 31, 23, 59)
    task = task_service.add_task(
        title="Deadline Task",
        due_date=due
    )
    assert task.due_date == due


def test_update_task_with_due_date(task_service):
    """T099: Test update_task with due_date parameter."""
    task = task_service.add_task("Test Task")
    assert task.due_date is None

    new_due = datetime(2025, 12, 25)
    task_service.update_task(task.id, "Test Task", "", due_date=new_due)
    updated = task_service.get_task(task.id)
    assert updated.due_date == new_due
