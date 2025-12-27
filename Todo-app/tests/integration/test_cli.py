"""Integration tests for CLI commands."""

import sys
from pathlib import Path
from io import StringIO
from unittest.mock import patch

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import pytest
from datetime import datetime
from services import TaskService
from ui import ConsoleUI


@pytest.fixture
def cli_setup():
    """Provide fresh TaskService and ConsoleUI instances for each test."""
    service = TaskService()
    ui = ConsoleUI(service)
    return service, ui


def test_handle_add_task_cli_flow(cli_setup):
    """T100: Test add task CLI flow with all fields."""
    service, ui = cli_setup

    # Simulate user input: title, description, priority, tags, due_date
    inputs = [
        "Test Task Title",
        "Test description",
        "High",
        "work,urgent",
        "2025-12-31"
    ]

    with patch('builtins.input', side_effect=inputs):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            ui.handle_add_task()

    # Verify task was created
    tasks = service.get_all_tasks()
    assert len(tasks) == 1
    task = tasks[0]
    assert task.title == "Test Task Title"
    assert task.description == "Test description"
    assert task.priority == "High"
    assert task.tags == ["work", "urgent"]
    assert task.due_date == datetime(2025, 12, 31)


def test_handle_update_task_cli_flow(cli_setup):
    """T101: Test update task CLI flow."""
    service, ui = cli_setup

    # First add a task
    service.add_task("Original Title", "Original description", "Medium", ["old"], datetime(2025, 1, 1))

    # Simulate update input: task ID, new title, new description, new priority, new tags, new due_date
    inputs = [
        "1",           # task ID
        "Updated Title",
        "Updated description",
        "High",
        "new,updated",
        "2025-12-25"
    ]

    with patch('builtins.input', side_effect=inputs):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            ui.handle_update_task()

    # Verify task was updated
    task = service.get_task(1)
    assert task.title == "Updated Title"
    assert task.description == "Updated description"
    assert task.priority == "High"
    assert task.tags == ["new", "updated"]
    assert task.due_date == datetime(2025, 12, 25)


def test_handle_search_tasks_cli_flow(cli_setup):
    """T102: Test search tasks CLI flow."""
    service, ui = cli_setup

    # Add some tasks
    service.add_task("Report Task", "Quarterly report")
    service.add_task("Grocery Shopping", "Buy groceries")

    # Simulate search input
    inputs = ["report"]

    with patch('builtins.input', side_effect=inputs):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            ui.handle_search_tasks()
            output = mock_stdout.getvalue()

    # Verify search results
    assert "1 task(s) found" in output
    assert "Report Task" in output


def test_handle_filter_tasks_cli_flow(cli_setup):
    """T103: Test filter tasks CLI flow."""
    service, ui = cli_setup

    # Add some tasks with different priorities
    service.add_task("High Priority", priority="High")
    service.add_task("Medium Priority", priority="Medium")
    service.add_task("Low Priority", priority="Low")

    # Simulate filter input (option 4 = High priority)
    inputs = ["4"]

    with patch('builtins.input', side_effect=inputs):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            ui.handle_filter_tasks()
            output = mock_stdout.getvalue()

    # Verify filter results
    assert "1 task(s) matching filter" in output
    assert "High Priority" in output


def test_handle_sort_tasks_cli_flow(cli_setup):
    """T104: Test sort tasks CLI flow."""
    service, ui = cli_setup

    # Add some tasks with different priorities
    service.add_task("Low Task", priority="Low")
    service.add_task("High Task", priority="High")
    service.add_task("Medium Task", priority="Medium")

    # Simulate sort input (option 2 = priority, desc)
    inputs = ["2", "desc"]

    with patch('builtins.input', side_effect=inputs):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            ui.handle_sort_tasks()
            output = mock_stdout.getvalue()

    # Verify sort results
    assert "3 task(s) sorted by priority" in output
    # High should appear before Medium, Medium before Low
    high_pos = output.find("High Task")
    medium_pos = output.find("Medium Task")
    low_pos = output.find("Low Task")
    assert high_pos < medium_pos < low_pos


def test_menu_displays_all_options(cli_setup):
    """Test that menu displays all 9 options."""
    service, ui = cli_setup

    with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        ui.show_menu()
        output = mock_stdout.getvalue()

    assert "1. Add Task" in output
    assert "2. View Tasks" in output
    assert "3. Update Task" in output
    assert "4. Delete Task" in output
    assert "5. Toggle Status" in output
    assert "6. Search Tasks" in output
    assert "7. Filter Tasks" in output
    assert "8. Sort Tasks" in output
    assert "9. Exit" in output
