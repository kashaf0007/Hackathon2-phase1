# Tasks: Task Organization Enhancement

**Feature**: 001-task-organization
**Branch**: `001-task-organization`
**Tests**: Required (per feature specification section 8)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1-US5)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Models**: `src/models.py`
- **Services**: `src/services.py`
- **UI**: `src/ui.py`
- **Main**: `src/main.py`
- **Unit tests**: `tests/unit/test_models.py`, `tests/unit/test_services.py`
- **Integration tests**: `tests/integration/test_cli.py`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization - add pytest for testing

- [X] T001 Add pytest>=8.0 to test dependencies in pyproject.toml
- [X] T002 [P] Create tests directory structure: tests/unit/ and tests/integration/
- [X] T003 [P] Create pytest fixtures base for TaskService in tests/unit/conftest.py

**Checkpoint**: Testing infrastructure ready - can now write tests

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Extend Task model with new fields that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Add VALID_PRIORITIES constant to src/models.py
- [X] T005 Update Task dataclass with priority field (str, default="Medium") in src/models.py
- [X] T006 Update Task dataclass with tags field (List[str], default_factory=list) in src/models.py
- [X] T007 Update Task dataclass with due_date field (Optional[datetime], default=None) in src/models.py
- [X] T008 Add import for datetime, List, Optional, field to src/models.py
- [X] T009 Implement __post_init__ method with priority validation in src/models.py

**Checkpoint**: Task model extended - all user stories can now be implemented independently

---

## Phase 3: User Story 1 - Task Prioritization (Priority: P1) 🎯 MVP

**Goal**: Allow users to assign priorities (High, Medium, Low) to tasks and see priority indicators displayed

**Independent Test**:
1. Create a task with priority "High" → task created with High priority displayed
2. Update task priority from "Medium" to "Low" → priority indicator updates to show Low
3. Attempt invalid priority value → clear error message displayed, task not updated
4. View task list → each task shows its current priority level

### Tests for User Story 1 (Required)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T010 [P] [US1] Test task creation with default priority in tests/unit/test_models.py
- [X] T011 [P] [US1] Test task creation with each valid priority in tests/unit/test_models.py
- [X] T012 [P] [US1] Test priority validation raises ValueError for invalid values in tests/unit/test_models.py
- [X] T013 [P] [US1] Test add_task with priority parameter in tests/unit/test_services.py
- [X] T014 [P] [US1] Test update_task with priority parameter in tests/unit/test_services.py
- [X] T015 [P] [US1] Test add_task validates invalid priority in tests/unit/test_services.py

### Implementation for User Story 1

- [X] T016 [US1] Update add_task signature to accept priority parameter in src/services.py
- [X] T017 [US1] Implement priority validation in add_task method in src/services.py
- [X] T018 [US1] Pass priority to Task constructor in add_task method in src/services.py
- [X] T019 [US1] Update update_task signature to accept priority parameter in src/services.py
- [X] T020 [US1] Implement priority field update logic in update_task method in src/services.py
- [X] T021 [US1] Update display_task to show priority field in src/ui.py
- [X] T022 [US1] Add get_priority helper method in src/ui.py
- [X] T023 [US1] Update handle_add_task to prompt for priority in src/ui.py
- [X] T024 [US1] Update handle_update_task to prompt for and display current priority in src/ui.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Task Categorization (Priority: P2)

**Goal**: Allow users to add tags to tasks and filter by tags

**Independent Test**:
1. Add tags "work" and "urgent" to a task → both tags are displayed
2. Remove "urgent" tag → task still displays "work" tag
3. Create task with no tags → shows no tag indicators
4. View task list → each task displays all its assigned tags

### Tests for User Story 2 (Required)

- [X] T025 [P] [US2] Test task creation with empty tags list in tests/unit/test_models.py
- [X] T026 [P] [US2] Test task creation with multiple tags in tests/unit/test_models.py
- [X] T027 [P] [US2] Test tags default to empty list when None in tests/unit/test_models.py
- [X] T028 [P] [US2] Test add_task with tags parameter in tests/unit/test_services.py
- [X] T029 [P] [US2] Test update_task with tags parameter in tests/unit/test_services.py

### Implementation for User Story 2

