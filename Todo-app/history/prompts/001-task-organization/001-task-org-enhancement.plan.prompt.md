---
id: 001
title: Task Org Enhancement Plan
stage: plan
date: 2025-12-24
surface: agent
model: claude-sonnet-4.5-20250929
feature: 001-task-organization
branch: 001-task-organization
user: (unknown)
command: /sp.plan
labels: ["planning","architecture","task-organization"]
links:
  spec: specs/001-task-organization/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-task-organization/plan.md
 - specs/001-task-organization/research.md
 - specs/001-task-organization/data-model.md
 - specs/001-task-organization/contracts/task-service-interface.md
 - specs/001-task-organization/contracts/cli-commands.md
 - specs/001-task-organization/quickstart.md
tests:
 - (none - planning phase)
---

## Prompt

1. Update Data Model
Task Class:
Add attributes:
priority: str (High, Medium, Low)
tags: List[str] (optional)
due_date: Optional[datetime]
Keep existing attributes: id, title, description, completed
Validation:
Ensure priority is one of allowed values.
Tags are optional; store as a list.
due_date should be parsed to datetime if provided.
2. Modify Task Creation & Update
add_task(title, description, priority=None, tags=None, due_date=None):
Accept new fields and validate.
Assign defaults if not provided (priority='Medium', tags=[], due_date=None).
update_task(task_id, ...):
Allow updating priority, tags, and due date.
Validate inputs.
3. Implement Search
search_tasks(keyword: str) -> List[Task]:
Case-insensitive search on title and description.
Return matching tasks.
4. Implement Filter
filter_tasks(status=None, priority=None, tags=None) -> List[Task]:
Filter by:
status -> completed or incomplete
priority -> High / Medium / Low
tags -> match if task has at least one of specified tags
5. Implement Sort
sort_tasks(by='due_date', order='asc') -> List[Task]:
Sort options:
by='due_date' -> ascending/descending
by='priority' -> High->Low or Low->High
by='title' -> alphabetical
Return sorted task list.
6. Update Console Commands
Add CLI parsing for new fields and commands:
add "Task Title" --priority High --tags work,urgent --due 2025-12-25
update 1 --priority Medium --tags home,chores
search "keyword"
filter --status incomplete --priority High --tags work
sort --by due_date --order asc
7. Display Enhancements
When listing tasks:
Show priority, tags, and due_date alongside title and status.
Format as a readable table for the console.
8. Testing
Unit tests for:
Adding/updating tasks with new fields.
Searching (case-insensitive, partial matches).
Filtering by status, priority, tags.
Sorting by all criteria.
Edge cases:
Empty tags list.
Invalid priority input.
Tasks without due date.

## Response snapshot

Completed implementation planning workflow for Task Organization Enhancement:

**Phase 0 - Research**: Generated research.md resolving testing framework choice (pytest with fixtures and parametrize, no external dependencies beyond pytest).

**Phase 1 - Design**:
- data-model.md: Extended Task dataclass with priority (High/Medium/Low), tags (List[str]), due_date (Optional[datetime])
- contracts/task-service-interface.md: API contracts for search_tasks(), filter_tasks(), sort_tasks() and updated add_task()/update_task()
- contracts/cli-commands.md: CLI contracts for search/filter/sort commands with enhanced display format
- quickstart.md: User guide with interactive examples

**Constitution Gates**: All principles passed (spec-driven, claude-only, in-memory, clean architecture, spec governance, fixed tech stack)

**Generated Artifacts**:
- specs/001-task-organization/plan.md
- specs/001-task-organization/research.md
- specs/001-task-organization/data-model.md
- specs/001-task-organization/contracts/task-service-interface.md
- specs/001-task-organization/contracts/cli-commands.md
- specs/001-task-organization/quickstart.md

**Next Steps**: Run `/sp.tasks` to generate testable task breakdown for implementation.

## Outcome

- ✅ Impact: Planning completed with all design artifacts generated. Ready for task breakdown phase.
- 🧪 Tests: None (planning phase)
- 📁 Files: 6 files created (plan.md, research.md, data-model.md, 2 contract files, quickstart.md)
- 🔁 Next prompts: Run /sp.tasks to generate tasks.md
- 🧠 Reflection: Constitution compliance verified. No violations detected. Clean architecture preserved. All spec requirements mapped to design artifacts.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A (planning phase)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A (proceed to tasks generation)
