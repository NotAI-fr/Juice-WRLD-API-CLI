# Project Context

This file preserves the human/project context that is useful when continuing development in a new chat or with another coding agent.

## User / environment context

- Primary OS: Arch Linux.
- The user prefers lightweight Linux tools and CLI/TUI workflows.
- The user uses MPD + rmpc for music playback.
- The user is comfortable running commands, but is not a Python developer and should not be expected to understand implementation details to use the project.
- Prefer straightforward commands, friendly output, sensible defaults, and safe automation.
- Do not make the user manage complicated development workflows for normal use.

## Music setup

Default local library:

`~/Music/Juice WRLD/Unreleased`

Default rmpc lyric directory:

`~/Music/Juice WRLD/lyrics`

The actual paths must remain configurable and portable; these are defaults only.

## Existing proven behavior

The 1.4.0 release was tested against a 35-song local library:

- 35/35 API matches
- 18 songs with synchronized lyrics
- 17 songs with plain lyrics only
- 18 rmpc LRC files generated
- 35/35 lyric embeddings verified
- version-aware matching works for v1/v2 tracks
- backups and restore work
- rmpc integration works

## Lyrics decisions

- Prefer API `synced_lyrics`.
- Synced lyrics are embedded as ID3 SYLT.
- Synced lyrics also produce `.lrc` files for rmpc.
- If only API `lyrics` exists, embed them as ID3 USLT.
- Do not invent timestamps or fake-sync plain lyrics.
- rmpc's Lyrics pane is intended for synced `.lrc` lyrics, so plain-only tracks may not display there.

## rmpc decisions

Keep MPD + rmpc as the primary playback setup.

Reasons:

- lightweight background playback
- TUI workflow
- low resource usage
- strong customization

Do not replace rmpc just because some tracks have plain rather than synced lyrics.

## Project direction

The project should gradually evolve from a lyrics utility into a polished Juice WRLD API frontend/hub while retaining the useful CLI underneath.

Long-term ideas:

- interactive browse TUI
- API search and discovery
- single-song acquisition/import for authorized resources
- bulk acquisition from explicit user-selected manifests/jobs
- richer library management
- better user-facing UX

Explicitly deprioritized/out of scope for now:

- custom streaming system
- popularity rankings unless the API clearly exposes a useful metric
- automatic audio/lyric alignment as a default feature

## UX philosophy

Normal users should mainly need:

- `juice-lyrics setup` once
- `juice-lyrics sync` for normal maintenance
- `juice-lyrics status` to check health
- `juice-lyrics search` / `info` for discovery
- `juice-lyrics guide` when unsure what to do
- `juice-lyrics doctor` for troubleshooting

Advanced commands can remain available without being required for ordinary use.

## Continuity rule

Before making large architectural changes, read this file together with `docs/ROADMAP.md` and `docs/ARCHITECTURE.md`.

Update this file when a major user-facing decision changes the project's direction or priorities.