- [X] T030 [US2] Update add_task signature to accept tags parameter in src/services.py
- [X] T031 [US2] Pass tags to Task constructor in add_task method in src/services.py
- [X] T032 [US2] Update update_task signature to accept tags parameter in src/services.py
- [X] T033 [US2] Implement tags field update logic in update_task method in src/services.py
- [X] T034 [US2] Update display_task to show tags field in src/ui.py
- [X] T035 [US2] Add get_tags helper method in src/ui.py
- [X] T036 [US2] Update handle_add_task to prompt for tags (comma-separated) in src/ui.py
- [X] T037 [US2] Update handle_update_task to prompt for and display current tags in src/ui.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Task Search (Priority: P3)

**Goal**: Allow users to search for tasks by keywords in title and description

**Independent Test**:
1. Search for "report" → only task containing "report" displayed
2. Search for "REPORT" (case-insensitive) → tasks with "report" displayed
3. Search for non-existent keyword → no tasks, helpful message shown
4. Search for keyword in description → matching task appears in results

### Tests for User Story 3 (Required)

- [X] T038 [P] [US3] Test search with matching keyword in title in tests/unit/test_services.py
- [X] T039 [P] [US3] Test search with matching keyword in description in tests/unit/test_services.py
- [X] T040 [P] [US3] Test case-insensitive search in tests/unit/test_services.py
- [X] T041 [P] [US3] Test search with no matches returns empty list in tests/unit/test_services.py
- [X] T042 [P] [US3] Test search with empty keyword returns all tasks in tests/unit/test_services.py

### Implementation for User Story 3

- [X] T043 [US3] Implement search_tasks method in src/services.py
- [X] T044 [US3] Add case-insensitive keyword matching logic in search_tasks in src/services.py
- [X] T045 [US3] Search both title and description fields in search_tasks in src/services.py
- [X] T046 [US3] Add handle_search_tasks method in src/ui.py
- [X] T047 [US3] Update show_menu to include search option (option 6) in src/ui.py
- [X] T048 [US3] Update run method to call handle_search_tasks in src/ui.py
- [X] T049 [US3] Display result count and enhanced task list for search results in src/ui.py

**Checkpoint**: User Stories 1, 2, 3 should now be independently functional

---

## Phase 6: User Story 4 - Task Filtering (Priority: P3)

**Goal**: Allow users to filter tasks by status, priority, and tags

**Independent Test**:
1. Filter for "incomplete" tasks → only incomplete tasks displayed
2. Filter for "High" priority → only High priority tasks displayed
3. Filter by tag "work" → only tasks with "work" tag displayed
4. Apply multiple filters → only tasks matching all criteria displayed

### Tests for User Story 4 (Required)

- [X] T050 [P] [US4] Test filter by status=True in tests/unit/test_services.py
- [X] T051 [P] [US4] Test filter by status=False in tests/unit/test_services.py
- [X] T052 [P] [US4] Test filter by priority in tests/unit/test_services.py
- [X] T053 [P] [US4] Test filter by single tag in tests/unit/test_services.py
- [X] T054 [P] [US4] Test filter by multiple tags (OR logic) in tests/unit/test_services.py
- [X] T055 [P] [US4] Test filter by multiple criteria (status + priority + tags) in tests/unit/test_services.py
- [X] T056 [P] [US4] Test filter with all None returns all tasks in tests/unit/test_services.py
- [X] T057 [P] [US4] Test filter with conflicting criteria returns empty list in tests/unit/test_services.py

### Implementation for User Story 4

- [X] T058 [US4] Implement filter_tasks method in src/services.py
- [X] T059 [US4] Implement status filtering logic in filter_tasks in src/services.py
- [X] T060 [US4] Implement priority filtering logic in filter_tasks in src/services.py
- [X] T061 [US4] Implement tags filtering logic (ANY match) in filter_tasks in src/services.py
- [X] T062 [US4] Add handle_filter_tasks method in src/ui.py
- [X] T063 [US4] Implement filter menu with 8 options in src/ui.py
- [X] T064 [US4] Implement single filter logic (options 1-6) in handle_filter_tasks in src/ui.py
- [X] T065 [US4] Implement multi-filter logic (option 8) in handle_filter_tasks in src/ui.py
- [X] T066 [US4] Update show_menu to include filter option (option 7) in src/ui.py
- [X] T067 [US4] Update run method to call handle_filter_tasks in src/ui.py
- [X] T068 [US4] Display filtered count and enhanced task list in src/ui.py

