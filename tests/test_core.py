from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from juice_lyrics.cli import parse_length, parse_synced_lyrics, patch_rmpc_config


def test_parse_length():
    assert parse_length("4:13") == 253.0
    assert parse_length("1:02:03") == 3723.0


def test_parse_synced_lyrics():
    result = parse_synced_lyrics("[0:01.64] hello\n[0:04.14] world")
    assert result == [("hello", 1640), ("world", 4140)]


def test_rmpc_config_patch_is_safe():
    config = '''#![enable(implicit_some)]\n(\n    cache_dir: Some("/tmp/rmpc/cache"),\n    lyrics_dir: "~/Music",\n)\n'''
    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "config.ron"
        path.write_text(config, encoding="utf-8")
        backup = patch_rmpc_config(path, Path(td) / "lyrics")
        text = path.read_text(encoding="utf-8")
        assert 'lyrics_dir: Some("' in text
        assert 'enable_lyrics_index: true,' in text
        assert 'enable_lyrics_hot_reload: true,' in text
        assert backup.exists()
