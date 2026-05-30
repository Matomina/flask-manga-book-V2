# MangaBook V2 — Functional parity roadmap

## Project decision

The current public design is frozen. This phase focuses on functional parity between V1 and V2, then cleanup, tests, security and final polish.

## Branch

`feature/functionality-parity-v1-v2`

## Checklist

| Step | Status | Summary | Expected validation |
| --- | --- | --- | --- |
| 1 | In progress | Save the functional roadmap in `docs/`. | Documentation commit and PR. |
| 2 | Todo | Restore full user registration. | Auth route and service tests. |
| 3 | Todo | Add cart and help pages with V1 compatibility routes. | Public route tests. |
| 4 | Todo | Add safe catalog sorting. | Public service and route tests. |
| 5 | Todo | Restore complete goodies grouping. | Public service and template tests. |
| 6 | Todo | Add JSON favorite toggle. | JSON and auth tests. |
| 7 | Todo | Complete missing admin workflows. | Admin tests. |
| 8 | Todo | Final stabilization. | Green CI. |

## Functional gaps

### Public

- Home sections from V1: partial in V2.
- Catalog sorting: missing in V2.
- Favorite JSON toggle: missing in V2.
- Planning: present in V2.
- Profile summary: split in V2.
- Forum: present in V2.
- Goodies grouping: simplified in V2.
- Cart page: missing in V2.
- Help page: missing in V2.
- Article detail and history: present in V2.

### Auth

- Login: present in V2.
- Logout: present in V2.
- Full registration workflow: missing in V2.
- User/admin guards: present in V2.

### Admin

- Dashboard: improved in V2.
- Articles workflow: present in V2.
- Orders workflow: partial in V2.
- Users workflow: partial in V2.
- Contact deletion: missing in V2.
- Admin forum reply: missing in V2.

## Validation target

```bash
python -m compileall app tests
python -m ruff check .
python -m pytest
```

## Step summaries

### Step 1

Status: in progress.

Summary: add this roadmap file and open the tracking PR.

### Step 2

Status: todo.

Summary: restore the full registration workflow with service-level validation and tests.

### Step 3

Status: todo.

Summary: add cart/help pages and legacy-compatible redirects or aliases.

### Step 4

Status: todo.

Summary: extend catalog query handling with safe sort mapping.

### Step 5

Status: todo.

Summary: restore V1 goodies sections while keeping V2 services.

### Step 6

Status: todo.

Summary: add a progressive JSON favorite toggle.

### Step 7

Status: todo.

Summary: complete missing admin workflows in focused batches.

### Step 8

Status: todo.

Summary: final check, CI review and merge readiness.
