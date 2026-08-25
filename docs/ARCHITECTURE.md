# Architecture

## Design goal

Keep the application lightweight and easy to use while preventing the CLI from becoming a giant module that owns every responsibility.

The user-facing CLI should be a thin layer over reusable services.

## Desired dependency direction

```text
CLI / TUI
   |
   +--> API
   +--> Library
   +--> Lyrics
   +--> rmpc
   +--> Acquisition
   +--> Backup
   +--> Config
```

Reusable modules should not import application commands from `cli.py` merely to reuse helper functions.

## API layer

Responsibilities:

- HTTP requests
- API base URL handling
- timeouts
- retry behavior
- search
- song lookup
- pagination
- response normalization
- caching

The API layer should not know about terminal prompts, MP3 tagging, or rmpc UI.

## Library layer

Responsibilities:

- scan local MP3s
- extract metadata
- duration handling
- fingerprints/state
- duplicate detection
- matching local files to API records
- incremental sync decisions

Matching must remain version-aware, alias-aware, and duration-aware.

## Lyrics layer

Responsibilities:

- parse API LRC-style `synced_lyrics`
- produce SYLT frames
- produce USLT frames
- verify lyric frames
- write plain `.lrc` text when synchronized lyrics exist

It must never manufacture timestamps for plain lyrics.

## rmpc layer

Responsibilities:

- generate `.lrc` files for synced lyrics
- locate/configure the user's rmpc config safely
- preserve unrelated rmpc settings/layout/keybinds
- trigger lyric re-indexing where supported
- provide diagnostics

## Backup layer

Responsibilities:

- timestamped backups
- manifests
- restore
- rollback after verification failures

## Configuration layer

Responsibilities:

- XDG config paths
- persistent settings
- validation
- default values

Do not hard-code a particular user's home directory.

## State layer

Track enough information to skip unchanged files safely.

State should include a local file identity/fingerprint and enough processing information to know whether lyrics/rmpc output are current.

Losing state must be recoverable: the application should be able to rescan and reconstruct it.

## Acquisition layer

Responsibilities:

- search result/resource models
- explicit resource selection
- authorized download/import
- manifests
- job state
- progress
- temporary files
- validation
- retry/resume
- duplicate handling

Acquisition should not directly perform lyric embedding or rmpc configuration. It should hand successful local files back to the library/post-processing workflow.

## CLI layer

Responsibilities:

- parse arguments
- choose commands
- call services
- render friendly output
- collect explicit user confirmation where needed

Normal user commands should be easy to remember.

## UI layer

Long term, an interactive TUI can sit on top of the same services.

The TUI must not contain the business logic itself. This allows both:

- `juice-lyrics search ...`
- interactive browse UI

to use the same API and acquisition code.

## Important existing behaviors to preserve

- explicit version matching
- known aliases
- duration matching
- SYLT first / USLT fallback
- rmpc `.lrc` generation only for synced lyrics
- backups before MP3 metadata changes
- verification after writes
- incremental sync


## Acquisition milestone
The acquisition package currently provides generic, explicitly-authorized resource primitives:

- `models.py` for item/result/job-state data
- `manifests.py` for explicit selection manifests
- `downloader.py` for safe HTTPS transport, temporary files, optional resume, retries, validation, and atomic finalization

It intentionally does not resolve or crawl a particular media archive. Resource resolution will be a separate step that hands an explicitly selected resource to the downloader.

## Current refactor milestone
The CLI remains the user-facing entrypoint, but reusable functionality now has dedicated modules under `api/`, `library/`, `lyrics/`, `rmpc/`, `backup/`, `config/`, and `state.py`. Compatibility adapters in `cli.py` preserve the existing command behavior while the codebase transitions away from a monolithic implementation.
