"""Entry point for Todo Application."""

from services import TaskService
from ui import ConsoleUI


def main() -> None:
    """Initialize and run the Todo application."""
    service = TaskService()
    ui = ConsoleUI(service)
    ui.run()


if __name__ == "__main__":
    main()
