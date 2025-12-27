"""Pytest fixtures for unit tests."""

import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import pytest
from services import TaskService


@pytest.fixture
def task_service():
    """Provide a fresh TaskService instance for each test."""
    service = TaskService()
    yield service
    # No cleanup needed for in-memory storage
