# Development Guide

## Baseline

The 1.4.0 release is the known-good functional baseline.

Run the tests with:

```bash
pytest -q
```

The baseline test suite includes core parsing and rmpc configuration/LRC checks.

## Before changing architecture

Read:

1. `PROJECT_CONTEXT.md`
2. `docs/ROADMAP.md`
3. `docs/ARCHITECTURE.md`

Then inspect the current implementation and tests.

## Change strategy

Prefer incremental, reviewable changes.

For large work:

1. refactor one responsibility
2. run tests
3. commit
4. implement the next responsibility
5. run tests again

Do not rewrite working behavior without a clear reason.

## Testing expectations

Do not make unit tests depend on the live Juice WRLD API.

Use fixed/mock API responses for deterministic tests.

New components should receive focused tests before being integrated into the main sync workflow.

## Packaging

The project uses `pyproject.toml` and exposes the `juice-lyrics` console script.

Keep the runtime dependency set small.

## GitHub workflow

GitHub should be the main source of truth for ongoing development.

The 1.4.0 archive is the known-good baseline. New work should be committed in logical milestones so changes can be inspected or reverted independently.


## Checkpoint workflow

Development checkpoints are distributed as source ZIPs. When applying one to a local Git checkout, keep `.git/` untouched, run the test suite, then commit the result as a single logical milestone.
