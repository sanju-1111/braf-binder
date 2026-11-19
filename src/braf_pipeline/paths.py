"""Single source of truth for the Google Drive folder layout."""
from pathlib import Path

DRIVE_ROOT = Path('/content/drive/MyDrive/braf-binder')

SUBDIRS = (
    'config',
    'models/hf_cache',
    'data/targets',
    'data/generation',
    'data/filtering',
    'data/blastdb',
    'data/af3/inputs',
    'data/af3/outputs',
    'data/prodigy',
    'data/ranking',
    'exports',
    'logs',
)


def ensure_layout(root: Path = DRIVE_ROOT) -> Path:
    """Create the folder layout if missing. Safe to call repeatedly,
    including after a Colab disconnect."""
    root = Path(root)
    for sub in SUBDIRS:
        (root / sub).mkdir(parents=True, exist_ok=True)
    return root
