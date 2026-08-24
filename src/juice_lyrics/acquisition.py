"""
Acquisition module for authorized media download and import.

Handles:
- Search with resource availability
- Download from approved sources
- Import from local files
- Duplicate detection
- Manifest-based bulk operations
"""

import hashlib
import json
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from . import __version__


def search_with_resources(settings: Any, query: str) -> list[dict[str, Any]]:
    """
    Search the API for songs with resource availability information.
    
    Returns songs with additional fields:
    - has_synced_lyrics
    - has_plain_lyrics
    - resource_available (placeholder for future expansion)
    """
    from .cli import search_api_advanced
    
    data = search_api_advanced(settings, query)
    results = data.get("results", [])
    
    for song in results:
        synced = bool(str(song.get("synced_lyrics") or "").strip())
        plain = bool(str(song.get("lyrics") or "").strip())
        song["has_synced_lyrics"] = synced
        song["has_plain_lyrics"] = plain
        # Placeholder for future resource availability
        song["resource_available"] = False
    
    return results


def sha256_file(path: Path) -> str:
    """Calculate SHA256 hash of a file."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def detect_duplicate(settings: Any, candidate: dict[str, Any], target_dir: Path) -> dict[str, Any]:
    """
    Check if a song already exists in the library.
    
    Returns a dict with:
    - status: "new", "exact_duplicate", "different_version", "possible_duplicate"
    - existing_file: Path if found
    - reason: explanation
    """
    from .cli import normalize, strip_version, parse_version
    
    if not target_dir.is_dir():
        return {"status": "new", "existing_file": None, "reason": "Target directory empty"}
    
    candidate_title = normalize(strip_version(str(candidate.get("name", ""))))
    candidate_version = parse_version(str(candidate.get("name", "")))
    candidate_duration = candidate.get("length")
    candidate_id = candidate.get("id")
    
    for mp3_file in sorted(target_dir.glob("*.mp3")):
        local_title = normalize(strip_version(mp3_file.stem))
        local_version = parse_version(mp3_file.stem)
        
        # Exact API ID match
        if candidate_id:
            from .cli import load_state
            state = load_state()
            for rel_path, entry in state.get("files", {}).items():
                if entry.get("song_id") == candidate_id:
                    return {
                        "status": "exact_duplicate",
                        "existing_file": settings.music_dir / rel_path,
                        "reason": f"Same API ID ({candidate_id})"
                    }
        
        # Title + version exact match
        if local_title == candidate_title:
            if local_version == candidate_version:
                return {
                    "status": "exact_duplicate",
                    "existing_file": mp3_file,
                    "reason": f"Exact title and version match"
                }
            elif local_version is not None and candidate_version is not None:
                return {
                    "status": "different_version",
                    "existing_file": mp3_file,
                    "reason": f"Title matches but v{local_version} vs v{candidate_version}"
                }
    
    return {"status": "new", "existing_file": None, "reason": "Not found in library"}


def validate_mp3(path: Path) -> tuple[bool, str]:
    """
    Validate an MP3 file.
    
    Returns (is_valid, message)
    """
    if not path.exists():
        return False, "File does not exist"
    
    if not path.is_file():
        return False, "Not a file"
    
    if path.suffix.lower() != ".mp3":
        return False, "Not an MP3 file"
    
    if path.stat().st_size < 1024:
        return False, "File too small (< 1KB)"
    
    # Basic MP3 header check
    try:
        with path.open("rb") as f:
            header = f.read(3)
            if header != b"ID3" and header[:2] != b"\xff\xfb":
                return False, "Invalid MP3 header"
    except Exception as e:
        return False, f"Cannot read file: {e}"
    
    return True, "Valid MP3"


def load_manifest(manifest_path: Path) -> list[dict[str, Any]]:
    """
    Load a manifest file with approved resources.
    
    Manifest format (JSON):
    [
        {"id": 123, "title": "Song Name", "version": "v1"},
        ...
    ]
    """
    if not manifest_path.exists():
        raise RuntimeError(f"Manifest not found: {manifest_path}")
    
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise RuntimeError("Manifest must be a JSON array")
        return data
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Invalid manifest JSON: {e}")


def import_local_files(source_dir: Path, target_dir: Path, settings: Any, 
                      allow_duplicates: bool = False) -> dict[str, Any]:
    """
    Import MP3 files from a local directory.
    
    Returns:
    {
        "imported": [list of imported file paths],
        "skipped": [{"file": path, "reason": str}],
        "errors": [{"file": path, "error": str}]
    }
    """
    result = {"imported": [], "skipped": [], "errors": []}
    
    if not source_dir.is_dir():
        raise RuntimeError(f"Source directory not found: {source_dir}")
    
    target_dir.mkdir(parents=True, exist_ok=True)
    
    for mp3_file in sorted(source_dir.glob("*.mp3")):
        # Validate
        valid, msg = validate_mp3(mp3_file)
        if not valid:
            result["errors"].append({"file": str(mp3_file), "error": msg})
            continue
        
        # Check for duplicates
        # (simplified - a real implementation would use the API matcher)
        target_file = target_dir / mp3_file.name
        if target_file.exists():
            if not allow_duplicates:
                result["skipped"].append({
                    "file": str(mp3_file),
                    "reason": f"File already exists at {target_file}"
                })
                continue
            else:
                # Rename with suffix
                stem = target_file.stem
                suffix_num = 1
                while target_file.exists():
                    target_file = target_dir / f"{stem}_{suffix_num}.mp3"
                    suffix_num += 1
        
        # Copy file
        try:
            import shutil
            shutil.copy2(mp3_file, target_file)
            result["imported"].append(str(target_file))
        except Exception as e:
            result["errors"].append({"file": str(mp3_file), "error": str(e)})
    
    return result


def format_search_result(song: dict[str, Any], index: int) -> str:
    """Format a song for search display."""
    name = song.get("name", "Unknown")
    category = song.get("category", "?")
    synced = "SYNCED" if song.get("has_synced_lyrics") else \
             ("PLAIN" if song.get("has_plain_lyrics") else "NONE")
    length = song.get("length") or "?"
    
    lines = [
        f"{index}. {name}",
        f"   Category: {category}  Lyrics: {synced}  Length: {length}",
    ]
    
    if song.get("era"):
        era_name = song["era"].get("name", "") if isinstance(song["era"], dict) else str(song["era"])
        lines.append(f"   Era: {era_name}")
    
    path = song.get("path")
    if path:
        lines.append(f"   Path: {path}")
    
    return "\n".join(lines)
