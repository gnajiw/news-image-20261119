"""Entry program for make.fun bounty news-image-20261119.

The finished one-day news image is entry.png beside this program.
The program copies it to the grader's output directory, so the judge
sees exactly the bytes committed here. Standard library only.

Local run:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
IMAGE = "entry.png"


def main():
    source = HERE / IMAGE
    if not source.is_file():
        raise SystemExit(f"missing image: {source}")
    data = source.read_bytes()
    # Bounty guardrails: whole PNG, at most 1 MiB, at most 1024x1024.
    if len(data) > 1_048_576:
        raise SystemExit(f"image too large: {len(data)} bytes")
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise SystemExit("image is not a PNG")
    dest = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    dest.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, dest / IMAGE)


if __name__ == "__main__":
    main()
