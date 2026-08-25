from __future__ import annotations
from pathlib import Path
from .matching import local_duration

def find_mp3s(music_dir: Path) -> list[Path]:
    if not music_dir.is_dir():
        raise RuntimeError(f"Music directory does not exist: {music_dir}")
    return sorted(music_dir.rglob("*.mp3"), key=lambda p: str(p).lower())
