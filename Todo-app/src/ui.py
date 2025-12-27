"""Console UI for Todo Application."""

from datetime import datetime
from typing import List

from models import Task
from services import TaskService


class ConsoleUI:
    """Handles console input/output for the Todo application.

    Attributes:
        service: TaskService instance for business logic.
    """

    def __init__(self, service: TaskService) -> None:
        """Initialize ConsoleUI with a TaskService.

        Args:
            service: TaskService instance to handle task operations.
        """
        self.service = service

    def get_task_title(self) -> str:
        """Read and validate task title from user.

        Returns:
            str: Non-empty string after strip.

        Note:
            Prompts until non-empty input received.
        """
        while True:
            title = input("Enter task title: ").strip()
            if title:
                return title
            print("Task title cannot be empty. Please try again.")

    def get_task_description(self) -> str:
        """Read optional task description from user.

        Returns:
            str: Any string (may be empty).
        """
        return input("Enter description (optional): ").strip()

    def get_priority(self) -> str:
        """Read and validate priority from user.

        Returns:
            str: Valid priority (High/Medium/Low).

        Note:
            Prompts until valid input received.
        """
        while True:
            priority_input = input("Enter priority (High/Medium/Low, default Medium): ").strip()
            if not priority_input:
                return "Medium"  # default

            if priority_input in ["High", "Medium", "Low"]:
                return priority_input
            print("Invalid priority. Must be High, Medium, or Low. Please try again.")

    def get_tags(self) -> List[str]:
        """Read optional tags from user.

        Returns:
            List[str]: List of tag strings (may be empty).

        Note:
            Splits input by comma and strips whitespace from each tag.
        """
        tags_input = input("Enter tags (comma-separated, optional): ").strip()
        if not tags_input:
            return []
        return [tag.strip() for tag in tags_input.split(",") if tag.strip()]

    def get_due_date(self) -> datetime | None:
        """Read optional due date from user.

        Returns:
            datetime | None: Parsed datetime or None if empty.

        Note:
            Prompts until valid date or empty input received.
        """
        while True:
            date_input = input("Enter due date (YYYY-MM-DD, optional): ").strip()
            if not date_input:
                return None
            try:
                return datetime.fromisoformat(date_input)
            except ValueError:
                print("Invalid date format. Use YYYY-MM-DD. Please try again.")

    def handle_add_task(self) -> None:
        """Handle the Add Task operation.

        Prompts for title, description, priority, tags, and due_date, creates task, displays confirmation.
        """
        title = self.get_task_title()
        description = self.get_task_description()
        priority = self.get_priority()
        tags = self.get_tags()
        due_date = self.get_due_date()

        try:
            task = self.service.add_task(title, description, priority, tags, due_date)
            print(f"Task added successfully! ID: {task.id}")
        except ValueError as e:
            print(f"Error: {e}")

    def display_task(self, task: Task) -> None:
        """Display a single task in the enhanced format.

        Args:
            task: Task to display.

        Format:
            ID: {id} | Title: {title} | Priority: {priority} | Status: {status}
            Due: {due_date} | Tags: {tags}  (if applicable)
            Description: {description}  (if not empty)
            ---
        """
        status = "Complete" if task.completed else "Incomplete"
        print(f"ID: {task.id} | Title: {task.title} | Priority: {task.priority} | Status: {status}")

        # Due date and tags line
        if task.due_date:
            due_str = task.due_date.strftime("%Y-%m-%d")
            if task.tags:
                print(f"Due: {due_str} | Tags: {', '.join(task.tags)}")
            else:
                print(f"Due: {due_str}")
        elif task.tags:
            print(f"Tags: {', '.join(task.tags)}")

        if task.description:
            print(f"Description: {task.description}")
        print("---")

    def handle_view_tasks(self) -> None:
        """Handle the View Tasks operation.

        Displays all tasks or a message if no tasks exist.
        """
        tasks = self.service.get_all_tasks()

        if not tasks:
            print("No tasks found. Add a task to get started.")
            return

        print("\n=== All Tasks ===")
        for task in tasks:
            self.display_task(task)

    def get_task_id(self) -> int:
        """Read and validate task ID from user.

        Returns:
            int: Positive integer ID.

        Note:
            Prompts until valid positive integer received.
        """
        while True:
            user_input = input("Enter task ID: ").strip()
            try:
                task_id = int(user_input)
                if task_id < 1:
                    print("Invalid ID. Please enter a positive number.")
                    continue
                return task_id
            except ValueError:
                print("Invalid ID format. Please enter a number.")

    def handle_toggle_status(self) -> None:
        """Handle the Toggle Status operation.

        Prompts for task ID, toggles status, displays result.
        """
        task_id = self.get_task_id()

        if self.service.toggle_status(task_id):
            task = self.service.get_task(task_id)
            status = "Complete" if task.completed else "Incomplete"
            print(f"Task status toggled to: {status}")
        else:
            print("Task not found")

    def handle_update_task(self) -> None:
        """Handle the Update Task operation.

        Prompts for task ID, new title, new description, new priority, new tags, new due_date.
        Updates task if found, displays error otherwise.
        """
        task_id = self.get_task_id()

        # Check if task exists first
        task = self.service.get_task(task_id)
        if task is None:
            print("Task not found")
            return

        print(f"Current title: {task.title}")
        print(f"Current description: {task.description or '(none)'}")
        print(f"Current priority: {task.priority}")
        print(f"Current tags: {', '.join(task.tags) if task.tags else '(none)'}")
        if task.due_date:
            print(f"Current due date: {task.due_date.strftime('%Y-%m-%d')}")
        else:
            print("Current due date: (none)")

        # Get new values (empty means keep current)
        new_title_input = input("Enter new title (leave empty to keep current): ").strip()
        new_description_input = input("Enter new description (leave empty to keep current): ").strip()
        new_priority_input = input("Enter new priority (High/Medium/Low, leave empty to keep current): ").strip()
        new_tags_input = input("Enter new tags (comma-separated, leave empty to keep current): ").strip()
        new_due_date_input = input("Enter new due date (YYYY-MM-DD, leave empty to keep current): ").strip()

        # Use current values if input is empty
        title = new_title_input if new_title_input else task.title
        description = new_description_input if new_description_input else task.description

        # Validate and set priority
        priority = None
        if new_priority_input:
            if new_priority_input not in ["High", "Medium", "Low"]:
                print("Invalid priority. Must be High, Medium, or Low.")
                return
            priority = new_priority_input

        # Parse tags if provided
        tags = None
        if new_tags_input:
            tags = [tag.strip() for tag in new_tags_input.split(",") if tag.strip()]

        # Parse due date if provided
        due_date = None
        if new_due_date_input:
            try:
                due_date = datetime.fromisoformat(new_due_date_input)
            except ValueError:
                print("Invalid date format. Use YYYY-MM-DD.")
                return

        try:
            if self.service.update_task(task_id, title, description, priority, tags, due_date):
                print("Task updated successfully!")
            else:
                print("Task not found")
        except ValueError as e:
            print(f"Error: {e}")

    def handle_delete_task(self) -> None:
        """Handle the Delete Task operation.

        Prompts for task ID, deletes if found, displays result.
        """
        task_id = self.get_task_id()

        if self.service.delete_task(task_id):
            print("Task deleted successfully")
        else:
            print("Task not found")

    def handle_search_tasks(self) -> None:
        """Handle the Search Tasks operation.

        Prompts for search keyword and displays matching tasks.
        """
        keyword = input("Enter search keyword: ").strip()
        results = self.service.search_tasks(keyword)

        if not results:
            print("No tasks found matching your search.")
            return

        print(f"\n=== {len(results)} task(s) found ===")
        for task in results:
            self.display_task(task)

    def handle_filter_tasks(self) -> None:
        """Handle the Filter Tasks operation.

        Displays filter menu and filters tasks based on user selection.
        """
        print("\nFilter by:")
        print("1. All tasks")
        print("2. Incomplete only")
        print("3. Complete only")
        print("4. High priority")
        print("5. Medium priority")
        print("6. Low priority")
        print("7. By tags")
        print("8. Multiple filters")

        while True:
            filter_input = input("Enter choice: ").strip()
            try:
                filter_choice = int(filter_input)
                if 1 <= filter_choice <= 8:
                    break
                print("Invalid option. Please enter a number between 1 and 8.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        results = []
        if filter_choice == 1:
            results = self.service.filter_tasks()
        elif filter_choice == 2:
            results = self.service.filter_tasks(status=False)
        elif filter_choice == 3:
            results = self.service.filter_tasks(status=True)
        elif filter_choice == 4:
            results = self.service.filter_tasks(priority="High")
        elif filter_choice == 5:
            results = self.service.filter_tasks(priority="Medium")
        elif filter_choice == 6:
            results = self.service.filter_tasks(priority="Low")
        elif filter_choice == 7:
            tags_input = input("Enter tags (comma-separated): ").strip()
            if tags_input:
                tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]
                results = self.service.filter_tasks(tags=tags)
            else:
                results = self.service.filter_tasks()
        elif filter_choice == 8:
            # Multiple filters
            status_input = input("Enter status (completed/incomplete, leave empty to skip): ").strip().lower()
            priority_input = input("Enter priority (High/Medium/Low, leave empty to skip): ").strip()
            tags_input = input("Enter tags (comma-separated, leave empty to skip): ").strip()

            status = None
            if status_input == "completed":
                status = True
            elif status_input == "incomplete":
                status = False

            priority = None
            if priority_input in ["High", "Medium", "Low"]:
                priority = priority_input

            tags = None
            if tags_input:
                tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]

            results = self.service.filter_tasks(status=status, priority=priority, tags=tags)

        if not results:
            print("No tasks match the filter criteria.")
            return

        print(f"\n=== {len(results)} task(s) matching filter ===")
        for task in results:
            self.display_task(task)

    def handle_sort_tasks(self) -> None:
        """Handle the Sort Tasks operation.

        Displays sort menu and sorts tasks based on user selection.
        """
        print("\nSort by:")
        print("1. Due date")
        print("2. Priority")
        print("3. Title (alphabetical)")

        while True:
            sort_input = input("Enter choice: ").strip()
            try:
                sort_choice = int(sort_input)
                if 1 <= sort_choice <= 3:
                    break
                print("Invalid option. Please enter a number between 1 and 3.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        while True:
            order_input = input("Sort order (asc/desc): ").strip().lower()
            if order_input in ["asc", "desc"]:
                break
            print("Invalid order. Please enter 'asc' or 'desc'.")

        by_field = "due_date"
        if sort_choice == 1:
            by_field = "due_date"
        elif sort_choice == 2:
            by_field = "priority"
        elif sort_choice == 3:
            by_field = "title"

        try:
            results = self.service.sort_tasks(by=by_field, order=order_input)

            if not results:
                print("No tasks to sort.")
                return

            print(f"\n=== {len(results)} task(s) sorted by {by_field} ({order_input}) ===")
            for task in results:
                self.display_task(task)
        except ValueError as e:
            print(f"Error: {e}")

    def show_menu(self) -> None:
        """Display the main menu options."""
        print("\n=== Todo Application ===")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Toggle Status")
        print("6. Search Tasks")
        print("7. Filter Tasks")
        print("8. Sort Tasks")
        print("9. Exit")

    def get_menu_choice(self) -> int:
        """Read and validate menu selection from user.

        Returns:
            int: Valid menu option (1-9).

        Note:
            Prompts until valid input received.
        """
        while True:
            user_input = input("\nEnter choice: ").strip()
            try:
                choice = int(user_input)
                if 1 <= choice <= 9:
                    return choice
                print("Invalid option. Please enter a number between 1 and 9.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def run(self) -> None:
        """Run the main application loop.

        Displays menu, handles user choices, and exits gracefully.
        """
        while True:
            self.show_menu()
            choice = self.get_menu_choice()

            if choice == 1:
                self.handle_add_task()
            elif choice == 2:
                self.handle_view_tasks()
            elif choice == 3:
                self.handle_update_task()
            elif choice == 4:
                self.handle_delete_task()
            elif choice == 5:
                self.handle_toggle_status()
            elif choice == 6:
                self.handle_search_tasks()
            elif choice == 7:
                self.handle_filter_tasks()
            elif choice == 8:
                self.handle_sort_tasks()
            elif choice == 9:
                print("Goodbye!")
                break
