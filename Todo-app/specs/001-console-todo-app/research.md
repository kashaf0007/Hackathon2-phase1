# Research: Python In-Memory Console Todo Application

**Feature**: 001-console-todo-app
**Date**: 2025-12-22
**Status**: Complete

## Overview

This document consolidates research findings for the Python In-Memory Console Todo Application Phase I MVP. All technical decisions are derived from the constitution and specification requirements.

---

## Technical Decisions

### 1. Language and Runtime

**Decision**: Python 3.13+ with UV runtime

**Rationale**:
- Constitution mandates Python 3.13+ (Section VI: Fixed Tech Stack)
- UV runtime provides fast dependency resolution and execution
- Standard library only - no external packages (NFR-007)

**Alternatives Considered**:
- None - technology stack is fixed per constitution

---

### 2. Project Structure

**Decision**: Four-file architecture under `/src`

```
src/
├── main.py      # Entry point - app wiring only
├── models.py    # Task data model
├── services.py  # Business logic (TaskService)
└── ui.py        # Console I/O
```

**Rationale**:
- Constitution Section IV mandates this exact structure
- Clean separation of concerns required
- No business logic permitted in UI layer

**Alternatives Considered**:
- Single-file implementation - rejected (violates constitution)
- Additional modules - rejected (over-engineering for MVP)

---

### 3. Data Model Design

**Decision**: Simple Task dataclass with four attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| id | int | Unique, stable, auto-incremented |
| title | str | Required, non-empty |
| description | str | Optional (empty string default) |
| completed | bool | Default False ("Incomplete") |

**Rationale**:
- Spec defines exactly these four attributes (Key Entities section)
- Dataclass provides clean, immutable-friendly structure
- No additional fields to maintain MVP scope

**Alternatives Considered**:
- Named tuple - rejected (less readable, harder to update)
- Plain dict - rejected (no type hints, error-prone)
- Class with methods - rejected (models should be data-only per user input)

---

### 4. Storage Pattern

**Decision**: In-memory list with ID counter in TaskService

**Rationale**:
- Constitution Section III mandates in-memory only
- NFR-004: No file/database persistence
- Simple list provides O(n) lookup acceptable for MVP scale (hundreds of tasks)

**Alternatives Considered**:
- Dict with ID keys - viable but list is simpler for iteration
- External storage - rejected (explicit constraint)

---

### 5. ID Generation Strategy

**Decision**: Auto-incrementing integer starting at 1

**Rationale**:
- Spec assumption: "Task IDs will be simple incrementing integers starting from 1"
- Stable throughout session (FR-002)
- Simple and predictable for users

**Alternatives Considered**:
- UUID - rejected (overkill for single-session, user-unfriendly)
- Random integers - rejected (not user-friendly)

---

### 6. Input Validation Strategy

**Decision**: Validate at service layer with clear error returns

| Input | Validation Rule | Error Response |
|-------|-----------------|----------------|
| Title | Non-empty after strip() | "Task title cannot be empty" |
| Task ID | Positive integer | "Invalid ID format" or "Task not found" |
| Menu choice | Valid option number | "Invalid option" |

**Rationale**:
- FR-009, FR-010 require graceful error handling
- Service layer validation keeps UI thin
- Clear, actionable error messages (SC-006)

**Alternatives Considered**:
- UI-only validation - rejected (violates separation of concerns)
- Exception-based - viable but return values simpler for this scale

---

### 7. Console UI Pattern

**Decision**: Menu-driven loop with numbered options

```
=== Todo Application ===
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Toggle Status
6. Exit
```

**Rationale**:
- FR-013: Clear text-based menu required
- Numbered options are standard console UX
- FR-014: Return to menu after each operation

**Alternatives Considered**:
- Command-line arguments - rejected (spec requires interactive menu)
- Sub-menus - rejected (over-engineering for 5 features)

---

### 8. Testing Strategy

**Decision**: Manual testing via console for Phase I

**Rationale**:
- No testing framework specified in requirements
- Standard library only constraint (NFR-007)
- Acceptance scenarios provide test cases

**Alternatives Considered**:
- unittest - viable but not required for MVP
- pytest - rejected (external dependency)

---

## Best Practices Applied

### Python Standard Library Patterns

1. **dataclasses** - Clean model definition with `@dataclass`
2. **typing** - Type hints for clarity (`Optional[str]`, `List[Task]`)
3. **Built-in input/print** - Standard console I/O

### Clean Code Principles

1. **Single Responsibility** - Each file has one purpose
2. **Dependency Injection** - Service passed to UI
3. **Early Returns** - Validate first, then proceed
4. **Descriptive Names** - `add_task()`, `toggle_status()`, not `add()`, `toggle()`

---

## Risk Mitigations

| Risk | Mitigation |
|------|------------|
| ID collision | Counter never decrements, even on delete |
| Empty title bypass | Strip whitespace before validation |
| Invalid menu input | Catch ValueError, show error, re-prompt |
| Large task count | Acceptable per assumptions (hundreds) |

---

## Conclusion

All technical decisions are fully specified by the constitution and spec. No NEEDS CLARIFICATION items remain. The implementation can proceed to Phase 1 design artifacts.

**Next Step**: Generate data-model.md and contracts
