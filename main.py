#!/usr/bin/env python3
"""Publish the finished news-image entry.

The entry artwork is the pre-rendered ``entry.png`` that lives next to
this script.  This program simply places a copy of it in the output
directory requested through the ``MAKEFUN_OUTPUT_DIR`` environment
variable, so the make.fun kit can pick it up as this entry's output.
"""

import os
import shutil
import sys
from pathlib import Path


def main() -> int:
    source_image = Path(__file__).resolve().parent / "entry.png"

    if not source_image.is_file():
        print(f"error: entry image not found: {source_image}", file=sys.stderr)
        return 1

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not output_dir:
        print(
            "error: MAKEFUN_OUTPUT_DIR is not set; "
            "run as MAKEFUN_OUTPUT_DIR=<dir> python3 main.py",
            file=sys.stderr,
        )
        return 1

    destination_dir = Path(output_dir)
    destination_dir.mkdir(parents=True, exist_ok=True)

    destination_image = destination_dir / source_image.name
    shutil.copyfile(source_image, destination_image)

    print(destination_image)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
