# Changelog

## Unreleased

### Architecture
- Began separating reusable engine code from the CLI entrypoint.
- Added dedicated API, library matching/scanning, lyrics, rmpc, backup, config, and state modules.
- Kept the existing CLI commands compatible through adapters so the refactor does not change the normal user workflow.

### Validation
- Existing test suite remains green: 4 tests passed.

## Unreleased — Acquisition foundation

- Added an isolated `acquisition/` package for explicitly authorized media resources.
- Added acquisition item/result/state models.
- Added safe manifest parsing for explicit selections.
- Added a generic HTTPS downloader with temporary `.part` files, retries, optional resume, size/checksum validation, maximum-size protection, and atomic finalization.
- Added acquisition foundation tests.
- Kept the acquisition layer independent from the lyrics/rmpc post-processing pipeline.
