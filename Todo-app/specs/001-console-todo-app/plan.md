# Implementation Plan: Python In-Memory Console Todo Application

**Branch**: `001-console-todo-app` | **Date**: 2025-12-22 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-console-todo-app/spec.md`

---

## Summary

Build a Python console-based Todo application with in-memory storage supporting five core operations: Add, View, Update, Delete, and Toggle task status. The application follows clean architecture with strict separation of concerns across four modules (models, services, ui, main).

---

## Technical Context

**Language/Version**: Python 3.13+ (Constitution VI requirement)
**Primary Dependencies**: None - Standard library only (NFR-007)
**Storage**: In-memory list (no persistence per NFR-004)
**Testing**: Manual console testing (Phase I)
**Target Platform**: Console/Terminal (Windows/Linux/macOS)
**Project Type**: Single project (console application)
**Performance Goals**: <1 second response time (SC-007)
**Constraints**: No external packages, no persistence, single-user
**Scale/Scope**: Hundreds of tasks per session (Assumptions)

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Pre-Phase 0 Check

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. Spec-Driven Development | PASS | spec.md created and approved |
| II. Claude-Only Code | PASS | All code will be generated via Claude Code |
| III. In-Memory Architecture | PASS | No persistence planned (NFR-004) |
| IV. Clean Architecture | PASS | 4-file structure matches constitution |
| V. Spec Governance | PASS | Spec versioned, stored in specs/ |
| VI. Fixed Tech Stack | PASS | Python 3.13+, UV, Claude Code |

### Post-Phase 1 Check (Design Validation)

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. Spec-Driven Development | PASS | data-model.md traces to spec entities |
| II. Claude-Only Code | PASS | Contracts define Claude-generated code |
| III. In-Memory Architecture | PASS | TaskService uses list, no DB |
| IV. Clean Architecture | PASS | Service contracts separate from UI |
| V. Spec Governance | PASS | All artifacts in specs/001-console-todo-app/ |
| VI. Fixed Tech Stack | PASS | dataclass from stdlib only |

**GATE RESULT**: PASSED - Proceed to implementation planning

---

## Project Structure

### Documentation (this feature)

```text
specs/001-console-todo-app/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0 output (complete)
├── data-model.md        # Phase 1 output (complete)
├── quickstart.md        # Phase 1 output (complete)
├── contracts/           # Phase 1 output (complete)
│   └── service-contracts.md
├── checklists/
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
src/
├── __init__.py      # Package marker (empty)
├── main.py          # Entry point - app wiring only
├── models.py        # Task dataclass
├── services.py      # TaskService class
└── ui.py            # ConsoleUI class
```

**Structure Decision**: Single project layout per constitution Section IV. Four files exactly as mandated: main.py, models.py, services.py, ui.py.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        main.py                                   │
│  - Initialize TaskService                                        │
│  - Initialize ConsoleUI with service                            │
│  - Start UI loop                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         ui.py                                    │
│  ConsoleUI                                                       │
│  - show_menu()                                                   │
│  - get_menu_choice()                                            │
│  - handle_add_task()                                            │
│  - handle_view_tasks()                                          │
│  - handle_update_task()                                         │
│  - handle_delete_task()                                         │
│  - handle_toggle_status()                                       │
│  - run()                                                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      services.py                                 │
│  TaskService                                                     │
│  - tasks: List[Task]                                            │
│  - next_id: int                                                  │
│  - add_task(title, description) -> Task                         │
│  - get_all_tasks() -> List[Task]                                │
│  - get_task(id) -> Task | None                                  │
│  - update_task(id, title, desc) -> bool                         │
│  - delete_task(id) -> bool                                      │
│  - toggle_status(id) -> bool                                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       models.py                                  │
│  @dataclass                                                      │
│  Task                                                            │
│  - id: int                                                       │
│  - title: str                                                    │
│  - description: str = ""                                         │
│  - completed: bool = False                                       │
└─────────────────────────────────────────────────────────────────┘
```

---

## Implementation Phases

### Phase 1: Foundation
1. Create `src/` directory structure
2. Implement `models.py` with Task dataclass
3. Implement `services.py` with TaskService

### Phase 2: User Interface
4. Implement `ui.py` with ConsoleUI
5. Wire components in `main.py`

### Phase 3: Validation
6. Test all five core operations
7. Test edge cases and error handling
8. Verify constitution compliance

---

## Dependency Graph

```
models.py (no dependencies)
    │
    ▼
services.py (imports: models)
    │
    ▼
ui.py (imports: services, models)
    │
    ▼
main.py (imports: services, ui)
```

**Implementation Order**: models.py → services.py → ui.py → main.py

---

## Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Data structure | `@dataclass` | Clean, type-hinted, standard library |
| ID generation | Auto-increment | Simple, predictable, user-friendly |
| Storage | List[Task] | Simple iteration, acceptable for MVP scale |
| Validation location | Service layer | Keeps UI thin, centralizes rules |
| Error handling | Return bool/None | Simple for MVP, exceptions overkill |
| Menu style | Numbered options | Standard console pattern |

---

## Risk Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Over-engineering | Medium | High | Strict adherence to 4-file structure |
| Scope creep | Low | High | Out of Scope section in spec enforced |
| Constitution violation | Low | Critical | Pre/post gate checks in this plan |

---

## Complexity Tracking

> No violations requiring justification - all design decisions align with constitution.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |

---

## Generated Artifacts

| Artifact | Path | Status |
|----------|------|--------|
| Research | `specs/001-console-todo-app/research.md` | Complete |
| Data Model | `specs/001-console-todo-app/data-model.md` | Complete |
| Service Contracts | `specs/001-console-todo-app/contracts/service-contracts.md` | Complete |
| Quickstart Guide | `specs/001-console-todo-app/quickstart.md` | Complete |

---

## Next Steps

1. Run `/sp.tasks` to generate detailed implementation tasks
2. Execute tasks in dependency order
3. Validate against acceptance scenarios in spec.md
4. Run constitution compliance check

---

## Traceability

| Spec Requirement | Plan Component |
|------------------|----------------|
| FR-001 (Add task) | services.py: add_task() |
| FR-002 (Unique ID) | services.py: next_id counter |
| FR-003 (Default status) | models.py: completed=False |
| FR-004 (View tasks) | services.py: get_all_tasks() |
| FR-005 (Empty message) | ui.py: handle_view_tasks() |
| FR-006 (Update task) | services.py: update_task() |
| FR-007 (Delete task) | services.py: delete_task() |
| FR-008 (Toggle status) | services.py: toggle_status() |
| FR-009 (Invalid ID errors) | services.py: returns None/False |
| FR-010 (Invalid input errors) | ui.py: input validation |
| FR-011 (In-memory only) | services.py: List storage |
| FR-012 (Exit mechanism) | ui.py: menu option 6 |
| FR-013 (Text menu) | ui.py: show_menu() |
| FR-014 (Return to menu) | ui.py: run() loop |
