# Roadmap

## Current baseline: 1.4.0

The project already provides a working local-library lyrics workflow:

- API song search and metadata lookup
- version-aware local/API matching
- alias-aware matching
- duration-aware matching
- synced lyrics parsing
- ID3 SYLT embedding
- ID3 USLT fallback
- rmpc `.lrc` generation
- safe rmpc config patching
- incremental state tracking
- timestamped MP3 backups
- verification and restore
- XDG-aware config/cache/data locations
- `setup`, `sync`, `status`, `scan`, `embed`, `verify`, `restore`, `doctor`, `guide`, `search`, `info`, `config`, and `rmpc` commands

## Phase 1 — Safety net and architecture

- Keep project documentation current.
- Separate API, library, lyrics, rmpc, backup, configuration, UI, and acquisition responsibilities.
- Reduce the amount of reusable logic living in `cli.py`.
- Keep all currently working behavior intact.
- Increase unit/integration test coverage before major feature work.

## Phase 2 — Acquisition foundation

For authorized resources only:

- normalized acquisition models ✅
- resource resolution (next)
- single-item download engine ✅ (generic/authorized-resource layer)
- temporary-file downloads ✅
- atomic finalization ✅
- content/size validation ✅
- retries and resumable downloads where supported ✅
- duplicate detection (next)
- explicit overwrite policy ✅
- progress reporting ✅ (library callback; CLI UI next)
- acquisition state/job tracking ✅ (foundation models; persistent jobs next)

## Phase 3 — Bulk acquisition

- manifest files
- interactive multi-select
- bulk job summaries
- retry failed jobs
- skip already-present files
- safe parallelism only where justified
- clear per-item status and final summaries

Bulk operations should operate on explicitly selected/authorized resources, not silently crawl an entire catalogue.

## Phase 4 — Post-download library integration

After an authorized file is obtained/imported:

- match metadata
- canonicalize filename
- embed synced/plain lyrics
- generate rmpc LRC when possible
- verify
- update incremental state
- preserve backups where metadata changes occur

## Phase 5 — Browse/search frontend

- interactive browse TUI
- search results with clean metadata
- song detail screen
- filters by category and era
- random discovery
- download/import actions from the browse UI

Do not add a popularity screen unless the API exposes a reliable popularity metric.

## Phase 6 — Project rename / hub UX

Only after the core architecture is stable:

- rename the product from `juice-lyrics` toward a broader Juice WRLD API hub name
- polish the interactive frontend
- update package name, executable name, README, docs, and release notes carefully
- preserve a compatibility path for existing users where practical

## Explicitly not planned right now

- custom streaming engine
- fake lyric synchronization
- unexplained popularity rankings
- unnecessary heavyweight GUI dependencies

## Current status

- Documentation safety net established.
- Core engine modularization started; tests remain green.
- Acquisition foundation added and tested; resource resolution, duplicate detection, bulk jobs, and CLI UX remain next.
