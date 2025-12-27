# Tasks: Python In-Memory Console Todo Application

**Input**: Design documents from `/specs/001-console-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md, contracts/service-contracts.md

**Tests**: Not requested in specification - manual console testing for Phase I MVP

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

---

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create src/ directory structure per plan.md
- [x] T002 [P] Create src/__init__.py as empty package marker
- [x] T003 [P] Create empty src/main.py placeholder
- [x] T004 [P] Create empty src/models.py placeholder
- [x] T005 [P] Create empty src/services.py placeholder
- [x] T006 [P] Create empty src/ui.py placeholder

**Checkpoint**: Directory structure ready

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T007 Implement Task dataclass in src/models.py with id, title, description, completed fields
- [x] T008 Implement TaskService class skeleton in src/services.py with tasks list and next_id counter
- [x] T009 Implement ConsoleUI class skeleton in src/ui.py with __init__ accepting TaskService

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Add New Task (Priority: P1)

**Goal**: Allow users to add tasks with title and optional description

**Independent Test**: Launch app, select "Add Task", enter title, verify task appears in list

### Implementation for User Story 1

- [x] T010 [US1] Implement add_task(title, description) method in src/services.py per service contract
- [x] T011 [US1] Add title validation (non-empty after strip) in add_task method in src/services.py
- [x] T012 [US1] Implement get_task_title() input method in src/ui.py with empty title validation
- [x] T013 [US1] Implement get_task_description() input method in src/ui.py (optional, allows empty)
- [x] T014 [US1] Implement handle_add_task() in src/ui.py calling service and displaying confirmation

**Checkpoint**: User Story 1 functional - can add tasks with title and description

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1)

**Goal**: Display all tasks showing ID, title, description, and status

**Independent Test**: Add tasks, select "View Tasks", verify all tasks displayed with correct details

### Implementation for User Story 2

- [x] T015 [US2] Implement get_all_tasks() method in src/services.py returning list of tasks
- [x] T016 [US2] Implement display_task(task) helper in src/ui.py per data-model.md display format
- [x] T017 [US2] Implement handle_view_tasks() in src/ui.py showing all tasks or "No tasks found" message

**Checkpoint**: User Stories 1 AND 2 functional - can add and view tasks

---

## Phase 5: User Story 3 - Toggle Task Status (Priority: P2)

**Goal**: Toggle task completion status between Complete and Incomplete

**Independent Test**: Add task, toggle status, verify status changed from Incomplete to Complete

### Implementation for User Story 3

- [x] T018 [US3] Implement get_task(task_id) helper method in src/services.py returning Task or None
- [x] T019 [US3] Implement toggle_status(task_id) method in src/services.py per service contract
- [x] T020 [US3] Implement get_task_id() input method in src/ui.py with numeric validation
- [x] T021 [US3] Implement handle_toggle_status() in src/ui.py calling service and displaying result

**Checkpoint**: User Story 3 functional - can toggle task completion status

---

## Phase 6: User Story 4 - Update Task (Priority: P2)

**Goal**: Update task title and/or description by ID

**Independent Test**: Add task, update title, verify change persisted in view

### Implementation for User Story 4

- [x] T022 [US4] Implement update_task(task_id, title, description) method in src/services.py per contract
- [x] T023 [US4] Add title validation in update_task (non-empty, preserve original if validation fails)
- [x] T024 [US4] Implement handle_update_task() in src/ui.py prompting for ID, new title, new description

**Checkpoint**: User Story 4 functional - can update task details

---

## Phase 7: User Story 5 - Delete Task (Priority: P3)

**Goal**: Remove task from list by ID

**Independent Test**: Add task, delete by ID, verify task no longer appears in view

### Implementation for User Story 5

- [x] T025 [US5] Implement delete_task(task_id) method in src/services.py per service contract
- [x] T026 [US5] Implement handle_delete_task() in src/ui.py prompting for ID and displaying result

**Checkpoint**: User Story 5 functional - can delete tasks

---

## Phase 8: User Story 6 - Exit Application (Priority: P3)

**Goal**: Provide clean exit with farewell message

**Independent Test**: Select "Exit", verify goodbye message displayed and app terminates

### Implementation for User Story 6

- [x] T027 [US6] Implement show_menu() in src/ui.py displaying numbered options 1-6
- [x] T028 [US6] Implement get_menu_choice() in src/ui.py with input validation (1-6, handle non-numeric)
- [x] T029 [US6] Implement run() main loop in src/ui.py routing menu choices to handlers
- [x] T030 [US6] Add exit handling in run() loop displaying "Goodbye!" and breaking loop

**Checkpoint**: All user stories functional - complete application ready for wiring

---

## Phase 9: Polish & Integration

**Purpose**: Wire application and final validation

- [x] T031 Implement main() function in src/main.py creating TaskService and ConsoleUI
- [x] T032 Add if __name__ == "__main__": main() entry point in src/main.py
- [x] T033 Run quickstart.md validation - test all 5 core operations manually
- [x] T034 Verify edge cases: empty title, invalid ID, non-numeric ID, empty task list
- [x] T035 Constitution compliance check - verify 4-file structure, no external dependencies

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-8)**: All depend on Foundational phase completion
  - US1 and US2 (both P1) can proceed in parallel after Foundational
  - US3 and US4 (both P2) depend on US1+US2 for testing but implementation can proceed
  - US5 and US6 (both P3) can proceed after P2 stories
- **Polish (Phase 9)**: Depends on all user stories being complete

### User Story Dependencies

| Story | Depends On | Can Start After |
|-------|------------|-----------------|
| US1 (Add) | Foundational | Phase 2 complete |
| US2 (View) | Foundational | Phase 2 complete |
| US3 (Toggle) | US1+US2 for testing | Phase 2 complete |
| US4 (Update) | US1+US2 for testing | Phase 2 complete |
| US5 (Delete) | US1+US2 for testing | Phase 2 complete |
| US6 (Exit/Menu) | All handlers exist | Phase 7 complete |

### Within Each User Story

- Service method before UI handler
- Input helpers before main handler
- Core implementation before integration

### Parallel Opportunities

**Phase 1** (all can run in parallel):
```
T002, T003, T004, T005, T006 can all run in parallel
```

**Phase 3+4** (after Foundational):
```
US1 and US2 can be implemented in parallel by different developers
```

**Phase 5+6** (after P1 stories):
```
US3 and US4 can be implemented in parallel by different developers
```

---

## Parallel Example: Setup Phase

```bash
# Launch all file creation tasks together:
Task: "Create src/__init__.py as empty package marker"
Task: "Create empty src/main.py placeholder"
Task: "Create empty src/models.py placeholder"
Task: "Create empty src/services.py placeholder"
Task: "Create empty src/ui.py placeholder"
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1 (Add Task)
4. Complete Phase 4: User Story 2 (View Tasks)
5. **STOP and VALIDATE**: Can add and view tasks
6. This is a minimal functional todo app!

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add US1 (Add) + US2 (View) → Basic MVP
3. Add US3 (Toggle) → Progress tracking
4. Add US4 (Update) → Task refinement
5. Add US5 (Delete) → List cleanup
6. Add US6 (Exit) + Polish → Complete application

