"""Front-page publisher for the 25 November 2026 world-news image.

Takes the committed 1024x1024 front page and places an exact copy in the
folder the harness points at. The copy is checked twice — length first,
then a SHA-256 digest — so a truncated or altered write is caught instead
of silently accepted. Nothing is drawn here; the image itself is the entry.
"""

from hashlib import sha256
from os import environ, makedirs
from pathlib import Path


def _digest_of(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _place_verified(source: Path, folder: Path) -> tuple[Path, int, str]:
    makedirs(folder, exist_ok=True)
    target = folder / source.name
    payload = source.read_bytes()
    if payload[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit(f"not a PNG image: {source}")
    target.write_bytes(payload)
    written_size = target.stat().st_size
    written_digest = _digest_of(target)
    if written_size != source.stat().st_size:
        raise SystemExit(f"length mismatch after writing {target}")
    if written_digest != _digest_of(source):
        raise SystemExit(f"digest mismatch after writing {target}")
    return target, written_size, written_digest


def publish() -> None:
    here = Path(__file__).resolve().parent
    front_page = here / "entry.png"
    if not front_page.is_file():
        raise SystemExit(f"missing entry image: {front_page}")
    destination = Path(environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    placed, size, digest = _place_verified(front_page, destination)
    print(f"published {placed} ({size} bytes, sha256 {digest})")


publish()
