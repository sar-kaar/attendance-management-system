# Database Standards — Attendance Management System

> **Purpose:** Conventions for schema design, migrations, and data operations going forward. For the actual current schema, see [database-schema.md](database-schema.md) and [architecture.md](architecture.md#data-model).
> **Scope:** Django ORM models/migrations across all apps.
> **Last updated:** 2026-07-26 · **Version:** 1.0

## Table of Contents

- [Naming Conventions](#naming-conventions)
- [Migration Strategy](#migration-strategy)
- [Indexes](#indexes)
- [Constraints & Relationships](#constraints--relationships)
- [Soft Deletes](#soft-deletes)
- [Audit Tables](#audit-tables)
- [Backups](#backups)
- [Seed Data](#seed-data)
- [Performance](#performance)

## Naming Conventions

- Table names: Django default (`<app_label>_<modelname>`, lowercase) — don't override with `db_table` unless there's a specific reason (e.g., aligning with a legacy table), and document that reason in the model's docstring.
- Field names: `snake_case`, matching the existing codebase.
- Foreign keys: named after the referenced concept, not the table (`faculty` FK to `User`, not `user_id_2`) — matches `courses_course.faculty`.
- Boolean fields: `is_<adjective>` / `has_<noun>` (`is_active`, `has_face_encoding`).
- Timestamps: `created_at`/`updated_at` for new models (not yet consistently present on all existing models — add on new models going forward, don't retrofit existing ones without a reason).

## Migration Strategy

- Every model change ships with a migration in the same commit — CI already gates this (`manage.py makemigrations --check`), see [rules.md](rules.md).
- **Additive-first for production-affecting changes**: add a new nullable/defaulted column, backfill, then make it required in a follow-up migration — don't add a `NOT NULL` column with no default against a table that already has rows, since SQLite/Postgres will require a default or fail (this is DRF/Django-enforced already, but the *sequencing* across multiple migrations for a safe rollout is a team discipline, not something the tool enforces).
- **Destructive migrations** (dropping a column/table, renaming — Django treats a rename as drop+add unless using `RenameField`) require a call-out in the PR description and, for anything touching a table with real production data, a `manage.py migrate --plan` dry run mentioned in the PR — see [deployment.md](deployment.md) Deployment Checklist.
- **Data migrations** (populating a new field from existing data) are separate migration files from schema migrations — don't mix `AddField` and a `RunPython` data backfill in one migration if the backfill could plausibly fail; keeping them separate lets the schema change land even if the backfill needs a retry.
- Never edit a migration file that has already been applied to any shared environment (CI/prod) — write a new migration instead, even to fix a mistake in a previous one.

## Indexes

- Add an explicit index (`db_index=True` or a `Meta.indexes` entry) on any field used in a `filter()`/`get()` in a hot path — notably anything used in [api-standards.md](api-standards.md) filtering/search query params.
- Composite unique constraints already in use (`(student, course, date)` on `Attendance`, `(student, course)` on `Enrollment`) are the reference pattern for any new "prevent duplicate" requirement — use `Meta.constraints` with `UniqueConstraint`, not a manual `validate()` check alone (the DB constraint is the actual guarantee; the serializer check is the friendly error message).
- Don't index every field speculatively — an index has a write-cost; add it when a real query pattern needs it, not preemptively for every FK (Django already indexes FKs by default).

## Constraints & Relationships

- Prefer a DB-level constraint (`UniqueConstraint`, `CheckConstraint`, `on_delete` policy) over an application-level-only check wherever the constraint is expressible in the ORM — the DB constraint holds even if application code has a bug; the reverse isn't true.
- `on_delete` policy must be a deliberate choice, documented if non-obvious: `SET_NULL` for `Course.faculty` (a course shouldn't vanish if the faculty account is deleted) is the existing pattern; default to `CASCADE` only when the child genuinely has no meaning without the parent (e.g., `Enrollment` without a `Course`).
- The known `Student` ↔ `accounts.User` gap (not FK-linked today, see [architecture.md](architecture.md)) should not be replicated in new models — if a new feature needs to link a login-account concept to a domain-record concept, FK them directly unless there's a specific reason not to (and if there is, document it in [decisions.md](decisions.md) the way this existing gap should be, per [memory.md](memory.md) Technical Debt).

## Soft Deletes

- **Not currently used anywhere in the schema** — all deletes today are hard deletes.
- **Recommendation for new sensitive-data models**: where "who was deleted and when" matters for audit/dispute purposes (e.g., a future `AttendanceRecord` correction history), use a soft-delete field (`deleted_at`, nullable) rather than a hard delete, and filter it out via a custom manager — don't apply this to every model by default; hard delete is simpler and correct for genuinely disposable data (e.g., an expired OTP code).

## Audit Tables

- **Not currently implemented.** No table tracks who changed an `Attendance`/`Enrollment`/`User` record or when, beyond Django admin's built-in `LogEntry` (which only covers admin-panel actions, not API writes).
- **Recommendation**: a generic audit log (actor, action, model, object id, timestamp, diff) using either `django-simple-history` (per-model history tables, easy to query "history of this record") or a single generic `AuditLog` table (simpler schema, harder to query per-record history) — evaluate against actual need before adding; this is real schema/write overhead and should be scoped to the models where dispute resolution genuinely matters (attendance, grades-adjacent data), not applied blanket across every table.

## Backups

- Production: PostgreSQL via Azure's managed offering — rely on the platform's automated backup/point-in-time-restore feature; confirm it's actually enabled on the resource (not assumed) as part of onboarding any new environment.
- Before any destructive migration or major-version DB upgrade, take a manual `pg_dump` in addition to relying on automated backups — see [tech-stack.md](tech-stack.md) Database upgrade strategy.
- Local dev (`db.sqlite3`): never a backup source of truth — it's disposable, gitignored, and regenerated via `migrate`.

## Seed Data

- No formal seed-data/fixture system is in place today. `manage.py createsuperuser` plus manual admin-panel entry is the current bootstrap path for a fresh environment.
- **Recommendation**: a `manage.py` management command (or Django fixtures) that seeds a minimal realistic dataset (a few students/courses/enrollments) for local dev and CI — reduces new-contributor setup friction ([contributing.md](contributing.md)) and gives integration tests a consistent baseline. Scope this as a phases.md task rather than doing it as a drive-by change.

## Performance

- N+1 queries: use `select_related`/`prefetch_related` on any view returning a list with related-object fields (e.g., attendance list including student/course names) — check with `django-debug-toolbar` in dev if a list endpoint feels slow before assuming it's a DB-tier problem.
- Dashboard aggregation endpoints (`dashboard` app — stats, at-risk detection, chronic-latecomer detection) are the most query-heavy part of the system; any new aggregation should be reviewed for query count (`assertNumQueries` in tests is a reasonable guard, see [testing-strategy.md](testing-strategy.md)) before merge.
- Pagination (see [api-standards.md](api-standards.md)) is itself a performance control — an unbounded list endpoint against a growing `Attendance` table is the most likely first real performance problem this system will hit.