**Checkpoint**: User Stories 1, 2, 3, 4 should now be independently functional

---

## Phase 7: User Story 5 - Task Sorting (Priority: P4)

**Goal**: Allow users to sort tasks by due date, priority, or title

**Independent Test**:
1. Sort by due date ascending → tasks displayed earliest to latest
2. Sort by due date descending → tasks displayed latest to earliest
3. Sort by priority descending → tasks: High, Medium, Low
4. Sort alphabetically → tasks in alphabetical order
5. Sort by due date with None values → tasks without dates at end

### Tests for User Story 5 (Required)

- [X] T069 [P] [US5] Test sort by due_date ascending in tests/unit/test_services.py
- [X] T070 [P] [US5] Test sort by due_date descending in tests/unit/test_services.py
- [X] T071 [P] [US5] Test sort by priority descending (High->Medium->Low) in tests/unit/test_services.py
- [X] T072 [P] [US5] Test sort by priority ascending (Low->Medium->High) in tests/unit/test_services.py
- [X] T073 [P] [US5] Test sort by title ascending in tests/unit/test_services.py
- [X] T074 [P] [US5] Test sort handles None due_date values (places at end) in tests/unit/test_services.py
- [X] T075 [P] [US5] Test sort with invalid by parameter raises ValueError in tests/unit/test_services.py
- [X] T076 [P] [US5] Test sort with invalid order parameter raises ValueError in tests/unit/test_services.py

### Implementation for User Story 5

- [X] T077 [US5] Implement sort_tasks method in src/services.py
- [X] T078 [US5] Add PRIORITY_ORDER constant (High=2, Medium=1, Low=0) to src/services.py
- [X] T079 [US5] Implement due_date sorting with None values at end in sort_tasks in src/services.py
- [X] T080 [US5] Implement priority sorting using PRIORITY_ORDER in sort_tasks in src/services.py
- [X] T081 [US5] Implement title sorting (case-insensitive) in sort_tasks in src/services.py
- [X] T082 [US5] Add validation for by and order parameters in sort_tasks in src/services.py
- [X] T083 [US5] Add handle_sort_tasks method in src/ui.py
- [X] T084 [US5] Implement sort menu (by: due_date/priority/title, order: asc/desc) in src/ui.py
- [X] T085 [US5] Update show_menu to include sort option (option 8) in src/ui.py
- [X] T086 [US5] Update run method to call handle_sort_tasks in src/ui.py
- [X] T087 [US5] Display sorted count and enhanced task list in src/ui.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Integration testing, display enhancements, and final polish

- [X] T088 [P] Add due date field to Task model (depends on US1 completion) in src/models.py
- [X] T089 [P] Update add_task to accept due_date parameter in src/services.py
- [X] T090 [P] Update update_task to accept due_date parameter in src/services.py
- [X] T091 Add get_due_date helper method in src/ui.py
- [X] T092 Update handle_add_task to prompt for due date in src/ui.py
- [X] T093 Update handle_update_task to prompt for and display current due date in src/ui.py
- [X] T094 Update display_task to show due_date in enhanced format in src/ui.py
- [X] T095 Update show_menu to include Exit option 9 (reordered) in src/ui.py
- [X] T096 Add test for due_date creation in tests/unit/test_models.py
- [X] T097 Add test for due_date validation in tests/unit/test_models.py
- [X] T098 [P] Add test for add_task with due_date in tests/unit/test_services.py
- [X] T099 [P] Add test for update_task with due_date in tests/unit/test_services.py
- [X] T100 Add test for handle_add_task CLI flow in tests/integration/test_cli.py
- [X] T101 [P] Add test for handle_update_task CLI flow in tests/integration/test_cli.py
- [X] T102 [P] Add test for handle_search_tasks CLI flow in tests/integration/test_cli.py
- [X] T103 [P] Add test for handle_filter_tasks CLI flow in tests/integration/test_cli.py
- [X] T104 [P] Add test for handle_sort_tasks CLI flow in tests/integration/test_cli.py
- [X] T105 Run all tests to verify 90%+ coverage
- [X] T106 Validate quickstart.md scenarios work end-to-end
- [X] T107 Code cleanup and remove any debug prints

