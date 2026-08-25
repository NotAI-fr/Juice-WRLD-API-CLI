"""Acquisition primitives for explicitly authorized media resources."""

from .models import AcquisitionItem, AcquisitionResult, AcquisitionState
from .downloader import DownloadPolicy, download_to
from .manifests import load_manifest

__all__ = [
    "AcquisitionItem",
    "AcquisitionResult",
    "AcquisitionState",
    "DownloadPolicy",
    "download_to",
    "load_manifest",
]
