# MangaBook V2 — Functional parity roadmap

> Statut : roadmap de parité fonctionnelle clôturée.
>
> Les principales fonctionnalités V1 attendues ont été restaurées ou remplacées par une version V2 testée.
> La suite du projet est suivie dans `docs/V2_OPTIMIZATION_ROADMAP.md`.

---

## Project decision

The public design was frozen during the V1/V2 parity phase. This phase focused on restoring missing V1 features in the cleaner V2 architecture, while keeping tests, CI and documentation aligned.

The active project phase is now quality optimization, security hardening, cleanup and RNCP preparation.

---

## Branch

Historical branch:

```text
feature/functionality-parity-v1-v2
```

Current documentation synchronization branch:

```text
docs/sync-project-documentation
```

---

## Checklist

| Step | Status | Summary | Expected validation |
| --- | --- | --- | --- |
| 1 | Done | Save the functional roadmap in `docs/`. | Documentation commit and PR. |
| 2 | Done | Restore full user registration. | Auth route and service tests. |
| 3 | Done | Add cart and help/contact pages with V1 compatibility routes. | Public route tests. |
| 4 | Done | Add safe catalog sorting. | Public service and route tests. |
| 5 | Done | Restore complete goodies grouping. | Public service and template tests. |
| 6 | Done | Add JSON favorite toggle. | JSON and auth tests. |
| 7 | Done | Complete missing admin workflows. | Admin tests. |
| 8 | Done | Final stabilization. | Green local validation and CI. |

---

## Functional parity result

### Public

- Home sections restored or adapted in V2.
- Catalog sorting added with safe allowlist mapping.
- Favorite JSON toggle added.
- Planning available.
- Profile, favorites and history available.
- Forum available and modernized.
- Goodies grouping restored.
- Cart page and backend cart synchronization added.
- Help/contact content regrouped into the about page.
- Article detail and history available.

### Auth

- Login available.
- Logout available and handled through POST.
- Full registration workflow restored.
- User/admin guards available.

### Admin

- Dashboard improved.
- Articles workflow available.
- Orders workflow added and test-covered.
- Users workflow added and test-covered.
- Contact deletion added.
- Admin forum reply added.
- Forum moderation available.

---

## Validation target

```bash
python -m ruff format --check .
python -m ruff check .
python -m compileall app tests
python -m pytest
```

Dernière validation locale connue :

```text
Python 3.14.3
Ruff format : OK
Ruff check : OK
Compileall : OK
Pytest : 226 passed
Coverage : 93%
```

---

## Step summaries

### Step 1

Status: done.

Summary: add the functional roadmap file and open the tracking PR.

### Step 2

Status: done.

Summary: restore the full registration workflow with service-level validation and tests.

### Step 3

Status: done.

Summary: add cart/help/contact pages and legacy-compatible redirects or aliases.

### Step 4

Status: done.

Summary: extend catalog query handling with safe sort mapping.

### Step 5

Status: done.

Summary: restore V1 goodies sections while keeping V2 services.

### Step 6

Status: done.

Summary: add a progressive JSON favorite toggle.

### Step 7

Status: done.

Summary: complete missing admin workflows in focused batches.

### Step 8

Status: done.

Summary: final check, CI review and merge readiness.

---

## Next project phase

The next project phase is tracked in:

```text
docs/V2_OPTIMIZATION_ROADMAP.md
```

Main remaining work:

1. synchronize documentation ;
2. harden configuration and security ;
3. refactor admin services ;
4. add CSRF protection ;
5. strengthen DB/migrations ;
6. finalize SEO/accessibility/smoke tests ;
7. clean unused files ;
8. prepare RNCP evidence.