**Checkpoint**: Feature complete, tested, and ready for deployment

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - US1 (Priority) can start after Foundational
  - US2 (Tags) can start after Foundational
  - US3 (Search) can start after Foundational
  - US4 (Filter) can start after Foundational
  - US5 (Sort) can start after Foundational
  - User stories can proceed in priority order: P1 → P2 → P3 → P3 → P4
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational - No dependencies on other stories
- **User Story 3 (P3)**: Can start after Foundational - No dependencies on other stories
- **User Story 4 (P3)**: Can start after Foundational - Uses extended Task model but independent of US1/US2/US3
- **User Story 5 (P4)**: Can start after Foundational - Sorts existing tasks, independent of other stories

### Within Each User Story

- Tests MUST be written and FAIL before implementation (TDD approach)
- Model tasks before service tasks
- Service tasks before UI tasks
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- **Setup Phase**: T001, T002, T003 can run in parallel
- **Foundational Phase**: T004-T009 must run sequentially (same file)
- **Within Each User Story Tests**: All [P] marked test tasks can run in parallel
- **Within User Story 1**: T016, T021, T022 can run in parallel (different files)
- **Within User Story 2**: T030, T034, T035 can run in parallel (different files)
- **Within User Story 3**: T046-T049 can run in parallel (different files)
- **Within User Story 4**: T062-T068 can run in parallel (different files)
- **Within User Story 5**: T083-T087 can run in parallel (different files)
- **Polish Phase**: T088, T089, T090, T096, T097, T098, T099 can run in parallel
- **User Stories**: Once Foundational is done, all user stories can proceed in parallel by different developers

---

## Parallel Example: User Story 1 Tests

```bash
# Launch all tests for User Story 1 together (run in parallel):
pytest tests/unit/test_models.py -k "priority"
pytest tests/unit/test_services.py -k "priority"
```

## Parallel Example: User Story 1 UI Tasks

```bash
# Launch UI updates in parallel (different files):
# Developer A: Update display_task in src/ui.py
# Developer B: Add get_priority helper in src/ui.py
# Developer C: Update handle_add_task in src/ui.py
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Foundational (T004-T009) - CRITICAL
3. Complete Phase 3: User Story 1 - Task Prioritization (T010-T024)
4. **STOP and VALIDATE**: Test User Story 1 independently
   - Create tasks with different priorities
   - Update priorities
   - Verify invalid values are rejected
   - View task list with priority indicators
5. Demo MVP: Task prioritization is working

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → MVP ready
3. Add User Story 2 → Test independently → Categorization available
4. Add User Story 3 → Test independently → Search available
5. Add User Story 4 → Test independently → Filtering available
6. Add User Story 5 → Test independently → Sorting available
7. Complete Polish Phase → Full feature complete
8. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup (T001-T003) and Foundational (T004-T009) together
2. Once Foundational is done:
   - Developer A: User Story 1 (Task Prioritization) - T010-T024
   - Developer B: User Story 2 (Task Categorization) - T025-T037
   - Developer C: User Story 3 (Task Search) - T038-T049
3. After P1-P3 complete:
   - Developer A: User Story 4 (Task Filtering) - T050-T068
   - Developer B: User Story 5 (Task Sorting) - T069-T087
4. Team completes Polish Phase (T088-T107) together
5. Stories complete and integrate independently

---

## MVP Scope Recommendation

**MVP = User Story 1 Only (Task Prioritization)**
- Total tasks for MVP: 24 tasks (T001-T024)
- Includes: Setup (3), Foundational (6), US1 (15)
- Delivers: Priority assignment and display
- Testable independently
- Incremental value without full feature scope

**Full Feature**: All 5 user stories + Polish = 107 tasks

---

## Task Count Summary

- **Phase 1 - Setup**: 3 tasks
- **Phase 2 - Foundational**: 6 tasks
- **Phase 3 - US1 (Priority)**: 15 tasks
- **Phase 4 - US2 (Tags)**: 13 tasks
- **Phase 5 - US3 (Search)**: 12 tasks
- **Phase 6 - US4 (Filter)**: 19 tasks
- **Phase 7 - US5 (Sort)**: 19 tasks
- **Phase 8 - Polish**: 20 tasks
- **Total**: 107 tasks

**MVP (US1 only)**: 24 tasks

---

## Notes

- [P] tasks = different files, no dependencies on incomplete tasks
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (TDD approach)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Due date integration spread across Foundational + Polish phases for modularity
- All test files created in Setup phase to avoid file conflicts