### Full Sequential Strategy

For single developer:
```
Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5 → Phase 6 → Phase 7 → Phase 8 → Phase 9
```

---

## Task Summary

| Phase | Tasks | Purpose |
|-------|-------|---------|
| 1. Setup | T001-T006 (6) | Directory structure |
| 2. Foundational | T007-T009 (3) | Core classes |
| 3. US1 Add | T010-T014 (5) | Add task feature |
| 4. US2 View | T015-T017 (3) | View tasks feature |
| 5. US3 Toggle | T018-T021 (4) | Toggle status feature |
| 6. US4 Update | T022-T024 (3) | Update task feature |
| 7. US5 Delete | T025-T026 (2) | Delete task feature |
| 8. US6 Exit | T027-T030 (4) | Menu and exit |
| 9. Polish | T031-T035 (5) | Integration |
| **Total** | **35 tasks** | |

### Tasks per User Story

| User Story | Task Count | Tasks |
|------------|------------|-------|
| US1 (Add) | 5 | T010-T014 |
| US2 (View) | 3 | T015-T017 |
| US3 (Toggle) | 4 | T018-T021 |
| US4 (Update) | 3 | T022-T024 |
| US5 (Delete) | 2 | T025-T026 |
| US6 (Exit) | 4 | T027-T030 |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Manual testing per quickstart.md for Phase I MVP
