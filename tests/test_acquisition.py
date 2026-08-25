from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from juice_lyrics.acquisition.manifests import load_manifest
from juice_lyrics.acquisition.downloader import DownloadPolicy
from juice_lyrics.acquisition.models import AcquisitionItem, AcquisitionState


def test_manifest_ignores_comments_and_duplicates(tmp_path):
    manifest = tmp_path / "wanted.txt"
    manifest.write_text("# comment\nRental\n\nBottle\nRental\n", encoding="utf-8")
    assert load_manifest(manifest) == ["Rental", "Bottle"]


def test_models_default_state():
    item = AcquisitionItem(
        identifier="123",
        title="Example",
        url="https://example.invalid/song.mp3",
        destination=Path("song.mp3"),
    )
    assert item.identifier == "123"
    assert AcquisitionState.PENDING.value == "pending"
    assert DownloadPolicy().retries == 3
